import csv
import mysql.connector
import random
import pandas
import datetime

paths = {'adres_id':"project_files/adres_id .csv",
         'dane_id':"project_files/dane_id .csv",
         'pracownicy':"project_files/pracownicy.csv",
         'oferta':'project_files/oferta_wycieczek.xlsx'}

db = mysql.connector.connect(
    host="giniewicz.it",      
    user="team12",  
    password="te@mzaiz",  
    database="team12"  
)
cursor = db.cursor()

# wypełniam tabelę adrey
file_path= paths['adres_id']
def dane(file_path):
    with open(file_path, mode="r", encoding='utf-8') as file:
        csv_reader=csv.reader(file, delimiter=';')
        data=list(csv_reader)
        data=data[1:]
    return data 

data=dane(file_path)
losowe_wiersze=random.sample(data, 50)
zapytanie="INSERT INTO Adresy (państwo, miasto, ulica, numer_domu, kod_pocztowy) VALUES (%s,%s,%s,%s,%s)"
cursor.executemany(zapytanie, losowe_wiersze)
db.commit()

#wypełniam tabelę dane osobowe

cursor.execute("SELECT adres_id from Adresy")
id=cursor.fetchall()
lista1=[]
for i in range(len(id)):
    lista1.append(list(id[i]))
lista1= [[str(x[0])] for x in lista1]
random.shuffle(lista1)

file_path= paths['dane_id']
def dane(file_path):
    with open(file_path, mode="r", encoding='utf-8') as file:
        csv_reader=csv.reader(file, delimiter=';')
        data=list(csv_reader)
        data=data[1:]
    return data 
data=dane(file_path)
losowe_wiersze=random.sample(data, 50)
lista=[]
for i in range(len(id)):
    lista.append(losowe_wiersze[i]+lista1[i])

zapytanie="INSERT INTO Dane_osobowe (imię, nazwisko, numer_telefonu, adres_email, alarmowy_numer_telefonu, adres_id) VALUES (%s,%s,%s,%s,%s,%s)"
cursor.executemany(zapytanie, lista)
db.commit()

#wypełniam tabelę Klienci

cursor.execute("SELECT dane_id from Dane_osobowe order by dane_id")
numery=cursor.fetchall()
losowe_id=random.sample(numery,40)
zapytanie="INSERT INTO Klienci (dane_id) VALUES (%s)"
cursor.executemany(zapytanie, losowe_id)
db.commit()

#dodaję tabelę pracownicy

id_pozostałe=[id for id in numery if id not in losowe_id]
id=[]
for i in range(len(id_pozostałe)):
    id.append(list(id_pozostałe[i]))
id= [[str(x[0])] for x in id]
random.shuffle(id)
file_path= paths['pracownicy']
def dane(file_path):
    with open(file_path, mode="r", encoding='utf-8') as file:
        csv_reader=csv.reader(file, delimiter=';')
        data=list(csv_reader)
        data=data[1:]
    return data 
data=dane(file_path)
organizator=[wiersz for wiersz in data if wiersz[0]=='Organizator']
losuje_organizatora=random.sample(organizator,3)

przewodnik=[wiersz for wiersz in data if wiersz[0]=='Przewodnik']
losuje_przewodnika=random.sample(przewodnik,3)

kierownik=[wiersz for wiersz in data if wiersz[0]=='Kierownik']
losuje_kierownika=random.sample(kierownik,2)

prezes=[wiersz for wiersz in data if wiersz[0]=='Prezes']
losuje_prezesa=random.sample(prezes,2)

losowe_wiersze=losuje_organizatora+losuje_przewodnika+losuje_kierownika+losuje_prezesa
random.shuffle(losowe_wiersze)
lista=[]
for i in range(len(id)):
    lista.append(id[i]+losowe_wiersze[i])
zapytanie="INSERT INTO Pracownicy (dane_id, stanowisko, wynagrodzenie) VALUES (%s,%s,%s)"
cursor.executemany(zapytanie, lista)
db.commit()

    
#wczytuję ofertę z pliku
oferta_wycieczek = pandas.read_excel(paths['oferta'])


