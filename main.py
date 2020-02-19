# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 14:55:57 2020

@author: Henri Lencioni
"""

from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import requests
import re
import numpy as np
from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()    
    url = contents['url']
    return url

def get_image_url(allowed_extension):
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url

def pic(bot, update):
    print("picture")
    allowed_extension = ['jpg','jpeg','png']
    url = get_image_url(allowed_extension)
    chat_id = update.message.chat_id
    bot.send_photo(chat_id = chat_id, photo = url)

def vid(bot, update):
    print("video")
    allowed_extension = ['gif','mp4']
    url = get_image_url(allowed_extension)
    chat_id = update.message.chat_id
    bot.sendAnimation(chat_id = chat_id, animation = url)
    
def fetch(bot, update):
    print('fetch')
    tickers = ['AMZN', 'GOOG', '.INX']
    start_date = '2000-01-01'
    end_date = '2020-01-01'
    amazon = data.DataReader('AMZN', 'yahoo', start_date, end_date)
    google = data.DataReader('AAPL', 'yahoo', start_date, end_date)
    index = data.DataReader('SPY', 'yahoo', start_date, end_date)
    chat_id = update.message.chat_id
    bot.sendMessage(chat_id = chat_id, text = "Fetched the data!")
    
def data(bot, update, args):
    for arg in args:
        print(arg)
    

def main():
    updater = Updater('1084871037:AAFlb-Z9LXTsgot3gj4sOxaaE64M64dBUCM')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('pic',pic))
    dp.add_handler(CommandHandler('vid',vid))
    dp.add_handler(CommandHandler('fetch', fetch))
    dp.add_handler(CommandHandler("data", data, pass_args = True))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()