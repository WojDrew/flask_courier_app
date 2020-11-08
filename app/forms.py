from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.fields.html5 import DateField

from datetime import date

from app.models import Osoba


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    imie = StringField('Imie', validators=[DataRequired()])
    nazwisko = StringField('Nazwisko', validators=[DataRequired()])
    nrTelefonu = StringField('nr Telefonu', validators=[DataRequired()])
    pesel = StringField('PESEL', validators=[DataRequired()])
    adres = StringField('adres', )
    password = PasswordField('Haslo', validators=[DataRequired()])
    password2 = PasswordField('Powtorz Haslo', validators=[DataRequired(), EqualTo('password')])
    isKurier = BooleanField('Chce sie zarejestrowac jako kurier')
    submit = SubmitField('Zarejestruj')

    def validate_nrTelefonu(self, phoneNumber):
        if len(phoneNumber.data) > 12 or len(phoneNumber.data) < 9 or not phoneNumber.data.isdecimal():
            raise ValidationError('Wprowadz poprawny nr telefonu')

    def validate_pesel(self, pesel):
        if not len(pesel.data) == 11 or not pesel.data.isdecimal():
            raise ValidationError('Wprowadz poprawny nr PESEL')

    def validate_email(self, email):
        osoba = Osoba.query.filter_by(eMail=email.data).first()
        if osoba is not None:
            raise ValidationError('Email juz istnieje')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Haslo', validators=[DataRequired()])
    remember_me = BooleanField('Zapamietaj mnie')
    submit = SubmitField('Zaloguj')


class OrderTakeForm(FlaskForm):
    adresNadawcy = StringField('Adres Nadawcy', validators=[DataRequired()])
    adresOdbiorcy = StringField('Adres Odbiorcy', validators=[DataRequired()])
    dataDostawy = DateField('Data Dostawy', validators=[DataRequired()])
    paczki = FieldList(StringField(), 'Paczki:')
    submit = SubmitField('Zloz')

    def validate_dataDostawy(self, data):
        if data.data < date.today():
            raise ValidationError('Data podana musi byc poxniejsza niz dzisiejsza')