#generuje losowe ceny wycieczek

def randomize_price(price,cost):
    difference = int((price - cost)*0.7)
    rand_difference = random.choice(range(-difference, difference,1))
    rand_difference = round(rand_difference/10)*10
    return rand_difference + price


oferta_wycieczek['cena'] = [randomize_price(price,cost) for price,cost in zip(oferta_wycieczek['cena'],oferta_wycieczek['koszt_organizacji'])]


#wstawiam orcanizatorów do oferty wycieczek
cursor.execute("SELECT pracownik_id FROM Pracownicy WHERE stanowisko LIKE 'Organizator' LIMIT 10")
pracownik_id = cursor.fetchall()
pracownik_id = [x[0] for x in pracownik_id]
oferta_pracownik_id = random.choices(population = pracownik_id,k = 10)
oferta_wycieczek['pracownik_id'] = oferta_pracownik_id


#wstawiam dane do tableli oferta_wycieczek
for_who_map = [i.replace(" ", "").split(',') for i in oferta_wycieczek['dla_kogo']]
oferta_wycieczek = oferta_wycieczek.drop(columns=['dla_kogo'])
oferta_insert_query = "INSERT INTO Oferta_wycieczek (nazwa, rodzaj, opis, cena, cel_podróży, min_limit_osób, max_limit_osób, pracownik_id, koszt_organizacji, sezon) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
for index, row in oferta_wycieczek.iterrows():
    cursor.execute(oferta_insert_query, tuple(row))
db.commit()

#Wypełniam tabelę Dla_kogo oraz zapamiętuje odpowiedznie klucze
for i in ['firma','grupa_zorganizowana','szkoła']:
    cursor.execute("INSERT INTO Dla_kogo (dla_kogo) VALUES (%s)", [i])
db.commit()

cursor.execute("SELECT * FROM Dla_kogo")
for_who_id = cursor.fetchall()
for_who_id = {i[1]:i[0] for i in for_who_id}

for index, for_who_list in enumerate(for_who_map):
    for j in for_who_list:
        cursor.execute("INSERT INTO Oferta_dla_kogo (wycieczka_id,dla_kogo_id) VALUES (%s,%s)", [index+1,for_who_id[j]])
db.commit()

 

#tworzę ramkę  z płatnościami
transakcje_finansowe = pandas.DataFrame(columns = ['klient_id',
                                                   'tytuł',
                                                   'data_płatności'])

#wstawiam do ramki id klienów
get_klient_id_query = "SELECT klient_id FROM Klienci"
cursor.execute(get_klient_id_query)
transakcje_klient_id = tuple(cursor.fetchall())
transakcje_klient_id = random.choices(transakcje_klient_id,k = 500)
transakcje_klient_id = [x[0] for x in transakcje_klient_id]
transakcje_finansowe['klient_id'] = transakcje_klient_id

#tworzę funkcję generującą daty i wstawiam je do ramki z płatnościami
#przy okazji mapuję daty do id wycieczek, tak aby zgadzał się sezon
#wektor z takimi id będzie wykorzystany później przy tworzeniu archiwum 

 
def get_date1():
    first_day = random.choices(population = [i for i in range(180)],
                                k=1)
    delta1 = datetime.timedelta(first_day[0])
    following_day = random.choices(population = [i for i in range(180)],
                                k=1)
    delta2 = datetime.timedelta(following_day[0]) + delta1
    return (datetime.date(2024,1,1) + delta1, datetime.date(2024,1,1) + delta2)

def get_date2():
    first_day = random.choices(population = [i for i in range(365)],
                                k=1)
    delta1 = datetime.timedelta(first_day[0])
    following_day = random.choices(population = [i for i in range(365,730)],
                                k=1)
    delta2 = datetime.timedelta(following_day[0]) + delta1
    return (datetime.date(2024,1,1) + delta1, datetime.date(2024,1,1) + delta2)

