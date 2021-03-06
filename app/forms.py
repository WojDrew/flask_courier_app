from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.fields.html5 import TimeField, DateField

from datetime import date

from app.models import Osoba


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Imie', validators=[DataRequired()])
    surname= StringField('Nazwisko', validators=[DataRequired()])
    phoneNumber = StringField('nr Telefonu', validators=[DataRequired()])
    pesel = StringField('PESEL', validators=[DataRequired()])
    address = StringField('adres', )
    password = PasswordField('Haslo', validators=[DataRequired()])
    password2 = PasswordField('Powtorz Haslo', validators=[DataRequired(), EqualTo('password')])
    isKurier = BooleanField('Chce sie zarejestrowac jako kurier')
    submit = SubmitField('Zarejestruj')

    def validate_phoneNumber(self, phoneNumber):
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
    senderAddress = StringField('Adres nadawcy:', validators=[DataRequired()])
    recipientAddress = StringField('Adres odbiorcy:', validators=[DataRequired()])
    deliveryDate = DateField('Data dostawy:', validators=[DataRequired()])
    packages = FieldList(StringField(), 'Paczki:')
    submit = SubmitField('Zloz')

    def validate_deliveryDate(self, data):
        if data.data < date.today():
            raise ValidationError('Data podana musi byc poxniejsza niz dzisiejsza')


class OrderFormSenderAddress(FlaskForm):
    senderAddress = StringField('Adres nadawcy:', validators=[DataRequired()])
    submit = SubmitField('Zmien')


class OrderFormRecipientAddress(FlaskForm):
    recipientAddress = StringField('Adres odbiorcy:', validators=[DataRequired()])
    submit = SubmitField('Zmien')


class OrderFormDate(FlaskForm):
    deliveryDate = DateField('Data dostawy:', validators=[DataRequired()])
    submit = SubmitField('Zmien')

    def validate_deliveryDate(self, data):
        if data.data < date.today():
            raise ValidationError('Data podana musi byc poxniejsza niz dzisiejsza')


class OrderFormTime(FlaskForm):
    deliveryTime = TimeField('Przewidywana godzina dostawy:', validators=[DataRequired()])
    submit = SubmitField('Zmien')


class FinalizeOrderForm(FlaskForm):
    finalized = RadioField('Dostarczono', validators=[DataRequired()], choices=[('y', "Tak"), ('n', 'Nie')])
    submit = SubmitField("Sfinalizuj")
