# Что же, мне лень было делать бота на aiogram
# Переписсывается данный бот буквально за несколько часов.
# ================================================================================
# Создатель бота: Nodus
# Telegram: @sirsus
# Vk: @crypto_ware
# ================================================================================
# Постарался добавлять комментарии по необходимости
# Сама библиотека изучается буквально за 1 час.
# Присутствует куча гавно кода (красивого зато)
# ================================================================================
# Что вам нужно сделать:
# 1. Подключить оплату
# 2. Создать систему выдачи обновлений (если вы хотите продавать кфг с обновами)
# 3. Желательно переписать бота на Aiogram библиотеку
# 4. Создать админку, и выдачу товара
# ================================================================================
# Удачи

# Бот
import telebot
from telebot import types

# Наша БД
import sqlite3 as sqlite 

# Забираем данные из config'a
from config import TOKEN, ADMIN_ID, INTRO
from messages import START_MSG, CFG_MSG, REVIEWS_MSG, FQA_MSG

# Рулетка
import ruletka

# Визуалка
import time
import os
from random import *

# Создаем нашего бота
bot = telebot.TeleBot(TOKEN)

os.system("cls")
# os.system("clear")
if INTRO == 1:
    time.sleep(1)
    print("---------------------------------------")
    time.sleep(0.25)
    print("|      TELEGRAM CFG SHOP TEMPLATE     |")
    time.sleep(1)
    print("|            Created by Nodus         |")
    time.sleep(1)
    print("| https://yougame.biz/threads/184424/ |")
    time.sleep(1)
    print("|             VERSION: 1.1            |")
    time.sleep(0.25)
    print("|-------------------------------------|")
    time.sleep(1)
    print("|              CHANGE LOG             |")
    time.sleep(1)
    print("|        [+] Added ban system         |")
    time.sleep(0.5)
    print("|        [+] Added random cfg         |")
    time.sleep(0.5)
    print("|        [+] Fix bugs                 |")
    time.sleep(0.5)
    print("|        [+] Added key system         |")
    time.sleep(0.5)
    print("|-------------------------------------|")
    time.sleep(1)
    print("|             LAST UPDATE             |")
    time.sleep(1)
    print("|       30.01.2021 in 01:48:20 PM     |")
    time.sleep(1)
    print("---------------------------------------")
    time.sleep(5)
    os.system("cls")
    # os.system("clear")
print("Bot Working...")

WORK_STATUS = None

# Проверка ADMIN_ID
if ADMIN_ID == 0:
    print("[АХТУНГ] Введи admin id")
    WORK_STATUS = False
else:
    WORK_STATUS = True

# Проверка токена (в любом случае если его не будет бот не будет рабоать лол)
if TOKEN == 'change this':
    print("[АХТУНГ] Введи TOKEN")
    WORK_STATUS = False
else:
    WORK_STATUS = True
    
# ============================================================================================ 

