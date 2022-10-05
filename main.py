from email import message
from requests.models import Response
import requests
from telebot import types 
import telebot
import urllib.request 
import json



bot = telebot.TeleBot(token="5605459338:AAHHaeDpFFR9-_Ez4rWwQp-iWCU-fBiPhjY")
url:str ="https://gogoanime.herokuapp.com/recent-release"

@bot.message_handler(commands=["start"])
def start(message):
    mess=f"Приветствую, <i><b>{message.from_user.first_name}</b></i>"
    bot.send_message(message.chat.id, mess, parse_mode="html")
    # Keyboard(Inline)
    markup=types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Каталог Аниме!", generate_catalog(message)))
    bot.send_message(message.chat.id, "Решил глянуть японскую анимацию?", reply_markup=markup)

def generate_catalog(message):
    # Создание всего каталога( Все аниме, их названия и ссылка на просмотр)
    url:str ="https://gogoanime.herokuapp.com/recent-release"
    all_json: Response = requests.get(url)
    if all_json.status_code == 200:
        _all=all_json.json()
        
        num=1
        for i in _all:
            aLink=i["episodeUrl"]
            aTitle=i["animeTitle"]
            markup=types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Смотреть", url=aLink))
            bot.send_message(message.chat.id, f"{num}) {aTitle}", parse_mode="html", reply_markup=markup)
            img=i["animeImg"]
            p= requests.get(img)
            out = open(f"{num}img.png", "wb")
            out.write(p.content)
            out.close()
            photo=open(f"{num}img.png", "rb")
            bot.send_photo(message.chat.id, photo)
            num+=1
            

    else:
        print(all_json.status_code)
        
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        if call.data == "catalog":
            bot.send_message(message.chat.id, generate_catalog())

@bot.message_handler(commands=["help"])
def start(message):
    # Keyboard
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    katalog=types.KeyboardButton("Каталог")
    start=types.KeyboardButton("Start")
    markup.add(katalog,start)

    bot.send_message(message.chat.id, "Help is here!", reply_markup=markup)



@bot.message_handler(content_types=["text"])
def get_user_text(message): 
    bot.send_message(message.chat.id, "I don't understand", parse_mode="html")


bot.polling(none_stop=True)