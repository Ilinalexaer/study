import requests
import re
from bs4 import BeautifulSoup
import datetime
from functools import reduce
import sqlite3
import sending_messages_to_tg
from uuid import uuid4
import db_connect

currentDateTime = datetime.datetime.now()

def parser(url):
    page_list = []
    id_list = []
    for j in range(0, 2):
        newUrl = url.replace(f'page={j}', f'page={j+1}')
        response = requests.get(newUrl)
        soup = BeautifulSoup(response.text, 'lxml')

        cards = soup.find_all('a', class_='a-card__title')
        prices = soup.find_all('div', class_='a-card__price')
        dates = soup.find_all('div', class_='card-stats__item', text=re.compile(r'[0-9]'))
        links = soup.find_all(href=re.compile("a/show"), class_='a-card__title')
        #data_id = soup.find_all('div', class_='a-card a-storage-live ddl_product ddl_product_link is-colored paid-color-light-red is-visible')
        #views = soup.find_all('div', class_='card-stats__item', title="Количество просмотров")

        for i in range(0, len(cards)):
            if links and prices and dates:
                page_list.append([int(str(links[i].get('href'))[8:]),
                                  links[i].text,
                                  reduce(lambda x, y: x + y, re.findall('\d+', prices[i].text.strip()))+'〒',
                                  dates[i].text.strip(),
                                  'https://krisha.kz'+links[i].get('href'),
                                  currentDateTime,
                                  True])
    return page_list

if __name__ == '__main__':
    conn = sqlite3.connect('flats.db')
    cur = conn.cursor()
    #Получаем значения фильтров из БД
    url = db_connect.get_url(cur)
    list_of_list = parser(url)

    if list_of_list:
        #Создаем БД, если ее нет
        db_connect.create_db(cur)
        #Сохраняем объявления в БД
        db_connect.insert_flat_to_db(cur, list_of_list)

    conn.commit()