# Обработчик комманды /start
@bot.message_handler(commands=['start'])
def start(message):

    # Подключение к БД и создаем курсор
    db = sqlite.connect('base.db')
    cur = db.cursor()

    # Проверка на наличие бд по telegram user id
    try:
        cur.execute(f"SELECT * FROM users WHERE id = {message.from_user.id}")
    except Exception as e:
        print(repr(e))

    # Если пользователя нет в бд
    if not cur.fetchone():
        try:
            # Добавляем в бд
            cur.execute("INSERT INTO users VALUES (?,?,?)", (
                message.from_user.id, # ID пользователя
                message.from_user.username, # Username пользователя (если нет вернет None или что то такого)
                129600,
            ))

            print(f"User: {message.from_user.id} successfully added!")
        except Exception as e:
            print(repr(e))
    else:
        print(f"User: {message.from_user.id} in the base yet...")

    db.commit()

    # Проверка на админа
    if message.from_user.id != ADMIN_ID:

        try:
            cur.execute(f"SELECT * FROM banlist WHERE id = {message.from_user.id}")
        except Exception as e:
            print(repr(e))

        if not cur.fetchone():
        
            # Клавиатура (под полем ввода текста)
            markup = types.ReplyKeyboardMarkup(row_width=1)

            # Наши кнопки
            item1 = types.KeyboardButton("📄 Конфиги 📄")
            item2 = types.KeyboardButton("💬 Отызвы 💬")
            item3 = types.KeyboardButton("❓ F.Q.A ❔")
            item4 = types.KeyboardButton("🎰 Рулетка 🎰")

            # Добавляем кнопки к клаве
            markup.add(
                item1,
                item2,
                item3,
                item4
            )

            # Сообщение
            # Редактируется в messages.py
            # Если хотите не хотите использовать HTML как редактор сообщений, то измените parse_mode="html" на parse_mode="Markdown".
            bot.send_message(message.chat.id, START_MSG, parse_mode="html", reply_markup=markup)

        else:

            for i in cur.execute(f"SELECT * FROM banlist WHERE id = {message.from_user.id}"):

                reason = str(i[1])

                bot.send_message(message.chat.id, f"Вы были забанены администратором/модератором по причине: {reason}")

    elif message.from_user.id == ADMIN_ID:

        # Клавиатура (под сообщением)
        markup = types.InlineKeyboardMarkup(row_width=1)

        # Кнопки
        item1 = types.InlineKeyboardButton("Управление конфигами", callback_data="general cfg")
        item2 = types.InlineKeyboardButton("Управление ботом", callback_data="general bot")
        item3 = types.InlineKeyboardButton("Забанить пользователя", callback_data="ban user")
        item4 = types.InlineKeyboardButton("Перейти в панель участника", callback_data="go to user panel")
        item5 = types.InlineKeyboardButton("Закрыть панель", callback_data="close")

        markup.add(
            item1,
            item2,
            item3,
            item4,
            item5,
        )

        # Сообщение
        bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name}!", parse_mode="html",reply_markup=markup)
    
    # Закрываем БД
    if db:
        db.close()

# ============================================================================================ 

# Отправка сообщения
@bot.message_handler(commands=['mail'])
def mail(message):

    if message.from_user.id == ADMIN_ID:

        msg = bot.send_message(message.chat.id, "Введите сообщение")
        bot.register_next_step_handler(msg, send_mail)

def send_mail(message):

    db = sqlite.connect("base.db")
    cur = db.cursor()

    markup = types.InlineKeyboardMarkup(row_width=1)

    item1 = types.InlineKeyboardButton("Закрыть", callback_data="close")

    markup.add(
        item1
    )

    try:
        for i in cur.execute(f"SELECT * FROM users"):

            bot.send_message(i[0], message.text, parse_mode="html", reply_markup=markup)

    except Exception as e:
        print(repr(e))

    if db:
        db.close

# ============================================================================================ 

@bot.message_handler(commands=['activate'])
def activate(message):

    msg = bot.send_message(message.chat.id, "Введите ключ")
    bot.register_next_step_handler(msg, activate_key)

# ============================================================================================ 

