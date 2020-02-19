# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 10:54:35 2020

@author: Henri Lencioni
"""

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
    bot.sendPhoto(chat_id = chat_id, photo = url)

def vid(bot, update):
    print("video")
    allowed_extension = ['gif','mp4']
    url = get_image_url(allowed_extension)
    chat_id = update.message.chat_id
    bot.sendAnimation(chat_id = chat_id, animation = url)