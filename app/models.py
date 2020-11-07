from app import db


class Osoba(db.Model):
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