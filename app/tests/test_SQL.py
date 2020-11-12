from app import db
import time
start = time.time()
result = db.engine.execute('''  SELECT osoba.imie, osoba.nazwisko, osoba."nrTelefonu", COUNT(paczka."idPaczka")  AS liczba_paczek
                                FROM osoba
                                INNER JOIN paczka ON
                                paczka."stanPaczki" =
                                (
                                    SELECT "stanPaczki"."stanPaczki"
                                    FROM "stanPaczki"
                                    WHERE "stanPaczki"."stanPaczkiOpis" = 'wDrodze'
                                )
                                AND
                                paczka."idZamowienie" IN
                                (
                                    SELECT zamowienie."idZamowienie"
                                    FROM zamowienie
                                    WHERE zamowienie."idKurier" = osoba.id
                                )
                                GROUP BY osoba.id
                                ORDER BY liczba_paczek;''')
end = time.time()
print("zapytanie 2:", end - start)

limit_paczek = '10'
nowe_paczki = '3'
limit_waga = '100'
waga_nowych_paczek = '30'
for r in result:
    print(r['imie'])
    print(r['liczba_paczek'])

start = time.time()
result = db.engine.execute('''  INSERT INTO zamowienie ("idKurier", "idKlient", "adresDostawcy", "adresNadawcy",
                                                        "calkowityKosztDostawy", zrealizowana)
                                SELECT kurier.id, 1, 'ul. Rolna 10 80-454 Gdansk', 'ul. Wartowa 80-987 Gdansk', '50', FALSE
                                FROM kurier
                                WHERE ''' + limit_paczek + ''' - ''' + nowe_paczki + ''' >
                                (
                                    SELECT COUNT(*)
                                    FROM paczka
                                    WHERE paczka."idZamowienie" IN 
                                    (
                                        SELECT zamowienie."idZamowienie"
                                        FROM zamowienie
                                        WHERE zamowienie."idKurier" = kurier."id"
                                    )
                                )
                                AND ''' + limit_waga + ''' - ''' + waga_nowych_paczek + ''' >
                                (
                                    SELECT SUM(paczka.waga)
                                    FROM paczka
                                    WHERE paczka."idZamowienie" IN 
                                    (
                                        SELECT zamowienie."idZamowienie"
                                        FROM zamowienie
                                        WHERE zamowienie."idKurier" = kurier."id"
                                    )
                                )
                                LIMIT 1;
                                ''')
end = time.time()
print("zapytanie 1:", end - start)
