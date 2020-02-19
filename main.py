# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 14:55:57 2020

@author: Henri Lencioni
"""

from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from doge import pic, vid
import numpy as np
from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd

def fetch(bot, update):
    #pass arguments to fetch yahoo data???
    global amazon, apple, index
    print('fetch')
    start_date = '2018-01-01'
    end_date = '2020-01-01'
    amazon = data.DataReader('AMZN', 'yahoo', start_date, end_date)
    print('amazon')
    apple = data.DataReader('AAPL', 'yahoo', start_date, end_date)
    print('apple')
    index = data.DataReader('SPY', 'yahoo', start_date, end_date)
    print('index')
    chat_id = update.message.chat_id
    bot.sendMessage(chat_id = chat_id, text = "Fetched the data!")
    
def data_f(bot, update, args):
    print('data')
    chat_id = update.message.chat_id
    if not args:
        bot.sendMessage(chat_id = chat_id, text = "Please pass arguments")
    for arg in args:
        if arg not in ['amazon', 'apple', 'index']:
            message = "Error: " + arg + " argument is not valid..." 
            bot.sendMessage(chat_id = chat_id, text = message)
        elif globals()[arg] is None:
            message = "Error: Remember to fetch " + arg + "!"
            bot.sendMessage(chat_id = chat_id, text = message)
        else:
            bot.sendMessage(chat_id = chat_id, text = arg)
            bot.sendMessage(chat_id = chat_id, text = globals()[arg].tail().to_string())

# def plot hae yksi ja plottaa
# def plot hae argumenttien mukaan
# plot joka näyttää myös moving average
# plot joka standardoi muuttujat ja plottaa päällekkäin

def main():
    updater = Updater('1084871037:AAFlb-Z9LXTsgot3gj4sOxaaE64M64dBUCM')
    global amazon, apple, index
    amazon, apple, index = None, None, None
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('pic',pic))
    dp.add_handler(CommandHandler('vid',vid))
    dp.add_handler(CommandHandler('fetch', fetch))
    dp.add_handler(CommandHandler("data", data_f, pass_args = True))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()