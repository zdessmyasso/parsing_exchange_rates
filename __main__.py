
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import sqlite3

table_name = 'exchange_rates'
scheme_name = 'currency.db'


# функция для создания схемы и таблицы в sqlite
def create_table():
    con = sqlite3.connect(scheme_name)
    con.execute(f"""
               CREATE TABLE IF NOT EXISTS {table_name}(
               date_currency text,
               numcode integer,
               charcode text,
               nominal integer,
               name text,
               value text)
               """
                )
    con.commit()


# функция для добавления значений в таблицу за указанную дату
def load_values(date):
    date = datetime.strptime(date, '%Y-%m-%d').strftime("%d/%m/%Y")
    URL = f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}"

    req = requests.get(URL)
    soup = BeautifulSoup(req.content, features="lxml")

    list_line = []
    for item in soup.find_all('valute'):
        list_line.append((soup.find('valcurs').attrs['date'],
                          item.find('numcode').text,
                          item.find('charcode').text,
                          item.find('nominal').text,
                          item.find('name').text,
                          item.find('value').text))

    con = sqlite3.connect(scheme_name)

    for item in list_line:
        con.execute(f"INSERT INTO {table_name} VALUES {item}")

        con.commit()

    table = con.execute(f"SELECT * FROM {table_name}")
    for row in table:
        print(row)

    return print('данные загружены')


# Функция для удаления записей по числовому коду валюты
def delete_currency(numcode):
    con = sqlite3.connect(scheme_name)

    con.execute(f"DELETE FROM {table_name} WHERE numcode IN ({numcode})")

    con.commit()

    table = con.execute(f"SELECT * FROM {table_name}")

    for row in table:
        print(row)


# функция для вывода уникальных значений кодов валюты (числовое + буквенное)
def unique_currency():
    con = sqlite3.connect(f"{scheme_name}")

    distinct_numcode = con.execute(f"SELECT DISTINCT numcode, charcode FROM {table_name}")

    con.commit()

    for row in distinct_numcode:
        print(row)


# функция вывода таблицы
def show_table():
    con = sqlite3.connect(f"{scheme_name}")

    table_currency = con.execute(f"SELECT * FROM {table_name}")

    for row in table_currency:
        print(row)


def menu():
    create_table()
    loop = True
    while loop == True:
        print('____________________________________________________')
        print('----------------------М Е Н Ю ----------------------')
        print('____________________________________________________')
        print('\n')
        print('возможные действия:')
        print('[1]-- загрузить курсы валют за указанную дату'),
        print('[2]-- удалить курсы валют по числовому коду'),
        print('[3]-- вывести уникальные коды валют '),
        print('[4]-- вывести таблицу')
        print('[5]-- завершить ')

        option = int(input('выберете действие:'))

        if option == 1:
            print('введите дату в формате YYYY-MM-DD:'),
            print(load_values(input()))

        elif option == 2:
            print('введите числовой код валюты:'),
            print(delete_currency(input()))

        elif option == 3:
            print(unique_currency())

        elif option == 4:
            print(show_table())

        elif option == 5:
            loop = False

        else:
            print('no such function exists')

menu()