# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 14:55:57 2020

@author: Henri Lencioni
"""

from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from doge import pic, vid
from data import fetch, data_f

def apple_f(bot, update):
    print("apple plot")
    fig, ax = plt.subplots(figsize=(16,9))
    ax.plot(apple.index, apple['Close'], label="apple")
    ax.plot(apple.index, apple['close_ma_20'], label='20 days rolling')
    ax.plot(apple.index, apple['close_ma_100'], label='100 days rolling')
    ax.set_xlabel('Date')
    ax.set_ylabel('Closing price ($)')
    ax.legend()
    fig.savefig('python-bot/' + 'apple')
    print("apple saved")
    # bot.sendPhoto(chat_id = chat_id, photo = open('python-bot/apple', 'rb'))


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
            print('python-bot/' + arg)
            fig.savefig('python-bot/' + arg)
            print("photo saved")
            # bot.sendPhoto(chat_id = chat_id, photo = open('python-bot/amazon', 'rb'))
            # bot.sendMessage(chat_id = chat_id, text = "plot " + arg)

# plot joka standardoi muuttujat ja plottaa päällekkäin

def help(bot, update):
    print('help')
    chat_id = update.message.chat_id
    message = """Hello and welcome to my demo python bot!
    
    Commands include:
    /pic for a cute doggo picture!
    /vid for a dog animation
    /fetch to access data for apple, amazon and index (S&P500)
    /data to see the actual data (remember to fetch first and pass one
    of the arguments)
    /plot (under construction) to plot the closing prices and moving
    averages for the stocks"""
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
    dp.add_handler(CommandHandler("data", data_f, pass_args = True))
    dp.add_handler(CommandHandler("plot", plot, pass_args = True))
    dp.add_handler(CommandHandler('apple', apple_f))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()