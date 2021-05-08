import telebot
from telebot import types

# Наша БД
import sqlite3 as sqlite 

# Забираем данные из config'a
from config import TOKEN, ADMIN_ID
from messages import START_MSG, CFG_MSG, REVIEWS_MSG, FQA_MSG

# Для рулетки
from random import *
import time
from datetime import datetime

# Создаем нашего бота
bot = telebot.TeleBot(TOKEN)

def start(message):

    db = sqlite.connect("base.db")
    cur = db.cursor()

    for i in cur.execute(f"SELECT * FROM users WHERE id = {message.from_user.id}"):

        if time.time() > int(i[2]):

            rn1 = randint(1, 1000)
            reloading_time = 129600 * 2

            try:

                new_time = float(time.time()) + reloading_time

                cur.execute(f"UPDATE users SET r_time = {new_time} WHERE id = {message.from_user.id}")

                if rn1 <= 100:

                    rn2 = randint(1, 1000)

                    if rn2 < rn1:

                        for x in cur.execute(f"SELECT * FROM rulletka"):

                            price = str(x[1])
                            link = str(x[2])

                            markup = types.InlineKeyboardMarkup(row_width=1)

                            item1 = types.InlineKeyboardButton("Получить", url=link)
                            item2 = types.InlineKeyboardButton("Закрыть", callback_data="close")
                            
                            markup.add(
                                item1,
                                item2
                            )


                            bot.send_message(message.chat.id, f"🎉 ТЫ ПОБЕДИЛ! 🎉\n\nТвой приз: {price}.", reply_markup=markup)

                else:

                    new_time = float(time.time()) + reloading_time

                    cur.execute(f"UPDATE users SET r_time = {new_time} WHERE id = {message.from_user.id}")

                    bot.send_message(message.chat.id, f"😔 ТЫ ПРОИГРАЛ! 😔")

            
            except Exception as e:
                print(repr(e))

        else:

            get_data = int(i[2])
            rasnica = float(get_data) - float(time.time())

            item2 = types.InlineKeyboardButton("Закрыть", callback_data="close")

            markup = types.InlineKeyboardMarkup(row_width=1).add(
                item2
            )

            bot.send_message(message.chat.id, "Вы уже крутили рулетку!\nПопробуйте через: <i>" + str(datetime.strftime(datetime.utcfromtimestamp(rasnica), '%H:%M:%S')) + "</i> ☺", parse_mode="html",  reply_markup=markup)

        db.commit()


            
