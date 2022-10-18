import telebot
import sqlite3


bot = telebot.TeleBot('5424286381:AAEC9ZJ4TNiFiqSEJ4Sa56hCPpDhLfzeOVY')

'''
def db_connect():
    conn = sqlite3.connect('flats.db')
    cur = conn.cursor()
    cur.execute("SELECT link FROM flats WHERE status = 0;")
    one_result = cur.fetchall()
    conn.commit()
    return one_result
'''

@bot.message_handler(content_types=['text'])

def get_text_messages(message):
    conn = sqlite3.connect('flats.db')
    cur = conn.cursor()
    cur.execute("SELECT link FROM flats WHERE status = 0;")
    new_flats = cur.fetchall()
    conn.commit()

    if message.text == "Покажи свежие квартивы":
        if new_flats:
            for i in new_flats:
                bot.send_message(message.from_user.id, i)
        else:
            bot.send_message(message.from_user.id, "Нет новых квартир, прости((")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Покажи свежие квартиры")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

bot.polling(none_stop=True, interval=0)