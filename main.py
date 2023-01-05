import telebot
import os
import logging
from config import *
from flask import Flask, request
from telebot import types

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
logger = telebot.logger
logger.setLevel(logging.DEBUG)
'''
@bot.message_handler(commands=["start"])
def start(message):
    username = message.from_user.username
    bot.reply_to(message, f"Hello, {username}!")
    #bot.send_message(message.chat.id, message)
'''

def extract_unique_code(text):
    # Extracts the unique_code from the sent /start command.
    return text.split()[1] if len(text.split()) > 1 else None

@bot.message_handler(commands=['start'])
def start(message):
    #bot.send_message(message.chat.id, message)
    bot.send_photo(message.chat.id, "https://imgur.com/q9ZPNyg")
    unique_code = extract_unique_code(message.text)
    if unique_code != None:
        bot.send_message(CHAT_ID_1, unique_code)
    bot.send_message(CHAT_ID_1,
                     f'{message.from_user.first_name}\t{message.from_user.last_name}\t{message.from_user.username}\t{message.from_user.language_code}')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    name = f'Здравствуйте, {message.from_user.first_name}, что вас интересует?'
    btn_remont = types.KeyboardButton("Ремонт спецтехники")
    btn_magaz = types.KeyboardButton("Магазин запчастей")
    btn_contact = types.KeyboardButton("Контакты")
    btn_site = types.KeyboardButton("Сайт")
    markup.add(btn_remont, btn_magaz)
    markup.add(btn_contact, btn_site)
    bot.send_message(message.chat.id, name, reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_user_text(message):
    if message.text == "Магазин запчастей":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_salnik = types.KeyboardButton("Сальник")
        btn_manjet = types.KeyboardButton("Манжет")
        markup.add(btn_salnik, btn_manjet)
        bot.send_message(message.chat.id, 'Выберете деталь', reply_markup=markup)
    elif message.text == "Ремонт спецтехники":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_gidromotor = types.KeyboardButton("Гидравлика")
        btn_gidrocilindr = types.KeyboardButton("Редуктор")
        btn_dvigatel = types.KeyboardButton("Ходовая часть")
        btn_kovsh = types.KeyboardButton("Ковш")
        btn_shtok = types.KeyboardButton("Мотор")
        btn_raspred = types.KeyboardButton("Топливная система")
        markup.add(btn_gidromotor, btn_gidrocilindr, btn_dvigatel, btn_kovsh, btn_shtok, btn_raspred)
        bot.send_message(message.chat.id, 'Что у вас сломалось?', reply_markup=markup)
    elif message.text == "Контакты":
        bot.send_message(message.chat.id, "По всем вопросам вы можете написать сюда @Bee_roi")
    elif message.text == "Сайт":
        bot.send_message(message.chat.id, "Наш сайт gidroservis.uz")
    elif message.text == "Гидравлика" or message.text == "Редуктор" or message.text == "Ходовая часть" or message.text == "Ковш" or message.text == "Мотор" or message.text == "Топливная система" or message.text == "Сальник" or message.text == "Манжет":
        service = message.text
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_phone = types.KeyboardButton(text='Отправить номер', request_contact=True)
        keyboard.add(button_phone)
        bot.send_message(message.chat.id, 'Нажмите "Отправить номер". Мы позвоним и проконсультируем вас', reply_markup=keyboard)
        @bot.message_handler(content_types=['contact'])
        def contact(message):
            if message.contact is not None:
                bot.forward_message(CHAT_ID_1, message.chat.id, message.message_id)
                bot.send_message(CHAT_ID_1, service)
                #bot.forward_message(CHAT_ID_2, message.chat.id, message.message_id)
                #bot.send_message(CHAT_ID_2, service)
                #bot.forward_message(CHAT_ID_3, message.chat.id, message.message_id)
                #bot.send_message(CHAT_ID_3, service)
                bot.send_message(message.chat.id, 'Заявка принята. Очень скоро мы позвоним вам. \nЕсли вам нужно что-то ещё, нажмите /start\n\nТак же можете посетить наш сайт gidroservis.uz', reply_markup=types.ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id, 'Чтобы поговорить с реальным человеком, напишите сюда @Beeroi\nЛибо нажмите /start и начните сначала')

@server.route(f"/{TOKEN}", methods=["POST"])
def redirect_message():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))