# Обработчик текста
@bot.message_handler(content_types=['text'])
def message(message):

    if message.chat.type == 'private':

        if message.text.lower() == "💬 отызвы 💬":

            db = sqlite.connect('base.db')
            cur = db.cursor()

            try:
                cur.execute(f"SELECT * FROM banlist WHERE id = {message.from_user.id}")
            except Exception as e:
                print(repr(e))
            
            if not cur.fetchone():

                bot.send_message(message.chat.id, REVIEWS_MSG)

            else:
                try:
                    for i in cur.execute(f"SELECT * FROM banlist WHERE id = {message.from_user.id}"):

                        reason = str(i[1])

                        bot.send_message(message.chat.id, f"Вы были забанены администратором/модератором по причине: {reason}")

                except Exception as e:
                    print(repr(e))

            if db:
                db.close

        if message.text.lower() == "❓ f.q.a ❔":

            db = sqlite.connect('base.db')
            cur = db.cursor()

            try:
                cur.execute(f"SELECT * FROM banlist WHERE id = {message.from_user.id}")
            except Exception as e:
                print(repr(e))
            
            if not cur.fetchone():

                bot.send_message(message.chat.id, FQA_MSG)

            else:
                try:
                    for i in cur.execute(f"SELECT * FROM banlist WHERE id = {message.from_user.id}"):

                        reason = str(i[1])

                        bot.send_message(message.chat.id, f"Вы были забанены администратором/модератором по причине: {reason}")

                except Exception as e:
                    print(repr(e))
            
            if db:
                db.close
        
        elif message.text.lower() == "🎰 рулетка 🎰":

            ruletka.start(message)
        
        # Можно было бы сделать так, что бы он определял по слову в мессадже, но мне лень это делать, кто захочет, тот сделает
        elif message.text.lower() == '📄 конфиги 📄':

            db = sqlite.connect('base.db')
            cur = db.cursor()

            try:
                cur.execute(f"SELECT * FROM banlist WHERE id = {message.from_user.id}")
            except Exception as e:
                print(repr(e))
            
            if not cur.fetchone():

                markup = types.ReplyKeyboardMarkup(row_width=2)

                item1 = types.KeyboardButton("Onetap")
                item2 = types.KeyboardButton("gamesense")
                item3 = types.KeyboardButton("Evolve")
                item4 = types.KeyboardButton("Legendware")
                item5 = types.KeyboardButton("Spirthack")
                item6 = types.KeyboardButton("XONE")
                item7 = types.KeyboardButton("OTC 2")
                item8 = types.KeyboardButton("OTC 3")
                item9 = types.KeyboardButton("BoberHook")
                item10 = types.KeyboardButton("Neverlose")
                item11 = types.KeyboardButton("❌ Назад ❌")

                markup.add(
                    item1, item2,
                    item3, item4,
                    item5, item6,
                    item7, item8,
                    item9, item10,
                    item11,
                )


                bot.send_message(message.chat.id, "Выбери конфиг", reply_markup=markup)

            else:
                try:
                    for i in cur.execute(f"SELECT * FROM banlist WHERE id = {message.from_user.id}"):

                        reason = str(i[1])

                        bot.send_message(message.chat.id, f"Вы были забанены администратором/модератором по причине: {reason}")

                except Exception as e:
                    print(repr(e)) 

            if db:
                db.close

        
        elif message.text.lower() == "gamesense":

            db = sqlite.connect('base.db')
            cur = db.cursor()

            try:
                cur.execute(f"SELECT * FROM banlist WHERE id = {message.from_user.id}")
            except Exception as e:
                print(repr(e))
            
            if not cur.fetchone():

                try:
                    cur.execute(f"SELECT * FROM configs WHERE cheat = 'gamesense'")
                except Exception as e:
                    print(repr(e))

                if not cur.fetchone():

                    bot.send_message(message.chat.id, "К сожалению конфига нет!")
                
                else:

                    for x in cur.execute(f"SELECT * FROM configs WHERE cheat = 'gamesense'"):

                        desc = str(x[1])
                        price = int(x[2])
                        link = str(x[3])

                        markup = types.InlineKeyboardMarkup(row_width=1)

                        if message.from_user.id != ADMIN_ID:

                            item1 = types.InlineKeyboardButton("Купить", callback_data="buy_gamesense")
                        else:
                            item1 = types.InlineKeyboardButton("Получить", url=link)

                        item2 = types.InlineKeyboardButton("Закрыть", callback_data="close")

                        markup.add(
                            item1,
                            item2
                        )

                        bot.send_message(message.chat.id, 
                        f"| Покупка конфига на <b>Gamesense</b>\nОписание: <i>{desc}</i>\n\nСтоимость: <b>{price}</b>", parse_mode="html", reply_markup=markup)
            
            else:
                try:
                    for i in cur.execute(f"SELECT * FROM banlist WHERE id = {message.from_user.id}"):

                        reason = str(i[1])

                        bot.send_message(message.chat.id, f"Вы были забанены администратором/модератором по причине: {reason}")

                except Exception as e:
                    print(repr(e))
            if db:
                db.close
        
        elif message.text.lower() == "onetap":

            db = sqlite.connect('base.db')
            cur = db.cursor()

            try:
                cur.execute(f"SELECT * FROM banlist WHERE id = {message.from_user.id}")
            except Exception as e:
                print(repr(e))
            
            if not cur.fetchone():

                try:
                    cur.execute(f"SELECT * FROM configs WHERE cheat = 'onetap'")
                except Exception as e:
                    print(repr(e))

                if not cur.fetchone():

                    bot.send_message(message.chat.id, "К сожалению конфига нет!")
                
                else:

                    for x in cur.execute(f"SELECT * FROM configs WHERE cheat = 'onetap'"):

                        desc = str(x[1])
                        price = int(x[2])
                        link = str(x[3])

                        markup = types.InlineKeyboardMarkup(row_width=1)

                        if message.from_user.id != ADMIN_ID:

                            item1 = types.InlineKeyboardButton("Купить", callback_data="buy_gamesense")
                        else:
                            item1 = types.InlineKeyboardButton("Получить", url=link)

                        item2 = types.InlineKeyboardButton("Закрыть", callback_data="close")

                        markup.add(
                            item1,
                            item2
                        )

                        bot.send_message(message.chat.id, 
                        f"| Покупка конфига на <b>Gamesense</b>\nОписание: <i>{desc}</i>\n\nСтоимость: <b>{price}</b>", parse_mode="html", reply_markup=markup)
            
            else:
                try:
                    for i in cur.execute(f"SELECT * FROM banlist WHERE id = {message.from_user.id}"):

                        reason = str(i[1])

                        bot.send_message(message.chat.id, f"Вы были забанены администратором/модератором по причине: {reason}")

                except Exception as e:
                    print(repr(e))
            if db:
                db.close

        
        # Вам нужно дополнить конфиги
        
        elif message.text.lower() == "evolve":

            pass

        elif message.text.lower() == "legendware":

            pass

        
        elif message.text.lower() == "spirthack":

            pass

        elif message.text.lower() == "neverlose":

            pass

        elif message.text.lower() == "xone":

            pass

        elif message.text.lower() == "otc 2":

            pass

        
        elif message.text.lower() == "otc 3":

            pass

        elif message.text.lower() == "boberhook":

            pass

