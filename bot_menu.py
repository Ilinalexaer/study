import telebot
from telebot import types  # для указание типов
import sqlite3
import db_connect
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
bot = telebot.TeleBot(os.getenv('TOKEN'))
#bot = telebot.TeleBot("5621991944:AAEsK1mLa_93MJgIR1_pWy4m9eFHf7EpAz0")

filters = {'city': '', 'price': '', 'room': ''}

def menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Город")
    btn2 = types.KeyboardButton("Стоимость")
    btn3 = types.KeyboardButton("Комнаты")
    btn4 = types.KeyboardButton("Сохранить")
    btn5 = types.KeyboardButton("Показать текущие")
    back = types.KeyboardButton("Главное меню")
    markup.add(btn1, btn2, btn3, btn4, btn5).add(back)
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🥳 Ссылка на krishka.kz")
    btn2 = types.KeyboardButton("🔐 Фильтры")
    markup.add(btn1).add(btn2)
    bot.send_message(message.chat.id, text="Привет! Меня зовут krishka.kz_bot. "
                                           "Я помогу настроить подбор квартив для канала krishka.kz", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    conn = sqlite3.connect('flats.db')
    cur = conn.cursor()

    if message.text == "🥳 Ссылка на krishka.kz":
        bot.send_message(message.chat.id, text="https://t.me/+O0AAxylCHno0ZGEy")

    elif message.text == "🔐 Фильтры":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Главное меню")
        markup.add(back)
        bot.send_message(message.chat.id, text="Введите пароль", reply_markup=markup)

    elif (message.text == "123") or (message.text == "Назад"):
        bot.send_message(message.chat.id, text="Молодец!!!", reply_markup=menu())

    elif message.text == "Город":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("г. Астана")
        btn2 = types.KeyboardButton("г. Алма-Аты")
        back = types.KeyboardButton("Назад")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="В каком городе ты хочешь искать квартиру?", reply_markup=markup)

    elif (message.text == "г. Астана") or (message.text == "г. Алма-Аты"):
        filters['city'] = message.text
        bot.send_message(message.chat.id, text=f"выбран {filters['city']}", reply_markup=menu())

    elif message.text == "Стоимость":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("до 200000 〒")
        btn2 = types.KeyboardButton("до 250000 〒")
        btn3 = types.KeyboardButton("до 300000 〒")
        btn4 = types.KeyboardButton("до 350000 〒")
        btn5 = types.KeyboardButton("до 400000 〒")
        btn6 = types.KeyboardButton("до 450000 〒")
        btn7 = types.KeyboardButton("до 500000 〒")
        back = types.KeyboardButton("Назад")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, back)
        bot.send_message(message.chat.id, text="Сколько денег ты готов заплатить?", reply_markup=markup)

    elif (message.text == "до 200000 〒") or (message.text == "до 250000 〒") \
            or (message.text == "до 300000 〒") or (message.text == "до 350000 〒") \
            or (message.text == "до 400000 〒") or (message.text == "до 450000 〒")\
            or (message.text == "до 500000 〒"):
        filters['price'] = message.text
        bot.send_message(message.chat.id, text=f"Ты готов отдать {filters['price']}, богач)", reply_markup=menu())

    elif message.text == "Комнаты":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("1")
        btn2 = types.KeyboardButton("2")
        btn3 = types.KeyboardButton("3")
        back = types.KeyboardButton("Назад")
        markup.add(btn1, btn2, btn3, back)
        bot.send_message(message.chat.id, text="Сколько комнат тебе нужно?", reply_markup=markup)

    elif (message.text == "1") or (message.text == "2") or (message.text == "3"):
        filters['room'] = message.text
        bot.send_message(message.chat.id, text=f"Нужно {filters['room']} комнат(ы)", reply_markup=menu())

    elif message.text == "Показать текущие":
        cur.execute(f"SELECT city, price, room FROM filters WHERE status = 0;")
        current_filters = cur.fetchone()
        bot.send_message(message.chat.id, text=f"Текущие фильтры: Город - {current_filters[0]}, "
                                               f"Цена - {current_filters[1]}, "
                                               f"Количество комнат - {current_filters[2]}")

    elif message.text == "Сохранить":
        flag = False
        for i in filters.values():
            if i != '':
                flag = True
                break
            else:
                continue
        if flag == True:
            bot.send_message(message.chat.id, text=f"Сохранено {filters.values()}", reply_markup=menu())
            #записываем новые фильтры в БД
            db_connect.insert_filter_to_db(cur, filters)

        else:
            bot.send_message(message.chat.id, text=f"Фильры не выбраны {filters.values()}", reply_markup=menu())

    elif message.text == "Главное меню":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("🥳 Ссылка на krishka.kz")
        btn2 = types.KeyboardButton("🔐 Фильтры")
        markup.add(btn1).add(btn2)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)

    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал...")
    conn.commit()

bot.polling(none_stop=True, interval=0)