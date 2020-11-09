from flask import render_template, url_for, flash, request
from werkzeug.utils import redirect
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user

from app import app_instance
from app import db
from app.forms import *
from app.models import *

import datetime


@app_instance.route('/')
@app_instance.route('/index')
def index():
    return render_template('index.html', title='KurierPol')


@app_instance.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.isKurier.data:
            osoba = Kurier(eMail=form.email.data,
                           imie=form.imie.data,
                           nazwisko=form.nazwisko.data,
                           nrTelefonu=form.nrTelefonu.data,
                           PESEL=form.pesel.data)
        else:
            osoba = Klient(eMail=form.email.data,
                           imie=form.imie.data,
                           nazwisko=form.nazwisko.data,
                           nrTelefonu=form.nrTelefonu.data,
                           PESEL=form.pesel.data,
                           adres=form.adres.data)
        osoba.set_password(form.password.data)
        db.session.add(osoba)
        db.session.commit()
        flash("Rejestracja zakonczyla sie powodzeniem")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app_instance.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        osoba = Osoba.query.filter_by(eMail=form.email.data).first()
        if osoba is None or not osoba.check_password(form.password.data):
            flash('Niepoprawne email lub haslo')
            return redirect(url_for('login'))
        login_user(osoba, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app_instance.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app_instance.route('/zamow', methods=['GET', 'POST'])
def make_order():
    if current_user.is_authenticated:
        form = OrderTakeForm()
        if form.validate_on_submit():
            if not len(form.paczki.data) > 0:
                flash("Zamowienie musi skladac sie z przynajmniej jednej paczki")
                return redirect(url_for('make_order'))
            kurier = Kurier.find_free_courier()
            zamowienie = Zamowienie(klient=current_user, kurier=kurier, adresDostawcy=form.adresOdbiorcy.data,
                                    adresNadawcy=form.adresNadawcy.data, dataDostawy=form.dataDostawy.data,
                                    zrealizowana=False)
            for waga in form.paczki.data:
                zamowienie.dodajPaczke(Paczka(waga=float(waga)))
            db.session.add(zamowienie)
            db.session.commit()
            flash("Zamowienie za kwote {} zostalo zlozone".format(zamowienie.calkowityKosztDostawy))
            return redirect(url_for('index'))
        return render_template('take_order.html', title='Zloz Zamowienie', form=form)
    else:
        return redirect(url_for('login'))

@app_instance.route('/zamowienie', methods=['GET', 'POST'])
def order_view_client():
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    elif request.args.get('id') is None or not request.args.get('id').isdecimal():
        return redirect(url_for('index'))
    elif isinstance(current_user, Kurier):
        return redirect(url_for('order_view_courier', id=request.args.get('id')))

    zamowienie = Zamowienie.query.filter_by(idZamowienie=request.args.get('id')).first()
    if zamowienie is None or not zamowienie in current_user.zamowienia:
        flash("Brak zamowienia")
        return redirect(url_for('index'))

    senderForm = OrderFormSenderAddress()
    recipientForm = OrderFormRecipientAddress()
    dateForm = OrderFormDate()

    if senderForm.validate_on_submit():
        zamowienie.adresNadawcy = senderForm.adresNadawcy.data
        db.session.add(zamowienie)
        db.session.commit()

    if recipientForm.validate_on_submit():
        zamowienie.adresDostawcy = recipientForm.adresOdbiorcy.data
        db.session.add(zamowienie)
        db.session.commit()

    if dateForm.validate_on_submit():
        zamowienie.dataDostawy = dateForm.dataDostawy.data
        db.session.add(zamowienie)
        db.session.commit()

    return render_template('order_client_view.html', zamowienie=zamowienie, recipientForm=recipientForm,
                           senderForm=senderForm, dateForm=dateForm)


@app_instance.route('/zamowienie_kurier', methods=['GET', 'POST'])
def order_view_courier():
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    elif request.args.get('id') is None or not request.args.get('id').isdecimal():
        return redirect(url_for('index'))
    elif isinstance(current_user, Klient):
        return redirect(url_for('order_view_client', id=request.args.get('id')))

    zamowienie = Zamowienie.query.filter_by(idZamowienie=request.args.get('id')).first()
    if zamowienie is None or not zamowienie in current_user.zamowienia:
        flash("Brak zamowienia")
        return redirect(url_for('index'))

    dateTimeForm = OrderFormDateTime()
    finalizeForm = FinalizeOrderForm()

    if dateTimeForm.validate_on_submit():
        zamowienie.przewidywanaGodzinaDostawy = datetime.datetime.combine(zamowienie.dataDostawy,
                                                                          dateTimeForm.godzinaDostawy.data)
        db.session.add(zamowienie)
        db.session.commit()

    if finalizeForm.validate_on_submit():
        zamowienie.zrealizowana = True
        db.session.add(zamowienie)
        db.session.commit()

    return render_template('order_courier_view.html', zamowienie=zamowienie, dateTimeForm=dateTimeForm, finalizeForm=finalizeForm)