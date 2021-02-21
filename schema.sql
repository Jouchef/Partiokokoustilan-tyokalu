CREATE TABLE paivakirja
(id SERIAL PRIMARY KEY, pvm DATE DEFAULT CURRENT_DATE, merkinta TEXT, kukakirjoitti TEXT);

INSERT INTO paivakirja (merkinta, kukakirjoitti)
VALUES ('Olimme ryhmän kanssa puistossa ja laskimme mäkeä, kun satoi niin paljon lunta', 'Joosef');

INSERT INTO paivakirja (merkinta, kukakirjoitti)
VALUES ('Nikkaroimme sudarien kanssa linnunpönttöä. Ensi kerralla viemme sen luontoon.', 'Jani-Petteri');





CREATE TABLE tavaralistaus
(tuote TEXT, kuvaus TEXT, maara INTEGER, id SERIAL PRIMARY KEY);

INSERT INTO tavaralistaus (tuote, kuvaus, maara)
VALUES ('Lumilapio', 'Fiskarsin vanha', 2);

INSERT INTO tavaralistaus (tuote, kuvaus, maara)
VALUES ('Myrskylyhty', 'Hopeinen pieni', 7);

INSERT INTO tavaralistaus (tuote, kuvaus, maara)
VALUES ('Makuualusta', 'Ohut', 3);

INSERT INTO tavaralistaus (tuote, kuvaus, maara)
VALUES ('Tulitikku', 'Aski', 100);





CREATE TABLE users
(id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT, role TEXT);

INSERT INTO users (username, password, role)
VALUES ('sadmin@sadmin.sadmin', 'pbkdf2:sha256:150000$RycREZON$f1a586c9cf0c62d9973854972684c4505c9f18161635ff39f3dc379cd9232b32', 'sadmin');

INSERT INTO users (username, password, role)
VALUES ('admin@admin.admin', 'pbkdf2:sha256:150000$0ZoDK7GW$73dd38394ae61cf60edb81a5651b6a5d7a0ba2b78d41026a468815c60f06f3e0', 'admin');





CREATE TABLE laskuri 
(id SERIAL PRIMARY KEY, realpvm DATE DEFAULT CURRENT_DATE, ryhma TEXT, pvm DATE, nuoria INTEGER, aikuisia INTEGER, ulkopaikkakuntalainen INTEGER);

INSERT INTO laskuri (ryhma, pvm, nuoria, aikuisia, ulkopaikkakuntalainen)
VALUES ('Ryhmä A', '2021-02-21', 10, 2, 1);

INSERT INTO laskuri (ryhma, pvm, nuoria, aikuisia, ulkopaikkakuntalainen)
VALUES ('Tulitähdet', '2021-02-20', 13, 3, 0);

INSERT INTO laskuri (ryhma, pvm, nuoria, aikuisia, ulkopaikkakuntalainen)
VALUES ('Puumat', '2021-02-19', 9, 2, 0);