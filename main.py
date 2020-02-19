# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 14:55:57 2020

@author: Henri Lencioni
"""

from telegram.ext import Updater, InlineQueryHandler, CommandHandler, Filters
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO

from doge import pic, vid
from data import fetch, data_f

def apple_f(bot, update):
    print("apple plot")
    if apple is None:
        print("none")
    chat_id = update.message.chat_id
    print(apple.round(2).tail())
    fig, ax = plt.subplots(figsize=(16,9))
    ax.plot(apple.index, apple['Close'], label="apple")
    ax.plot(apple.index, apple['close_ma_20'], label='20 days rolling')
    ax.plot(apple.index, apple['close_ma_100'], label='100 days rolling')
    ax.set_xlabel('Date')
    ax.set_ylabel('Closing price ($)')
    ax.legend()
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    update.message.reply_photo(buffer)
    print("test")

def standardized(bot, update):
    print("standardized")
    chat_id = update.message.chat_id
    if globals() is None:
        bot.sendMessage(chat_id = chat_id, text = "Error: Remember to fetch!")
    else:
        print("plotting")
        fig, ax = plt.subplots(figsize=(16,9))
        ax.plot(amazon.index, amazon['standardized'], label="amazon")
        ax.plot(apple.index, apple['standardized'], label="apple")
        ax.plot(index.index, index['standardized'], label="index")
        ax.set_xlabel('Date')
        ax.set_ylabel('Closing price ($)')
        ax.legend()
        fig.savefig('python-bot/standardized.png')
        print("fig saved standard")
        bot.sendPhoto(chat_id = chat_id, photo = open('python-bot/standardized.png', 'rb'))
        # bot.sendMessage(chat_id = chat_id, text = "plot " + arg)

def plot(bot, update, args):
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
            fig, ax = plt.subplots(figsize=(16,9))
            ax.plot(globals()[arg].index, globals()[arg]['Close'], label=arg)
            ax.plot(globals()[arg].index, globals()[arg]['close_ma_20'], label='20 days rolling')
            ax.plot(globals()[arg].index, globals()[arg]['close_ma_100'], label='100 days rolling')
            ax.set_xlabel('Date')
            ax.set_ylabel('Closing price ($)')
            ax.legend()
            buffer = BytesIO()
            fig.savefig(buffer, format='png')
            buffer.seek(0)
            update.message.reply_photo(buffer)

# plot joka standardoi muuttujat ja plottaa päällekkäin

def help(bot, update):
    print('help')
    chat_id = update.message.chat_id
    message = """Hello and welcome to my demo python bot!
    
    Commands include:
    /pic for a cute doggo picture!
    /vid for a dog animation
    /fetch to access data for apple, amazon and index (S&P500)
    /data [args] to see the actual data (remember to fetch first)
    /plot [args] (under construction) to plot the closing prices and
    moving averages for the stocks
    /standardized plots all three stocks on the same plot as 
    standardized"""
    bot.sendMessage(chat_id = chat_id, text = message)
    

def main():
    updater = Updater('1084871037:AAFlb-Z9LXTsgot3gj4sOxaaE64M64dBUCM')
    global amazon, apple, index
    amazon, apple, index = None, None, None
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('pic',pic))
    dp.add_handler(CommandHandler('vid',vid))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('fetch', fetch))
    dp.add_handler(CommandHandler('standardized', standardized))
    dp.add_handler(CommandHandler("data", data_f, pass_args = True))
    dp.add_handler(CommandHandler("plot", plot, pass_args = True))
    dp.add_handler(CommandHandler('apple', apple_f))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()