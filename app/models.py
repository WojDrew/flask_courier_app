import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import func

from threading import Lock

from app import db, login, enums


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


class NumerZamowienia(db.Model):
    __tablename__ = 'numerZamowienia'

    numerZamowienia = db.Column(db.Integer, primary_key=True)


class NumerPaczki(db.Model):
    __tablename__ = 'numerPaczki'

    numerPaczki = db.Column(db.Integer, primary_key=True)


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
    LOCK = Lock()

    def dodajPaczke(self, package):
        if self.calkowityKosztDostawy is None:
            self.calkowityKosztDostawy = 0
        self.calkowityKosztDostawy = self.calkowityKosztDostawy + package.waga * 4.5
        package.zmienStatus(enums.PackageState.U_nadawcy)
        package.setCode()
        self.paczki.append(package)

    def ustawPrzewidywanaGodzineDostawyiPowiadom(self, time):
        self.przewidywanaGodzinaDostawy = datetime.datetime.combine(self.dataDostawy, time)

    def sfinalizuj(self):
        for package in self.paczki:
            package.zmienStatus(enums.PackageState.Dostarczone)
        self.zrealizowana = True

    @staticmethod
    def getOrderNum():
        with Zamowienie.LOCK:
            orderNum = NumerZamowienia.query.first()
            num = orderNum.numerZamowienia
            orderNum.numerZamowienia = num + 1
            db.session.add(orderNum)
            db.session.commit()
            return num


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
    LOCK = Lock()

    def zmienStatus(self, state):
        self.stanPaczki = state.value

    def setCode(self):
        self.kod = str(self.getPackageCode())

    def getPackageCode(self):
        with Paczka.LOCK:
            packageCode = NumerPaczki.query.first()
            code = packageCode.numerPaczki
            packageCode.numerPaczki = code + 1
            db.session.add(packageCode)
            db.session.commit()
            return code
