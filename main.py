# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 14:55:57 2020

@author: Henri Lencioni
"""

from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import requests
import re

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
    bot.send_photo(chat_id=chat_id, photo=url)

def vid(bot, update):
    print("video")
    allowed_extension = ['gif','mp4']
    url = get_image_url(allowed_extension)
    chat_id = update.message.chat_id
    bot.sendAnimation(chat_id=chat_id, animation=url)
    
def main():
    updater = Updater('1084871037:AAFlb-Z9LXTsgot3gj4sOxaaE64M64dBUCM')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('pic',pic))
    dp.add_handler(CommandHandler('vid',vid))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()