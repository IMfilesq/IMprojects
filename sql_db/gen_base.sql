DELETE FROM Archiwum_wycieczek;
DELETE FROM Transakcje_finansowe;
DELETE FROM Oferta_dla_kogo;
DELETE FROM Dla_kogo;
DELETE FROM Oferta_wycieczek;
DELETE FROM Klienci;
DELETE FROM Pracownicy;
DELETE FROM Dane_osobowe;
DELETE FROM Adresy;

DROP TABLE Archiwum_wycieczek,
          Transakcje_finansowe,
          Oferta_dla_kogo,
          Dla_kogo,
          Oferta_wycieczek,    
          Klienci,
          Pracownicy,
          Dane_osobowe,
          Adresy;



CREATE TABLE Adresy
(
  adres_id         INT          NOT NULL AUTO_INCREMENT PRIMARY KEY,
  państwo          VARCHAR (15) NOT NULL,
  miasto           VARCHAR (50) NOT NULL,
  ulica            VARCHAR (100)NOT NULL,
  numer_domu       VARCHAR (10) NOT NULL,
  kod_pocztowy     VARCHAR (10) NOT NULL
) COMMENT 'pracownicy i klienci';



CREATE TABLE Dane_osobowe
(
  dane_id                 INT          AUTO_INCREMENT PRIMARY KEY,
  imię                    VARCHAR (15) ,
  nazwisko                VARCHAR (20) ,
  numer_telefonu          INT          ,
  adres_email             VARCHAR (40) ,
  alarmowy_numer_telefonu INT           COMMENT 'kontakt w razie  wypadku',
  adres_id                INT          ,
  FOREIGN KEY (adres_id) REFERENCES Adresy(adres_id)
) COMMENT 'pracownicy i klienci';


CREATE TABLE Klienci 
(
  klient_id INT  AUTO_INCREMENT PRIMARY KEY,
  dane_id   INT,
  FOREIGN KEY (dane_id) REFERENCES Dane_osobowe(dane_id)
);



CREATE TABLE Pracownicy
(
  pracownik_id  INT          NOT NULL AUTO_INCREMENT,
  dane_id       INT          NOT NULL,
  stanowisko    VARCHAR (30) NOT NULL,
  wynagrodzenie DECIMAL (8,2)NOT NULL    ,
  PRIMARY KEY (pracownik_id),
  FOREIGN KEY (dane_id) REFERENCES Dane_osobowe(dane_id)
);

CREATE TABLE Dla_kogo
(
  dla_kogo_id INT NOT NULL AUTO_INCREMENT,
  dla_kogo VARCHAR(30) NOT NULL,
  PRIMARY KEY (dla_kogo_id)
);

CREATE TABLE Oferta_wycieczek
(
  wycieczka_id      INT            NOT NULL AUTO_INCREMENT,
  nazwa             VARCHAR (100)  NOT NULL    ,
  rodzaj            VARCHAR (40)   NOT NULL    ,
  opis              VARCHAR (500)  NOT NULL    ,
  cena              INT            NOT NULL     COMMENT 'w PLN, za wycieczke',
  cel_podróży       VARCHAR (50)   NOT NULL    ,
  min_limit_osób    INT NOT NULL,
  max_limit_osób    INT      NOT      NULL     DEFAULT 5,
  pracownik_id      INT           NOT NULL,
  koszt_organizacji INT      NOT      NULL    ,
  sezon           set("Wiosna","Lato","Jesień","Zima")  NOT NULL,
  PRIMARY KEY (wycieczka_id),
  FOREIGN KEY (pracownik_id) REFERENCES Pracownicy(pracownik_id)
);


CREATE TABLE Oferta_dla_kogo
(
  oferta_dla_kogo_id INT NOT NULL AUTO_INCREMENT,
  wycieczka_id INT NOT NULL,
  dla_kogo_id INT NOT NULL,
  PRIMARY KEY (oferta_dla_kogo_id),
  FOREIGN KEY (dla_kogo_id) REFERENCES Dla_kogo(dla_kogo_id),
  FOREIGN KEY (wycieczka_id) REFERENCES Oferta_wycieczek(wycieczka_id)
);


CREATE TABLE Transakcje_finansowe
(
  transakcja_id  INT          NOT NULL AUTO_INCREMENT,
  klient_id      INT          NOT NULL,
  tytuł          VARCHAR (40) NOT NULL    ,
  data_płatności DATE NOT NULL    ,
  PRIMARY KEY (transakcja_id),
  FOREIGN KEY (klient_id) REFERENCES Klienci(klient_id)
);

CREATE TABLE Archiwum_wycieczek
(
  archiwum_id   INT          NOT NULL AUTO_INCREMENT,
  wycieczka_id  INT          NOT NULL,
  transakcja_id INT          NOT NULL,
  termin        DATE NOT NULL    ,
  status        VARCHAR (30) NOT NULL,
  liczba_osób   INT NULL,
  PRIMARY KEY (archiwum_id),
  FOREIGN KEY (wycieczka_id)  REFERENCES Oferta_wycieczek (wycieczka_id),
  FOREIGN KEY (transakcja_id) REFERENCES Transakcje_finansowe(transakcja_id)
);



