from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup
import os

def extract_text(row, tag):
    element = BeautifulSoup(row, 'html.parser').find_all(tag)
    text = [col.get_text() for col in element]
    return text

def scrape_coronavirus_data():
    today_date = datetime.now().strftime('%Y-%m-%d')

    html = requests.get('https://www.worldometers.info/coronavirus/').text
    print('Загрузка данных Worldometer')
    html_soup = BeautifulSoup(html, 'html.parser')
    rows = html_soup.find_all('tr')

    heading = rows.pop(0)
    heading_row = extract_text(str(heading), 'th')[1:9]

    # Проверка наличия файла
    file_exists = os.path.exists('corona_latest.csv')

    with open('corona_latest.csv', 'a', encoding='utf-8', newline='') as store:
        Store = csv.writer(store, delimiter=',')

        # Если файл не существует, записываем заголовок
        if not file_exists:
            heading_row.append('Date')  # Добавляем новую колонку 'Date' в заголовок
            Store.writerow(heading_row)

        for row in rows:
            test_data = extract_text(str(row), 'td')[1:9]
            test_data.append(today_date)  # Добавляем сегодняшнюю дату в данные
            Store.writerow(test_data)

    print('Загрузка данных Worldometer завершена')

def load_coronavirus_data(file_name='corona_latest.csv'):
    data_new = pd.read_csv(file_name)
    print('Данные о коронавирусе загружены успешно')
    return data_new

def load_vaccination_data():
    url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
    data = pd.read_csv(url)
    vaccination_data = data.loc[:, ['date', 'location', 'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated', 'total_boosters']]
    print('Данные о вакцинации загружены успешно')
    return vaccination_data

# Вызов функций
scrape_coronavirus_data()
coronavirus_data = load_coronavirus_data()
vaccination_data = load_vaccination_data()

# Вывод данных для проверки
print(coronavirus_data.head())
print(vaccination_data.head())