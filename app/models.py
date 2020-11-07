from app import db


class Osoba(db.Model):
    __tablename__ = 'osoba'

    id = db.Column(db.Integer, primary_key=True)
    eMail = db.Column(db.String(100), index=True, unique=True)
    password = db.Column(db.String(128), unique=True)
    imie = db.Column(db.String(100))
    nazwisko = db.Column(db.String(100))
    nrTelefonu = db.Column(db.String(12))
    PESEL = db.Column(db.String(11))
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity':'osoba',
        'polymorphic_on':type
    }

class Klient(Osoba):
    __tablename__ = 'klient'

    id = db.Column(db.Integer, db.ForeignKey(Osoba.id), primary_key=True)
    adres = db.Column(db.String(100))

    __mapper_args__ = {
        'polymorphic_identity':'klient',
    }

class Kurier(Osoba):
    __tablename__ = 'kurier'

    id = db.Column(db.Integer, db.ForeignKey(Osoba.id), primary_key=True)
    aktualnePolozenie = db.Column(db.JSON)

    __mapper_args__ = {
        'polymorphic_identity':'kurier',
    }