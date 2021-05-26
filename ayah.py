import requests
import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot
import random


import os
APITOKEN = os.environ.get('APITOKEN2')
bot = telebot.TeleBot(APITOKEN)


def gen_markup(textMessage):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton(textMessage, callback_data='ok'))
    return markup


# print(ayahinsura)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = bot.send_message(
        message.chat.id, "\"بِسْمِ اللَّـهِ الرَّحْمَـٰنِ الرَّحِيمِ  \n (اقْرَؤُوا القُرْآنَ فإنَّه يَأْتي يَومَ القِيامَةِ شَفِيعًا لأَصْحابِهِ)\"", reply_markup=gen_markup('ارسل لي اية'))


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

    try:
        aya_num = random.randint(1, 6237)
        randomAyaha = requests.get(
            'http://api.alquran.cloud/ayah/'+str(aya_num)).json()
        ayah = randomAyaha['data']['text']
        sura = randomAyaha['data']['surah']['name']
        sajda = bool(randomAyaha['data']['sajda'])
        ayahinsura = randomAyaha['data']['numberInSurah']

        ifsajda = 'توجد سجدة' if sajda else ''

        if(call.data):
            bot.send_message(call.from_user.id, '*'+str(ayah)+'*' +
                             '\n\n'+str(sura)+'\n\n' + 'اية'+str(ayahinsura) + ifsajda)
            bot.send_message(call.from_user.id, "احسنت",reply_markup=gen_markup('ارسل اية اخرى'))

    except:
        bot.send_message(call.from_user.id,
                         'something went wrong try agin later')


bot.polling()
