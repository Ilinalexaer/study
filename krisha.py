import requests
import re
from bs4 import BeautifulSoup
import datetime
from functools import reduce
import sqlite3
import sending_messages_to_tg

currentDateTime = datetime.datetime.now()

url = 'https://krisha.kz/arenda/kvartiry/astana/?das[_sys.hasphoto]=1&' \
      'das[live.furniture][0]=1&das[live.furniture][1]=2&das[live.rooms]=2&' \
      'das[price][to]=400000&das[rent.period]=2&das[who]=1&page=0'

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


def create_db(cur):
    cur.execute("""CREATE TABLE IF NOT EXISTS flats(
        flat_id INT PRIMARY KEY,
        discription TEXT,
        money TEXT,
        date_of_post TEXT,
        link TEXT,
        date TIMESTAMP,
        status BOOL);
        """)


def check_id_flat(id, cur):
    id_flat = id[0]
    cur.execute(f"SELECT flat_id FROM flats WHERE flat_id = {id_flat};")
    return cur.fetchall()


def insert_flat_to_db(cur, list_of_list):
    for i in list_of_list:
        #heck_id_flat(i, cur)
        # cur.execute(f"SELECT flat_id FROM flats WHERE flat_id = {i[0]};")
        # all_result = cur.fetchall()
        all_result = check_id_flat(i, cur)
        if all_result:
            print('Есть такая квартира в базе')
        else:
            print('Нет такой квартиры, давай добавим!')
            sending_messages_to_tg.send_telegram(i[4])
            cur.execute("INSERT INTO flats VALUES(?, ?, ?, ?, ?, ?, ?);", i)

if __name__ == '__main__':
    list_of_list = parser(url)

    if list_of_list:
        conn = sqlite3.connect('flats.db')
        cur = conn.cursor()

        create_db(cur)
        insert_flat_to_db(cur, list_of_list)

        conn.commit()

