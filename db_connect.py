import datetime
import sqlite3
import sending_messages_to_tg
from uuid import uuid4
import time



currentDateTime = datetime.datetime.now()
#conn = sqlite3.connect('flats.db')
#cur = conn.cursor()

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

    cur.execute("""CREATE TABLE IF NOT EXISTS filters(
        filter_id TEXT PRIMARY KEY,
        city TEXT,
        price TEXT,
        room TEXT,
        date TIMESTAMP,
        status BOOL);
        """)


def check_id_flat(id, cur):
    id_flat = id[0]
    cur.execute(f"SELECT flat_id FROM flats WHERE flat_id = {id_flat};")
    return cur.fetchall()


def insert_flat_to_db(cur, list_of_list):
    for i in list_of_list:
        all_result = check_id_flat(i, cur)
        if all_result:
            print('Есть такая квартира в базе')
        else:
            print('Нет такой квартиры, давай добавим!')
            sending_messages_to_tg.send_telegram(i[4])
            time.sleep(3)  # Сон в 3 секунды, чтобы телега не ругалась
            cur.execute("INSERT INTO flats VALUES(?, ?, ?, ?, ?, ?, ?);", i)


def insert_filter_to_db(cur, filters: dict):
    #должен быть коннект к базе!!!
    flag = False
    for i in filters.values():
        if i != '':
            flag = True
            break
        else:
            continue
    if flag:
        data_tuple = (str(uuid4()), filters['city'], filters['price'], filters['room'], currentDateTime, False)
        cur.execute("UPDATE filters set status = 1 where status = 0;")
        cur.execute("INSERT INTO filters VALUES(?, ?, ?, ?, ?, ?);", data_tuple)


def get_url(cur):
    city = {'г. Астана': 'astana','г. Алма-Аты': 'almaty'}
    price = {'до 150000 〒': '150000', 'до 200000 〒': '200000', 'до 250000 〒': '250000',
             'до 300000 〒': '300000', 'до 350000 〒': '350000', 'до 400000 〒': '400000',
             'до 450000 〒': '450000'}
    room = {'1': '1', '2': '2', '3': '3'}

    cur.execute(f"SELECT city, price, room FROM filters WHERE status = 0;")
    current_filters = cur.fetchone()

    base_url = 'https://krisha.kz/arenda/kvartiry/?das[_sys.hasphoto]=1&das[live.furniture][]=1&' \
               'das[live.furniture][]=2&das[rent.period]=2'

    new_url = ''

    if current_filters[0]:
        new_url = f'https://krisha.kz/arenda/kvartiry/{city[current_filters[0]]}/?das[_sys.hasphoto]=1&das[live.furniture][]=1&' \
                'das[live.furniture][]=2&das[rent.period]=2'
    else:
        new_url = base_url
    if current_filters[1]:
        new_url += f'&das[price][to]={price[current_filters[1]]}'
    if current_filters[2]:
        new_url += f'&das[live.rooms]={room[current_filters[2]]}'
    new_url += '&page=0'

    return new_url