# ============================================================================================ 

# Бан пользователя
def banuser(message):

    db = sqlite.connect('base.db')
    cur = db.cursor()

    try:
        cur.execute(f"SELECT * FROM banlist WHERE id = {message.from_user.id}")
    except Exception as e:
        print(repr(e))

    if not cur.fetchone():
        try:
            cur.execute("INSERT INTO banlist VALUES (?,?)", (
                int(message.text),
                "Без указания причины"
            ))

            msg = bot.send_message(message.chat.id, f"Введите причину бана")
            bot.register_next_step_handler(msg, banuser2)
        except Exception as e:
            print(repr(e))
    else:

        for i in cur.execute(f"SELECT * FROM banlist WHERE id = {message.text}"):

            reason = str(i[1])

            bot.send_message(message.chat.id, f"Пользователь: {message.text} уже забанен по причине: {reason}!")

    db.commit()

    if db:
        db.close

def banuser2(message):

    db = sqlite.connect('base.db')
    cur = db.cursor()

    try:
        for x in cur.execute(f"SELECT * FROM banlist WHERE id = {message.from_user.id}"):

            try:

                id = str(x[0])

                cur.execute(f"UPDATE banlist SET reason = '{message.text}' WHERE id = {id}")

            except Exception as e:
                print(repr(e))
    except Exception as e:
        print(repr(e))

    db.commit()

    if db:
        db.close

# ============================================================================================ 

