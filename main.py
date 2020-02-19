# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 14:55:57 2020

@author: Henri Lencioni
"""

from telegram.ext import Updater, InlineQueryHandler, CommandHandler, Filters

from doge import pic, vid
from data import plot, standardized, data_f, fetch

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
    /standardized plots all three stocks on the same plot
    standardized to start from 1
    /help and of course we have the command you just used :)
    
    Have fun!"""
    bot.sendMessage(chat_id = chat_id, text = message)
    

def main():
    updater = Updater('1084871037:AAFlb-Z9LXTsgot3gj4sOxaaE64M64dBUCM')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('pic',pic))
    dp.add_handler(CommandHandler('vid',vid))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('fetch', fetch))
    dp.add_handler(CommandHandler('standardized', standardized))
    dp.add_handler(CommandHandler("data", data_f, pass_args = True))
    dp.add_handler(CommandHandler("plot", plot, pass_args = True))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()