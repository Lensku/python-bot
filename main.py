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
    amazon.insert(6, "close_ma_20", amazon['Close'].rolling(20).mean())
    amazon.insert(7, "close_ma_100", amazon['Close'].rolling(100).mean())
    print('amazon')
    apple = data.DataReader('AAPL', 'yahoo', start_date, end_date)
    apple.insert(6, "close_ma_20", apple['Close'].rolling(20).mean())
    apple.insert(7, "close_ma_100", apple['Close'].rolling(100).mean())
    print('apple')
    index = data.DataReader('SPY', 'yahoo', start_date, end_date)
    index.insert(6, "close_ma_20", index['Close'].rolling(20).mean())
    index.insert(7, "close_ma_100", index['Close'].rolling(100).mean())
    print('index')
    chat_id = update.message.chat_id
    bot.sendMessage(chat_id = chat_id, text = "Fetched the data!")
    
def data_f(bot, update, args):
    print('data')
    chat_id = update.message.chat_id
    if not args:
        bot.sendMessage(chat_id = chat_id, text = "Please pass an argument")
    for arg in args:
        if arg not in ['amazon', 'apple', 'index']:
            message = "Error: " + arg + " argument is not valid..." 
            bot.sendMessage(chat_id = chat_id, text = message)
        elif globals()[arg] is None:
            message = "Error: Remember to fetch " + arg + "!"
            bot.sendMessage(chat_id = chat_id, text = message)
        else:
            bot.sendMessage(chat_id = chat_id, text = arg)
            bot.sendMessage(chat_id = chat_id, text = globals()[arg].round(2).tail().to_string())

def plot(bot,update, args):
    print("plot")
    chat_id = update.message.chat_id
    if not args:
        bot.sendMessage(chat_id = chat_id, text = "Please pass an argument")
    for arg in args:
        if arg not in ['amazon', 'apple', 'index']:
            message = "Error: " + arg + " argument is not valid..." 
            bot.sendMessage(chat_id = chat_id, text = message)
        elif globals()[arg] is None:
            message = "Error: Remember to fetch " + arg + "!"
            bot.sendMessage(chat_id = chat_id, text = message)
        else:
            print("else")
            fig, ax = plt.subplots(figsize=(16,9))
            ax.plot(globals()[arg].index, globals()[arg]['Close'], label=arg)
            ax.plot(globals()[arg].index, globals()[arg]['close_ma_20'], label='20 days rolling')
            ax.plot(globals()[arg].index, globals()[arg]['close_ma_100'], label='100 days rolling')
            print("axes")
            ax.set_xlabel('Date')
            ax.set_ylabel('Closing price ($)')
            ax.legend()
            print("photo")
            fig.savefig('python-bot/' + arg)
            print("photo saved")
            # bot.sendPhoto(chat_id = chat_id, photo = open('python-bot/amazon', 'rb'))
            # bot.sendMessage(chat_id = chat_id, text = "plot " + arg)
"""
print("else")
fig, ax = plt.subplots(figsize=(16,9))
ax.plot(apple.index, apple['Close'], label="apple")
ax.plot(apple.index, apple['close_ma_20'], label='20 days rolling')
ax.plot(apple.index, apple['close_ma_100'], label='100 days rolling')
print("axes")
ax.set_xlabel('Date')
ax.set_ylabel('Closing price ($)')
ax.legend()
print("photo")
fig.savefig('python-bot/' + 'apple')
print("photo saved")
"""

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
    dp.add_handler(CommandHandler("plot", plot, pass_args = True))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()