# Изменение приза в рулетке
def new_prize(message):

    db = sqlite.connect('base.db')
    cur = db.cursor()

    try:
        cur.execute(f"UPDATE rulletka SET priz = '{message.text}'")

        msg = bot.send_message(message.chat.id, "Введите ссылку на получение товара")
        bot.register_next_step_handler(msg, new_prize2)
    except Exception as e:
        print(repr(e))

    db.commit()

    if db:
        db.close

def new_prize2(message):

    db = sqlite.connect('base.db')
    cur = db.cursor()

    try:
        cur.execute(f"UPDATE rulletka SET link = '{message.text}'")

        bot.send_message(message.chat.id, "В приз в рулетке был обновлен!")
    except Exception as e:
        print(repr(e))

    db.commit()

    if db:
        db.close

# ============================================================================================ 
# Создание и активация ключа
def generate_key(message):

    db = sqlite.connect('base.db')
    cur = db.cursor()

    try:
        cur.execute(f"SELECT * FROM configs WHERE cheat = '{message.text}'")
    except Exception as e:
        print(repr(e))

    if not cur.fetchone():

        msg = bot.send_message(message.chat.id, "Конфиг не найден!\nПроверьте правильность написания или наличие конфигурации и повторите попытку")
        bot.register_next_step_handler(msg, generate_key)

    else:

        for x in cur.execute(f"SELECT * FROM configs WHERE cheat = '{message.text}'"):

            try:

                chars = "zaqwsxcderfvbgtyhnmjuiklop" + "ZAQWSXCDERFVBGTYHNMJUIKLOP" + "1234567890"
                
                key = ''.join(choice(chars) for j in range(175))

                cur.execute("INSERT INTO keys VALUES (?,?,?)", (
                    key,
                    message.text,
                    str(x[3])
                ))

                bot.send_message(message.chat.id, f"Ключ был успешно создан!\n\n`{key}`", parse_mode="markdown")

            except Exception as e:
                print(repr(e))

        db.commit()

    if db:
        db.close

def activate_key(message):

    db = sqlite.connect('base.db')
    cur = db.cursor()

    try:
        cur.execute(f"SELECT * FROM keys WHERE key = '{message.text}'")
    except Exception as e:
        print(repr(e))

    if not cur.fetchone():

        msg = bot.send_message(message.chat.id, "Неверный ключ! Проверьте правильность ключа и повторите попытку!")
        bot.register_next_step_handler(msg, activate_key)

    else:

        for i in cur.execute(f"SELECT * FROM keys WHERE key = '{message.text}'"):

            markup = types.InlineKeyboardMarkup(row_width=1)

            item1 = types.InlineKeyboardButton("Получить товар", url=str(i[2]))
            item2 = types.InlineKeyboardButton("Закрыть", callback_data="close")

            markup.add(
                item1,
                item2
            )

            bot.send_message(message.chat.id, f"Вы успешно активировали ключ на {str(i[1])}!\n\nНажмите кнопку получить, что бы скачать товар!", reply_markup=markup)

            try:
                cur.execute(f"DELETE FROM keys WHERE key = '{message.text}'")
            except Exception as e:
                print(repr(e))
            
        db.commit()

        if db:
            db.close

# ============================================================================================ 

