# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 14:32:39 2020

@author: Henri Lencioni
"""

from pandas_datareader import data

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