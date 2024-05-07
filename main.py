import random
import sqlite3
from abc import ABC, abstractmethod
import requests
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton,QFormLayout
from PyQt5 import *
from  PyQt5 import QtCore , QtWidgets
from PyQt5.QtGui import QFont


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

    class Kantor:
        def __init__(self):
            self.wynik = None




        def Kurs11(self, api_key, waluta):
            self.wynik = None
            r = requests.get(
                f"https://www.amdoren.com/api/currency.php?api_key={api_key}&from={waluta}&to=PLN&amount=1", )
            data = r.json()
            kurs = data["amount"]
            if kurs == 0:
                print("Nie poprawna waluta")
                self.wynik = "Nie poprawna waluta"
            else:
                print(f"Kurs 1 {waluta} to {kurs} PLN")
                self.wynik = f"Kurs 1 {waluta} to {kurs} PLN"





        def Kurs22(self, api_key, waluta, waluta2):
            self.wynik = None
            r = requests.get(
                f"https://www.amdoren.com/api/currency.php?api_key={api_key}&from={waluta}&to={waluta2}&amount=1", )
            data = r.json()
            kurs = data["amount"]
            if kurs == 0:
                print("Nie poprawna waluta")
                self.wynik = "Nie poprawna waluta"
            else:
                print(f"Kurs 1 {waluta} to {kurs} {waluta2}")
                self.wynik = f"Kurs 1 {waluta} to {kurs} {waluta2}"




        def Kurs33(self, konto, api_key, waluta2, ilosc):

            conn = sqlite3.connect("klienci_db")
            cursor = conn.cursor()

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
                self.wynik = "nie wystarczajace srodki"
            else:

                r = requests.get(
                    f"https://www.amdoren.com/api/currency.php?api_key={api_key}&from=PLN&to={waluta2}&amount={ilosc}")
                data = r.json()
                kurs = float(data["amount"])
                print(kurs)
                if kurs == 0:
                    print("Nie prawidlowa waluta")
                    self.wynik = "Nie prawidlowa waluta"
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
                    self.wynik = f"Stan konta w {waluta2} wynosi {res[0][0]}"
                    konto.stan_konta -= ilosc
                    conn.commit()

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
    kantor = Kantor()
    #menu = Menu()
    Konto.Zapisanie_db(konto)




# Zapisywanie i logowanie


