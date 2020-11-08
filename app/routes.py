from flask import render_template, url_for, flash, request
from werkzeug.utils import redirect
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user

from app import app_instance
from app import db
from app.forms import RegistrationForm, LoginForm, OrderTakeForm
from app.models import *


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
                zamowienie.dodajPaczke(Paczka(dataOdbioru=form.dataDostawy.data, waga=float(waga)))
            db.session.add(zamowienie)
            db.session.commit()
            flash("Zamowienie za kwote {} zostalo zlozone".format(zamowienie.calkowityKosztDostawy))
            return redirect(url_for('index'))
        return render_template('take_order.html', title='Zloz Zamowienie', form=form)
    else:
        return redirect(url_for('login'))

