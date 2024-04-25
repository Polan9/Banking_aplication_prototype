import random
import sqlite3
from abc import ABC, abstractmethod
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
import PyQt5
from PyQt5.QtWidgets import QApplication, QLabel,QWidget, QVBoxLayout, QPushButton,QFormLayout,QMainWindow
import sys


class app():
    conn = sqlite3.connect("klienci_db")
    cursor = conn.cursor()

    create_table = """

    CREATE TABLE IF NOT EXISTS klienci (
    id INTEGER PRIMARY KEY , 
    Imie TEXT NOT NULL,
    Nazwisko TEXT NOT NULL,
    Stan_konta INTEGER

    );
    """

    cursor.execute(create_table)
    conn.commit()

    login = input("podaj Imie")
    login2 = input("podaj Nazwisko")



    class SqlMethods:
        def __init__(self):
            self.conn = sqlite3.connect("klienci_db")
            self.cursor = self.conn.cursor()

        @staticmethod
        def insert3_data(self, row, row2, row3, value, value2, value3):
            data = f"""

                 INSERT INTO klienci ({str(row)},{str(row2)},{str(row3)}) VALUES ("{value}","{value2}","{value3}",);

            """
            self.cursor.execute(data)

    class Klient:
        def __init__(self, imie, nazwisko, id_konta):
            self.imie = imie
            self.nazwisko = nazwisko
            self.id_konta = id_konta

    class Konto(Klient):
        def __init__(self, stan_konta, imie, nazwisko, id_konta, waluta):
            self.is_run = True
            self.stan_konta = stan_konta
            self.waluta = waluta
            super().__init__(imie, nazwisko, id_konta)
            self.conn = sqlite3.connect("klienci_db")
            self.cursor = self.conn.cursor()

        def update_task(self):
            sql = f"""

            UPDATE klienci SET Stan_konta = {self.stan_konta} WHERE id={self.id_konta}


            """
            self.cursor.execute(sql)
            self.conn.commit()

        def Zapisanie_db(self):
            Insert_data = f"""


            INSERT INTO klienci (Imie,Nazwisko,Stan_konta) VALUES ("{self.imie}","{self.nazwisko}","{self.stan_konta}");

            """

            get_data = "SELECT Imie,Nazwisko FROM klienci"
            self.cursor.execute(get_data)
            res = self.cursor.fetchall()
            is_in_data_base = False

            if len(res) == 0:
                self.cursor.execute(Insert_data)
                print("lista pusta dodany")
            get_data = "SELECT Imie,Nazwisko FROM klienci"
            self.cursor.execute(get_data)
            res = self.cursor.fetchall()

            for row in res:

                if row[0] == self.imie and row[1] == self.nazwisko:
                    is_in_data_base = True
                    break
                else:
                    is_in_data_base = False

            if is_in_data_base == False:
                self.cursor.execute(Insert_data)
                print("Dodany1")
            else:
                print("Jest w bazie danych")

            self.conn.commit()

        def info(self, konto):
            print(f"Włascciel: {konto.imie} {konto.nazwisko}\n"
                  f"Id Konta: {konto.id_konta}\n"
                  f"Stan Konta: {konto.stan_konta}\n"
                  f"Waluta:{konto.waluta}")

        def usun_z_db(self):
            id_us = input("Podaj Id klietna do usuniecia")
            delete = f"""

            DELETE FROM klienci WHERE id= {id_us}

            """
            self.cursor.execute(delete)
            self.conn.commit()

    class Aktualizacja(Konto):
        def __init__(self, stan_konta, imie, nazwisko, id_konta, waluta):
            super().__init__(stan_konta, imie, nazwisko, id_konta, waluta)

        def dodaj(self, value, konto):
            konto.stan_konta += value

        def usun(self, value, konto):
            konto.stan_konta -= value

        def poka(self, konto):
            print(konto.stan_konta)

    class Karta(Klient):
        def __init__(self, imie, nazwisko, id_konta):
            self.numer_karty = None
            self.data_waz = None
            self.pin = None
            super().__init__(imie, nazwisko, id_konta)

        def dane_karty(self):
            print(f"numer karty: {self.numer_karty}\n"
                  f"Pin: {self.pin}\n"
                  f"data waznosci {self.data_waz}")

        def generuj_nowa(self):
            numer = ""
            for i in range(16):
                i = random.randrange(0, 9)
                numer += str(i)
            self.numer_karty = numer

            pin_numer = ""
            for i in range(4):
                i = random.randrange(0, 9)
                pin_numer += str(i)
            self.pin = pin_numer

            data_waz = ""
            dzien = random.randrange(1, 30)
            miesiac = random.randrange(1, 12)
            data_waz += str(dzien)
            data_waz += "/"
            data_waz += str(miesiac)
            self.data_waz = str(data_waz)
            print(f"Nowy numer karty: {self.numer_karty}\n"
                  f"Nowy Pin: {self.pin}\n"
                  f"Nowa data waznosci {self.data_waz}")

        def poka(self):
            print(self.numer_karty)


    class API_currency(ABC):
        @abstractmethod
        def Kurs(self):
            api_key = "aqmTVkGy8uLnyex5Q6Bwy7PpvBM42G"
            r = requests.get(f"https://www.amdoren.com/api/currency.php?api_key={api_key}")
            print(r.text)



    class Menu(API_currency):
        def __init__(self):
            akcja = 0

        def menu_logic(self, konto, aktualizacja, karta):
            print(f"1. Dane Konta\n"
                  f"2. Przelewy\n"
                  f"3. Karta Debetowa\n"
                  f"4. Kantor\n"
                  f"5. Zakoncz")

            akcja = input("Wybierz akcje")

            match akcja:
                case "1":
                    konto.info(konto)
                case "2":
                    print(f"1. Dodaj Srodki\n"
                          f"2. Wyplac Srodki\n"
                          f"3. Stan Konta")
                    przelewy_input = input("wybierz akcje")
                    match przelewy_input:
                        case "1":
                            try:
                                aktualizacja.dodaj(int(input("Podaj Kwote")), konto)
                                print(f"Nowy Stan Konta:{konto.stan_konta}")
                            except ValueError:
                                print("Zła wartosc")
                        case "2":

                            try:
                                aktualizacja.usun(int(input("Podaj Kwote")), konto)
                                print(f"Nowy Stan Konta:{konto.stan_konta}")
                            except ValueError:
                                print("Zła wartosc")

                        case "3":
                            print(f"Stan Konta:{konto.stan_konta}")

                        case _:
                            print("nie ma takiej akcji")
                case "3":
                    print(f"1. Dane Karty\n"
                          f"2. Wygeneruj nowa karte")
                    karta_input = input("wybierz akcje")
                    match karta_input:
                        case "1":
                            karta.dane_karty()
                        case "2":
                            karta.generuj_nowa()
                        case _:
                            print("nie ma takiej akcji")
                case "5":
                    konto.is_run = False
                    konto.update_task()
                case "4":
                    print("1. Kurs PLN\n"
                          "2. Kursy wymian dowolnych walut\n"
                          "3. Wymien")


                    akcja = input("wybierz akcje")
                    api_key = "2ThjwETUVfKunPpRmtSWP6rP96qF2Q"

                    match akcja:

                        case "1":
                            def Kurs1():
                                waluta = input("podaj walute na ktora chcesz sprawdzic kurs np. USD,EUR,PKR")
                                r = requests.get(f"https://www.amdoren.com/api/currency.php?api_key={api_key}&from={waluta}&to=PLN&amount=1", )
                                data = r.json()
                                kurs = data["amount"]
                                if kurs == 0:
                                    print("Nie poprawna waluta")
                                else:
                                    print(f"Kurs 1 {waluta} to {kurs} PLN")

                            Kurs1()
                        case "2":
                            def Kurs2():
                                waluta = input("podaj pierwsza walute np. USD,EUR,PKR")
                                waluta2 = input("podaj druga walute np. USD,EUR,PKR")
                                r = requests.get(
                                    f"https://www.amdoren.com/api/currency.php?api_key={api_key}&from={waluta}&to={waluta2}&amount=1", )
                                data = r.json()
                                kurs = data["amount"]
                                if kurs == 0:
                                    print("Nie poprawna waluta")
                                else:
                                    print(f"Kurs 1 {waluta} to {kurs} {waluta2}")
                            Kurs2()

                        case "3":
                            def Kurs3():

                                conn = sqlite3.connect("klienci_db")
                                cursor = conn.cursor()
                                waluta2 = input("podaj druga walute np. USD,EUR,CAD")
                                ilosc = int(input("podaj ilosc PLN"))


                                try:

                                    getter = f"""SELECT {waluta2} FROM klienci WHERE id = {konto.id_konta}"""
                                    cursor.execute(getter)
                                    res = cursor.fetchall()
                                    print(res)
                                    if res[0][0] == None:
                                        res = 0
                                except sqlite3.OperationalError:
                                    res = 0

                                if ilosc > konto.stan_konta:
                                    print("nie wystarczajace srodki")
                                else:

                                    r = requests.get(
                                        f"https://www.amdoren.com/api/currency.php?api_key={api_key}&from=PLN&to={waluta2}&amount={ilosc}")
                                    data = r.json()
                                    kurs = float(data["amount"])
                                    print(kurs)
                                    if kurs == 0:
                                        print("Nie prawidlowa waluta")
                                    else:

                                        try:
                                            sql = f"""
                                            ALTER TABLE klienci ADD {waluta2} float
                                            """
                                            cursor.execute(sql)
                                            sql2 = f"""UPDATE klienci SET {waluta2} = {kurs} WHERE id={konto.id_konta}"""
                                            cursor.execute(sql2)
                                        except:
                                             if res == 0:
                                                sql2 = f"""UPDATE klienci SET {waluta2} = {kurs} WHERE id={konto.id_konta}"""
                                                cursor.execute(sql2)
                                             else:
                                                sql2 = f"""UPDATE klienci SET {waluta2} = {kurs + res[0][0]} WHERE id={konto.id_konta}"""
                                                cursor.execute(sql2)



                                        getter2 = f"""SELECT {waluta2} FROM klienci WHERE id = {konto.id_konta}"""
                                        cursor.execute(getter2)
                                        res = cursor.fetchall()
                                        print(f"Stan konta w {waluta2} wynosi {res[0][0]}")


                                        konto.stan_konta -= ilosc
                                        conn.commit()
                            Kurs3()

                case _:
                    print("nie ma takiej akcji")




    # Zapisywanie i logowanie
    try:
        cursor.execute(f"SELECT id FROM klienci WHERE Nazwisko=? AND Imie=?", (login2, login))
        res2 = cursor.fetchall()
        id_klienta = res2[0][0]

    except IndexError:
        try:
            cursor.execute(f"SELECT id FROM klienci")
            res3 = cursor.fetchall()
            id_value = res3[-1][0]
            id_klienta = int(id_value) + 1
        except IndexError:
            id_klienta = 1

    klient = Klient(login, login2, id_klienta)

    try:
        get_data = f"SELECT Stan_konta FROM klienci WHERE id={klient.id_konta}"
        cursor.execute(get_data)
        res = cursor.fetchall()
        saldo = res[0][0]

    except IndexError:
        saldo = 0

    konto = Konto(saldo, klient.imie, klient.nazwisko, klient.id_konta, "PLN")
    aktu = Aktualizacja(konto.stan_konta, konto.imie, konto.nazwisko, konto.id_konta, konto.waluta)
    karta = Karta(klient.imie, klient.nazwisko, klient.id_konta)
    menu = Menu
    Konto.Zapisanie_db(konto)

# Zapisywanie i logowanie


bank = app()
bank.konto.usun_z_db()





while bank.konto.is_run == True:
    bank.Menu.menu_logic(bank.menu, bank.konto, bank.aktu, bank.karta)

