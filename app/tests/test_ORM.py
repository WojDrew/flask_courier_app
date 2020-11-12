from app import db
from app.models import Osoba, Paczka, StanPaczki, Zamowienie, Kurier
from sqlalchemy import func, and_
from sqlalchemy.sql import insert, select, text
import time

start = time.time()
result = Osoba.query\
    .join(Paczka,
          and_(Paczka.stanPaczki == StanPaczki.query.filter(StanPaczki.stanPaczkiOpis == 'wDrodze')\
               .with_entities(StanPaczki.stanPaczki),
          Paczka.idZamowienie.in_(Zamowienie.query.filter(Zamowienie.idKurier == Osoba.id)
               .with_entities(Zamowienie.idZamowienie))))\
    .with_entities(Osoba.imie, Osoba.nazwisko, Osoba.nrTelefonu, func.count(Paczka.idPaczka).label('liczba_paczek'))\
    .group_by(Osoba.id)\
    .order_by('liczba_paczek')
end = time.time()
print("zapytanie 2:", end - start)
for r in result:
    print(r.imie)
    print(r.liczba_paczek)

limit_paczek = 10
nowe_paczki = 3
limit_waga = 100
waga_nowych_paczek = 30

start = time.time()
result2 = insert(Zamowienie)\
    .from_select(['idKurier', 'idKlient', 'adresDostawcy', 'adresNadawcy', 'calkowityKosztDostawy', 'zrealizowana'],
                 select([Kurier.id, 1, text("'ul. Internetowa 10 80-111 Gdansk'"), text("'ul. Duza 80-127 Gdansk'"), text("'50'"), False]).where(
                     and_(limit_paczek - nowe_paczki > (select([func.count(Paczka.idPaczka)]).where(
                         Paczka.idZamowienie.in_(
                             select([Zamowienie.idZamowienie]).where(
                                 Zamowienie.idKurier == text("kurier.id")
                             )
                         )
                     )).as_scalar(), limit_waga - waga_nowych_paczek > select([func.sum(Paczka.waga)]).where(
                         Paczka.idZamowienie.in_(
                             select([Zamowienie.idZamowienie]).where(
                                 Zamowienie.idKurier == text("kurier.id")
                             )
                         )
                     ).as_scalar())
                 ).limit(1))
db.engine.execute(result2)
end = time.time()
print("zapytanie 1:", end - start)