bank = app()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        serifFont = QFont("Times", 25, QFont.Bold)

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(734, 600)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, -50, 101, 1151))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_buttons = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_buttons.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_buttons.setSpacing(0)
        self.verticalLayout_buttons.setObjectName("verticalLayout_buttons")
        spacerItem = QtWidgets.QSpacerItem(20, 80, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_buttons.addItem(spacerItem)

        self.pushButton_Main = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_Main.setStyleSheet("color: rgb(255, 255, 255);")
        self.pushButton_Main.setObjectName("pushButton_Main")
        self.pushButton_Main.clicked.connect(self.okno_stona_glowna)

        self.verticalLayout_buttons.addWidget(self.pushButton_Main)

        self.pushButton_Przelewy = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_Przelewy.setStyleSheet("color: rgb(255, 255, 255);")
        self.pushButton_Przelewy.setObjectName("pushButton_Przelewy")
        self.pushButton_Przelewy.clicked.connect(self.okno_przelewy)


        self.verticalLayout_buttons.addWidget(self.pushButton_Przelewy)

        self.pushButton_Kantor = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_Kantor.setStyleSheet("color: rgb(255, 255, 255);")
        self.pushButton_Kantor.setObjectName("pushButton_Kantor")
        self.pushButton_Kantor.clicked.connect(self.okno_kantor)



        self.verticalLayout_buttons.addWidget(self.pushButton_Kantor)

        self.pushButton_Karta = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_Karta.setStyleSheet("color: rgb(255, 255, 255);")
        self.pushButton_Karta.setObjectName("pushButton_Karta")
        self.pushButton_Karta.clicked.connect(self.okno_karta)

        self.verticalLayout_buttons.addWidget(self.pushButton_Karta)

        self.pushButton_Zakoncz = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_Zakoncz.setStyleSheet("color: rgb(0, 0, 0);")
        self.pushButton_Zakoncz.setObjectName("pushButton_Zakoncz")

        self.verticalLayout_buttons.addWidget(self.pushButton_Zakoncz)

        spacerItem1 = QtWidgets.QSpacerItem(20, 800, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_buttons.addItem(spacerItem1)
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(99, 59, 701, 541))
        self.stackedWidget.setStyleSheet("background-color: rgb(81, 81, 81);")
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_main = QtWidgets.QWidget()
        self.page_main.setObjectName("page_main")
        self.label = QtWidgets.QLabel(self.page_main)
        self.label.setGeometry(QtCore.QRect(30, 40, 151, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.page_main)
        self.label_2.setGeometry(QtCore.QRect(240, 40, 200, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.page_main)
        self.label_3.setGeometry(QtCore.QRect(380, 100, 151, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.page_main)
        self.label_4.setGeometry(QtCore.QRect(560, 100, 70, 31))
        self.label_4.setObjectName("label_4")
        self.stackedWidget.addWidget(self.page_main)
        self.page_kantor = QtWidgets.QWidget()
        self.page_kantor.setObjectName("page_kantor")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.page_kantor)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(20, 10, 601, 61))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.pushButton_6 = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(self.kantor_kurs_pln)
        self.horizontalLayout_2.addWidget(self.pushButton_6)


        self.pushButton_7 = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.clicked.connect(self.kantor_kurs_walut)
        self.horizontalLayout_2.addWidget(self.pushButton_7)

        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.kantor_wymiana)


        self.horizontalLayout_2.addWidget(self.pushButton)
        self.stackedWidget_2 = QtWidgets.QStackedWidget(self.page_kantor)
        self.stackedWidget_2.setGeometry(QtCore.QRect(29, 99, 591, 421))
        self.stackedWidget_2.setObjectName("stackedWidget_2")
        self.page_kurs_pln = QtWidgets.QWidget()
        self.page_kurs_pln.setObjectName("page_kurs_pln")
        self.label_kurs_1_pln = QtWidgets.QLabel(self.page_kurs_pln)
        self.label_kurs_1_pln.setGeometry(QtCore.QRect(0, 190, 571, 91))
        self.label_kurs_1_pln.setObjectName("label_kurs_1_pln")

        self.lineEdit = QtWidgets.QLineEdit(self.page_kurs_pln)
        self.lineEdit.setGeometry(QtCore.QRect(50, 40, 461, 61))
        self.lineEdit.setObjectName("lineEdit")

        self.label_waluta_text = QtWidgets.QLabel(self.page_kurs_pln)
        self.label_waluta_text.setGeometry(QtCore.QRect(160, 0, 221, 31))
        self.label_waluta_text.setAlignment(QtCore.Qt.AlignCenter)
        self.label_waluta_text.setObjectName("label_waluta_text")

        self.pushButton_przelicz = QtWidgets.QPushButton(self.page_kurs_pln)
        self.pushButton_przelicz.setGeometry(QtCore.QRect(230, 130, 75, 23))
        self.pushButton_przelicz.setObjectName("pushButton_przelicz")
        self.pushButton_przelicz.clicked.connect(self.kantor_kurs_pln_logic)
        self.stackedWidget_2.addWidget(self.page_kurs_pln)

        self.page_kurs_walut = QtWidgets.QWidget()
        self.page_kurs_walut.setObjectName("page_kurs_walut")

        self.label_kurs_walut = QtWidgets.QLabel(self.page_kurs_walut)
        self.label_kurs_walut.setGeometry(QtCore.QRect(10, 200, 591, 111))
        self.label_kurs_walut.setObjectName("label_kurs_walut")

        self.lineEdit_pierwsza_waluta = QtWidgets.QLineEdit(self.page_kurs_walut)
        self.lineEdit_pierwsza_waluta.setGeometry(QtCore.QRect(120, 40, 141, 31))
        self.lineEdit_pierwsza_waluta.setObjectName("lineEdit_pierwsza_waluta")

        self.lineEdit_druga_waluta = QtWidgets.QLineEdit(self.page_kurs_walut)
        self.lineEdit_druga_waluta.setGeometry(QtCore.QRect(290, 40, 141, 31))
        self.lineEdit_druga_waluta.setObjectName("lineEdit_druga_waluta")

        self.label_5 = QtWidgets.QLabel(self.page_kurs_walut)
        self.label_5.setGeometry(QtCore.QRect(120, 20, 141, 20))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.page_kurs_walut)
        self.label_6.setGeometry(QtCore.QRect(290, 20, 141, 16))
        self.label_6.setObjectName("label_6")

        self.pushButton_Przelicz2 = QtWidgets.QPushButton(self.page_kurs_walut)
        self.pushButton_Przelicz2.setGeometry(QtCore.QRect(240, 120, 75, 23))
        self.pushButton_Przelicz2.setObjectName("pushButton_Przelicz2")
        self.pushButton_Przelicz2.clicked.connect(self.kantor_kurs_dwoch_walut_logic)

        self.stackedWidget_2.addWidget(self.page_kurs_walut)
        self.page_wymien = QtWidgets.QWidget()
        self.page_wymien.setObjectName("page_wymien")

        self.lineEdit_ilosc = QtWidgets.QLineEdit(self.page_wymien)
        self.lineEdit_ilosc.setGeometry(QtCore.QRect(190, 40, 201, 41))
        self.lineEdit_ilosc.setObjectName("lineEdit_ilosc")

        self.lineEdit_waluta = QtWidgets.QLineEdit(self.page_wymien)
        self.lineEdit_waluta.setGeometry(QtCore.QRect(190, 110, 201, 41))
        self.lineEdit_waluta.setObjectName("lineEdit_waluta")

        self.label_7 = QtWidgets.QLabel(self.page_wymien)
        self.label_7.setGeometry(QtCore.QRect(190, 20, 201, 16))
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")

        self.label_8 = QtWidgets.QLabel(self.page_wymien)
        self.label_8.setGeometry(QtCore.QRect(190, 80, 201, 31))
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")

        self.pushButton_Wymien = QtWidgets.QPushButton(self.page_wymien)
        self.pushButton_Wymien.setGeometry(QtCore.QRect(194, 182, 201, 41))
        self.pushButton_Wymien.setObjectName("pushButton_Wymien")

        self.label_status_wymiany = QtWidgets.QLabel(self.page_wymien)
        self.label_status_wymiany.setGeometry(QtCore.QRect(10, 280, 591, 101))
        self.label_status_wymiany.setObjectName("label_status_wymiany")

        self.stackedWidget_2.addWidget(self.page_wymien)
        self.stackedWidget.addWidget(self.page_kantor)

        self.page_przelewy = QtWidgets.QWidget()
        self.page_przelewy.setObjectName("page_przelewy")

        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.page_przelewy)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(29, 30, 581, 501))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(20, 120, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem2)
        self.lineEdit_kwota = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_kwota.sizePolicy().hasHeightForWidth())

        self.lineEdit_2 = QtWidgets.QLineEdit(self.page_main)
        self.lineEdit_2.setGeometry(QtCore.QRect(10, 380, 321, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.label_API_KEY = QtWidgets.QLabel(self.page_main)
        self.label_API_KEY.setGeometry(QtCore.QRect(20, 353, 71, 20))
        self.label_API_KEY.setObjectName("label_API_KEY")



        #Przelewy
        self.lineEdit_kwota.setSizePolicy(sizePolicy)
        self.lineEdit_kwota.setMinimumSize(QtCore.QSize(555, 0))
        self.lineEdit_kwota.setSizeIncrement(QtCore.QSize(0, 0))
        self.lineEdit_kwota.setBaseSize(QtCore.QSize(0, 0))
        self.lineEdit_kwota.setObjectName("lineEdit_kwota")

        self.verticalLayout.addWidget(self.lineEdit_kwota)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.pushButton_Dodaj = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_Dodaj.setObjectName("pushButton_Dodaj")
        self.pushButton_Dodaj.clicked.connect(self.przelewy_dodaj)


        self.horizontalLayout.addWidget(self.pushButton_Dodaj)

        self.pushButton_odejmij = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_odejmij.setObjectName("pushButton_odejmij")
        self.pushButton_odejmij.clicked.connect(self.przelewy_odejmij)


        self.horizontalLayout.addWidget(self.pushButton_odejmij)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.stackedWidget.addWidget(self.page_przelewy)
        #Karta
        self.page_karta = QtWidgets.QWidget()
        self.page_karta.setObjectName("page_karta")

        self.label_Imie = QtWidgets.QLabel(self.page_karta)
        self.label_Imie.setGeometry(QtCore.QRect(20, 290, 161, 31))
        self.label_Imie.setObjectName("label_Imie")

        self.label_Nazwisko = QtWidgets.QLabel(self.page_karta)
        self.label_Nazwisko.setGeometry(QtCore.QRect(210, 290, 190, 31))
        self.label_Nazwisko.setObjectName("label_Nazwisko")

        self.label_numer = QtWidgets.QLabel(self.page_karta)
        self.label_numer.setGeometry(QtCore.QRect(20, 350, 351, 31))
        self.label_numer.setObjectName("label_numer")

        self.label_data = QtWidgets.QLabel(self.page_karta)
        self.label_data.setGeometry(QtCore.QRect(20, 410, 161, 31))
        self.label_data.setObjectName("label_data")

        self.label_Cvv = QtWidgets.QLabel(self.page_karta)
        self.label_Cvv.setGeometry(QtCore.QRect(210, 410, 161, 31))
        self.label_Cvv.setObjectName("label_Cvv")

        self.pushButton_wyswietl = QtWidgets.QPushButton(self.page_karta)
        self.pushButton_wyswietl.setGeometry(QtCore.QRect(20, 80, 131, 51))
        self.pushButton_wyswietl.setObjectName("pushButton_wyswietl")

        self.pushButton_Generuj = QtWidgets.QPushButton(self.page_karta)
        self.pushButton_Generuj.setGeometry(QtCore.QRect(20, 40, 131, 23))
        self.pushButton_Generuj.setObjectName("pushButton_Generuj")
        self.pushButton_Generuj.clicked.connect(self.generuj_nowa_karte)

        self.stackedWidget.addWidget(self.page_karta)
        MainWindow.setCentralWidget(self.centralwidget)

        self.label.setFont(serifFont)
        self.label_2.setFont(serifFont)
        self.label_3.setFont(serifFont)
        self.label_4.setFont(serifFont)




        self.label_numer.setFont(serifFont)
        self.label_data.setFont(serifFont)
        self.label_Imie.setFont(serifFont)
        self.label_Nazwisko.setFont(serifFont)
        self.label_Cvv.setFont(serifFont)

        self.pushButton_Wymien.clicked.connect(self.kantor_wymiana_logic)

        self.label_kurs_1_pln.setFont(serifFont)
        self.label_kurs_walut.setFont(serifFont)
        self.label_status_wymiany.setFont(serifFont)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def main(self,konto):
        self.label.setText(konto.imie)
        self.label_2.setText(konto.nazwisko)
        self.label_3.setText(str(konto.stan_konta))
        self.label_4.setText(konto.waluta)

    def przelewy_dodaj(self):
        bank.aktu.dodaj(int(self.lineEdit_kwota.text()),bank.konto)
        bank.konto.update_task()

    def przelewy_odejmij(self):
        bank.aktu.usun(int(self.lineEdit_kwota.text()),bank.konto)
        bank.konto.update_task()

    def generuj_nowa_karte(self):
        bank.karta.generuj_nowa()
        self.label_Imie.setText(bank.karta.imie)
        self.label_Cvv.setText(bank.karta.pin)
        self.label_data.setText(bank.karta.data_waz)
        self.label_Nazwisko.setText(bank.karta.nazwisko)
        self.label_numer.setText(bank.karta.numer_karty)

    def kantor_kurs_pln_logic(self):
        bank.kantor.Kurs11(self.lineEdit_2.text(),self.lineEdit.text())
        self.label_kurs_1_pln.setText(bank.kantor.wynik)

    def kantor_kurs_dwoch_walut_logic(self):
        bank.kantor.Kurs22(self.lineEdit_2.text(),self.lineEdit_pierwsza_waluta.text(),self.lineEdit_druga_waluta.text())
        self.label_kurs_walut.setText(bank.kantor.wynik)




    def kantor_wymiana_logic(self):
        bank.kantor.Kurs33(bank.konto,self.lineEdit_2.text(),self.lineEdit_waluta.text(),int(self.lineEdit_ilosc.text()))
        self.label_status_wymiany.setText(bank.kantor.wynik)
        bank.konto.update_task()




#Strony
    def okno_stona_glowna(self):
        self.stackedWidget.setCurrentIndex(0)
        self.main(bank.konto)

    def okno_przelewy(self):
        self.stackedWidget.setCurrentIndex(2)

    def okno_kantor(self):
        self.stackedWidget.setCurrentIndex(1)
    def okno_karta(self):
        self.stackedWidget.setCurrentIndex(3)

    def kantor_kurs_pln(self):
        self.stackedWidget_2.setCurrentIndex(0)

    def kantor_wymiana(self):
        self.stackedWidget_2.setCurrentIndex(2)

    def kantor_kurs_walut(self):
        self.stackedWidget_2.setCurrentIndex(1)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_Main.setText(_translate("MainWindow", "Strona Glowna"))
        self.pushButton_Przelewy.setText(_translate("MainWindow", "Przelewy"))
        self.pushButton_Kantor.setText(_translate("MainWindow", "Kantor"))
        self.pushButton_Karta.setText(_translate("MainWindow", "Karta"))
        self.pushButton_Zakoncz.setText(_translate("MainWindow", "Zakoncz"))
        self.label.setText(_translate("MainWindow", "1"))
        self.label_2.setText(_translate("MainWindow", "2"))
        self.label_3.setText(_translate("MainWindow", "3"))
        self.label_4.setText(_translate("MainWindow", "4"))
        self.pushButton_6.setText(_translate("MainWindow", "Kurs PLN"))
        self.pushButton_7.setText(_translate("MainWindow", "Kurs Walut"))
        self.pushButton.setText(_translate("MainWindow", "Wymiana"))
        self.label_kurs_1_pln.setText(_translate("MainWindow", "N/A"))
        self.label_waluta_text.setText(_translate("MainWindow", "Waluta"))
        self.pushButton_przelicz.setText(_translate("MainWindow", "Przelicz"))
        self.label_kurs_walut.setText(_translate("MainWindow", "N/A"))
        self.label_5.setText(_translate("MainWindow", "Pierwsza Waluta"))
        self.label_6.setText(_translate("MainWindow", "Druga Waluta"))
        self.pushButton_Przelicz2.setText(_translate("MainWindow", "Przelicz"))
        self.label_7.setText(_translate("MainWindow", "Ilosc PLN"))
        self.label_8.setText(_translate("MainWindow", "Waluta"))
        self.pushButton_Wymien.setText(_translate("MainWindow", "Wymien"))
        self.label_status_wymiany.setText(_translate("MainWindow", "N/A"))
        self.pushButton_Dodaj.setText(_translate("MainWindow", "Dodaj"))
        self.pushButton_odejmij.setText(_translate("MainWindow", "Odejmij"))
        self.label_Imie.setText(_translate("MainWindow", "N/A"))
        self.label_Nazwisko.setText(_translate("MainWindow", "N/A"))
        self.label_numer.setText(_translate("MainWindow", "N/A"))
        self.label_data.setText(_translate("MainWindow", "N/A"))
        self.label_Cvv.setText(_translate("MainWindow", "N/A"))
        self.pushButton_wyswietl.setText(_translate("MainWindow", "Wyswietl info"))
        self.pushButton_Generuj.setText(_translate("MainWindow", "Generuj nowa"))
        self.label_API_KEY.setText(_translate("MainWindow", "API Key"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.main(bank.konto)



    MainWindow.show()
    sys.exit(app.exec_())

# while bank.konto.is_run == True:
#   bank.Menu.menu_logic(bank.menu, bank.konto, bank.aktu, bank.karta)
#  bank.Menu.init_ui(bank.menu,bank.konto,bank.aktu,bank.karta)