def get_date3():
    first_day = random.choices(population = [i for i in range(365)],
                                k=1)
    delta1 = datetime.timedelta(first_day[0])
    following_day = random.choices(population = [i for i in range(720-first_day[0])],
                                k=1)
    delta2 = datetime.timedelta(following_day[0]) + delta1
    return (datetime.date(2024,1,1) + delta1, datetime.date(2024,1,1) + delta2)

wycieczka_sezon = {'Wiosna' : [],
                'Lato' : [],
                'Jesień' : [],
                'Zima' : []}

for id, season_list in enumerate(oferta_wycieczek['sezon']):
    for season in season_list.split(','):
        wycieczka_sezon[season].append(id+1)

def get_wycieczka_id(date):
    if date.month in [3,4,5]:
        season =  "Wiosna"
    elif date.month in [6,7,8]:
        season = "Lato"
    elif date.month in [9,10,11]:
        season  = "Jesień"
    else:
        season = "Zima"
    return random.choice(wycieczka_sezon[season])


daty = [get_date1() for i in range(225)] + [get_date2() for i in range(225)] + [get_date3() for i in range(50)]

wycieczka_id = [get_wycieczka_id(x[1]) for x in daty]

#while len(set(wycieczka_id)) < 5:
#    daty = [get_date1() for i in range(225)] + [get_date2() for i in range(225)] + [get_date3() for i in range(50)]
#    wycieczka_id = [get_wycieczka_id(date[1]) for date in daty]

transakcje_finansowe['data_płatności'] = [str(x[0]) for x in daty]

#generuję tytuły i wstawiam je do ramki z płatnościami
tytuły_transakcji = ["wycieczka z dnia " + str(x[1]) for x in daty]
transakcje_finansowe['tytuł'] = tytuły_transakcji

#wstawiam ramkę z płatnościami do bazy dancyh
transakcje_insert_query = "INSERT INTO Transakcje_finansowe (klient_id,tytuł, data_płatności) VALUES (%s, %s, %s)"
for index, row in transakcje_finansowe.iterrows():
    cursor.execute(transakcje_insert_query, tuple(row))
db.commit()

#tworzę ramkę z archiwum wycieczek
archiwum_wycieczek = pandas.DataFrame(columns = ['wycieczka_id','transakcja_id','termin','status'])

#wstawiam transakcje id do ramki archiwum
transakcja_id_query = "SELECT transakcja_id FROM Transakcje_finansowe order by transakcja_id"

cursor.execute(transakcja_id_query)
transakcja_id = cursor.fetchall()

transakcja_id = [x[0] for x in transakcja_id]
archiwum_wycieczek['transakcja_id'] = transakcja_id

#wstawiam termin do ramki z archiwum
archiwum_wycieczek['termin'] = [str(x[1]) for x in daty]
#wstawiam status do ramki z archiwum
def get_status(date):
    if date > (datetime.datetime.now()).date():
        return "zaplanowana"
    else:
        return "odbyła się"
    
status = [get_status(x[1]) for x in daty]
archiwum_wycieczek['status'] = status


#wstawiam wycieczka id do ramki z archiwum

archiwum_wycieczek['wycieczka_id'] = wycieczka_id

#wstawiam liczbę osób do ramki z archiwum
cursor.execute("SELECT wycieczka_id, max_limit_osób, min_limit_osób FROM Oferta_wycieczek ORDER BY wycieczka_id")
t = cursor.fetchall()
nof_people = [random.choice(range(t[i-1][2],t[i-1][1] + 5)) for i in archiwum_wycieczek['wycieczka_id'] ]
for index,element in enumerate(nof_people):
    if archiwum_wycieczek['status'][index] == "zaplanowana" :
        nof_people[index] = None
archiwum_wycieczek['liczba_osób'] =  nof_people

#wstawiam ramkę archiwum do archiwum w bazie

archiwum_insert_query = "INSERT INTO Archiwum_wycieczek (wycieczka_id, transakcja_id, termin, status, liczba_osób) VALUES (%s,%s,%s,%s,%s)"
for index, row in archiwum_wycieczek.iterrows():
    row = [None if pandas.isna(x) else x for x in row]
    cursor.execute(archiwum_insert_query, tuple(row))
db.commit()