# Работа с инлайновыми кнопками
@bot.callback_query_handler(func=lambda call: True)
def call(call):

    if call.message:
        
        if call.data == "ban user":
            
            msg = bot.send_message(call.message.chat.id, "Введите ID пользователя")
            bot.register_next_step_handler(msg, banuser)

        elif call.data == "general cfg":

            markup = types.InlineKeyboardMarkup(row_width=2)

            item1 = types.InlineKeyboardButton("1", callback_data="1")
            item2 = types.InlineKeyboardButton("2", callback_data="2")
            item3 = types.InlineKeyboardButton("3", callback_data="3")
            item4 = types.InlineKeyboardButton("4", callback_data="4")
            item5 = types.InlineKeyboardButton("5", callback_data="5")
            item6 = types.InlineKeyboardButton("6", callback_data="6")
            item7 = types.InlineKeyboardButton("7", callback_data="7")
            item8 = types.InlineKeyboardButton("8", callback_data="8")
            item9 = types.InlineKeyboardButton("9", callback_data="9")
            item10 = types.InlineKeyboardButton("10", callback_data="10")
            item11 = types.InlineKeyboardButton("11", callback_data="11")
            
            markup.add(
                item1, item2,
                item3, item4,
                item5, item6,
                item7, item8,
                item9, item10,
                item11,
            )

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выберите конфиг для обновления данных", reply_markup=markup)

            
        elif call.data == "general bot":

            markup = types.InlineKeyboardMarkup(row_width=1)

            item1 = types.InlineKeyboardButton("Управление рулеткой", callback_data="ruletka")
            item3 = types.InlineKeyboardButton("Создать ключ", callback_data="create key")
            item2 = types.InlineKeyboardButton("Вернуться", callback_data="back to admin panel")

            markup.add(
                item1,
                item3,
                item2,
            )

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Управление ботом", reply_markup=markup)
        
        elif call.data == "create key":

            msg = bot.send_message(call.message.chat.id, "Введите конфиг который хотите зашифровать в ключ")
            bot.register_next_step_handler(msg, generate_key)
        
        elif call.data == "ruletra":

            db = sqlite.connect('base.db')
            cur = db.cursor()

            markup = types.InlineKeyboardMarkup(row_width=1)

            for i in cur.execute(f"SELECT * FROM rulletka"):

                if int(i[0]) == 0:

                    toggle = types.InlineKeyboardButton("Включить", callback_data="on ruletka")

                    item3 = types.InlineKeyboardButton("Назад", callback_data="general bot")

                    markup.add(
                        toggle,
                        item3,
                    )
                
                elif int(i[0]) == 1:
                
                    toggle = types.InlineKeyboardButton("Выключить", callback_data="of ruletka")

                    item1 = types.InlineKeyboardButton("Сменить приз", callback_data="change priz")
                    item3 = types.InlineKeyboardButton("Назад", callback_data="general bot")

                    markup.add(
                        toggle,
                        item1,
                        item3,
                    )

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Управление рулеткой", reply_markup=markup)
        
        elif call.data == 'change priz':

            msg = bot.send_message(call.message.chat.id, "Введите название приза")
            bot.register_next_step_handler(msg, new_prize)
        
        elif call.data == 'on ruletka':

            db = sqlite.connect('base.db')
            cur = db.cursor()

            cur.execute(f"UPDATE rulletka SET mode = {1}")

            db.commit()

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Управление рулеткой", reply_markup=markup)

            if db:
                db.close

        elif call.data == "of ruletka":

            db = sqlite.connect('base.db')
            cur = db.cursor()

            cur.execute(f"UPDATE rulletka SET mode = {0}")

            db.commit()

            if db:
                db.close
        
        elif call.data == "back to admin panel":

            start(message)
        
        elif call.data == "go to user panel":

            # Клавиатура (под полем ввода текста)
            markup = types.ReplyKeyboardMarkup(row_width=1)

            # Наши кнопки
            item1 = types.KeyboardButton("📄 Конфиги 📄")
            item2 = types.KeyboardButton("💬 Отызвы 💬")
            item3 = types.KeyboardButton("❓ F.Q.A ❔")
            item4 = types.KeyboardButton("🎰 Рулетка 🎰")

            # Добавляем кнопки к клаве
            markup.add(
                item1,
                item2,
                item3,
                item4
            )

            # Сообщение
            # Редактируется в messages.py
            # Если хотите не хотите использовать HTML как редактор сообщений, то измените parse_mode="html" на parse_mode="Markdown".
            bot.send_message(call.message.chat.id, START_MSG, parse_mode="html", reply_markup=markup)
        
        elif call.data == "close":

            bot.delete_message(call.message.chat.id, call.message.message_id)

        

# Запуск бота
if __name__ == "__main__":
    if WORK_STATUS == True:
        bot.polling(none_stop=True)