from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import func

from app import db
from app import login


@login.user_loader
def load_user(id):
    return Osoba.query.get(int(id))

class Osoba(UserMixin, db.Model):
    __tablename__ = 'osoba'

    id = db.Column(db.Integer, primary_key=True)
    eMail = db.Column(db.String(100), index=True, unique=True)
    password = db.Column(db.String(128))
    imie = db.Column(db.String(100))
    nazwisko = db.Column(db.String(100))
    nrTelefonu = db.Column(db.String(12), unique=True)
    PESEL = db.Column(db.String(11), unique=True)
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity':'osoba',
        'polymorphic_on':type
    }
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Klient(Osoba):
    __tablename__ = 'klient'

    id = db.Column(db.Integer, db.ForeignKey(Osoba.id), primary_key=True)
    adres = db.Column(db.String(100))
    zamowienia = db.relationship("Zamowienie", backref="klient", lazy="dynamic")

    __mapper_args__ = {
        'polymorphic_identity':'klient',
    }


class Kurier(Osoba):
    __tablename__ = 'kurier'

    id = db.Column(db.Integer, db.ForeignKey(Osoba.id), primary_key=True)
    aktualnePolozenie = db.Column(db.JSON)
    zamowienia = db.relationship("Zamowienie", backref="kurier", lazy="dynamic")

    __mapper_args__ = {
        'polymorphic_identity':'kurier',
    }

    @staticmethod
    def find_free_courier():
        kurier = db.session.query(Kurier.id).outerjoin(Zamowienie).order_by(
            func.count(Zamowienie.idZamowienie)).group_by(Kurier.id).first()
        return Kurier.query.get(kurier.id)


class Zamowienie(db.Model):
    __tablename__ = 'zamowienie'

    idZamowienie = db.Column(db.Integer, primary_key=True)
    idKurier = db.Column(db.Integer, db.ForeignKey(Kurier.id))
    idKlient = db.Column(db.Integer, db.ForeignKey(Klient.id))
    adresDostawcy = db.Column(db.String(256))
    adresNadawcy = db.Column(db.String(256))
    calkowityKosztDostawy = db.Column(db.Float(8))
    dataDostawy = db.Column(db.Date)
    dataZaplaty = db.Column(db.DateTime)
    przewidywanaGodzinaDostawy = db.Column(db.DateTime)
    zrealizowana = db.Column(db.Boolean)
    paczki = db.relationship("Paczka", backref="zamowienie", lazy="dynamic")

    def dodajPaczke(self, paczka):
        if self.calkowityKosztDostawy is None:
            self.calkowityKosztDostawy = 0
        self.calkowityKosztDostawy = self.calkowityKosztDostawy + paczka.waga * 4.5
        self.paczki.append(paczka)


class StanPaczki(db.Model):
    __tablename__ = "stanPaczki"

    stanPaczki = db.Column(db.Integer, primary_key=True)
    stanPaczkiOpis = db.Column(db.String(256))


class Paczka(db.Model):
    __tablename__ = 'paczka'

    idPaczka = db.Column(db.Integer, primary_key=True)
    idZamowienie = db.Column(db.Integer, db.ForeignKey(Zamowienie.idZamowienie))
    dataOdbioru = db.Column(db.DateTime)
    kod = db.Column(db.String(128))
    waga = db.Column(db.Float(8))
    stanPaczki = db.Column(db.Integer, db.ForeignKey(StanPaczki.stanPaczki))