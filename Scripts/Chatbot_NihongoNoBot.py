#!/usr/bin/env python
# coding: utf-8


# Libraries 
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from google_trans_new import google_translator
import pykakasi
import pandas as pd
import random
import numpy as np
import pyodbc 
import os

# Connect database
name = 'User-name'
database = 'Database-Name'
cnxn = pyodbc.connect(driver='{SQL Server}', server= name, database= database,               
               trusted_connection='yes')
cursor = cnxn.cursor()

# Create the translator
translator = google_translator()  
kks = pykakasi.kakasi()

# Add the vocabulary
teach_voc = pd.read_excel(r'C:/.../VocabJapanese.xls')
teach_voc = teach_voc.fillna('-')

# Brief explanation of Japanese Language 
intro_japanese = 'Japanese language can be read in different ways, brief explanation:\n'
intro_kanji = 'Kanji: characters that represent whole words.\n'
intro_hiragana = 'Hiragana: simplification of Kanji. This is usually the first alphabet learned and taught to people learning Japanese.\n'
intro_katakana = 'Katakana: type of reading maninly for words borrowed from other languages.\n'
intro_romanji = 'Romaji: how to write a Japanese word in Western characters.\n\n'
    

# Function start command
def start(update, context):
    
    # Get data - Unused
    # chat_id = update.message.chat_id
    # first_name = update.message.chat.first_name
    # last_name = update.message.chat.last_name
    # username = update.message.chat.username
    # date = update.message.date
    # file = update.update_id
    # data = [file, chat_id, first_name, last_name, username, str(date), 'Start']
    # print(data)
 
    # Introduction text
    intro_1 = 'Welcome to NihongoNoSensei!\n\n'
    intro_2 = 'The purpose of this bot is to help people learn Japanese. '
    intro_3 = 'Write something and it will automatically be translated into Japanese.\nIf you want to translate it to English, then write \'Jp\' before the message.\n'
    intro_4 = 'Press /help to get information about the bot.\n'
    intro_5 = 'Press /join in order to receive automatically a new word in Japanese every day.\n'
    intro_6 = 'If you can´t wait, then press /teachme and you will receive immediately a new word.\n\n'
    intro_7 = 'Bot developed by David Borque: https://www.linkedin.com/in/davidborque/\n\nCheck the code on GitHub: https://github.com/DavidBor17/Bot_NihongoNoSensei \nI hope you like it. Open to any suggestions.'
    intro_full = intro_1 + intro_2 + intro_japanese + intro_kanji + intro_hiragana + intro_katakana + intro_romanji + intro_3 + intro_4 + intro_5 + intro_6 + intro_7
    update.message.reply_text(intro_full)
    
    
    # Send screenshots
    file_1 = r'C:\...Screenshot1.jpg'
    file_2 = r'C:\...Screenshot2.jpg'
    update.message.reply_photo(photo = open(file_1,'rb'))
    update.message.reply_photo(photo = open(file_2,'rb'))
    


# Help command
def help(update, context):

    
    # Helpt text
    help_text_1 = 'Let´s get some help:\n'
    help_text_2 = 'The purpose of this bot is to help people learn Japanese. '
    help_text_3 = 'Write something and it will automatically be translated into Japanese.\n'
    help_text_4 = 'If you want to translate it to English, then write \'Jp\' before the message.\n'
    help_text_5 = 'Press /join in order to receive automatically a new word in Japanese every day.\n'
    help_text_6 = 'If you can´t wait, then press /teachme and you will receive immediately a new word.\n\n'
    help_text_7 = 'Bot developed by David Borque: https://www.linkedin.com/in/davidborque/ \n\nCheck the code on GitHub https://github.com/DavidBor17/Bot_NihongoNoSensei \nI hope you like it. Open to any suggestions.'
    help_text = help_text_1 + help_text_2 + intro_japanese + intro_kanji + intro_hiragana + intro_katakana + intro_romanji + help_text_3 + help_text_4 + help_text_5 + help_text_6 + help_text_7
    
    # Send help
    update.message.reply_text(help_text)
    
    # Send screenshots
    file_1 = r'C:/...Screenshot1.jpg'
    file_2 = r'C:/...Screenshot2.jpg'
    update.message.reply_photo(photo = open(file_1,'rb'))
    update.message.reply_photo(photo = open(file_2,'rb'))


# Function to handle errors occured in the dispatcher 
def error(update, context):
    update.message.reply_text('An error occurred, please contact the administrator.')

# Function to teach a new word 
def teachme(update, context):
    

    # Teach a random word    
    teach_1 = 'Let´s learn a new word!.\n'
    teach_2 = 'Kanji: {}, Hiragana: {}, Romanji: {}, Meaning: {}'.format(teach_voc.iloc[rand][3],teach_voc.iloc[rand][4],teach_voc.iloc[rand][6],teach_voc.iloc[rand][5])
    teach_full = teach_1 + teach_2
    update.message.reply_text(teach_full)

    
# Join the learn team
def join(update, context):
    
    # Send join message 
    update.message.reply_text('Thanks for joining the learning club. You will get an update of a new word every day.\nIn case you want to leave the group, then press /leave.')
    
    # Insert user into SQL Server 
    chat_id = update.message.chat_id
    cursor.execute("insert into club values('{}')".format(chat_id))
    cursor.commit()
    
# Leave the learn team    
def leave(update, context):
    
    # Send leave message
    update.message.reply_text('You have been deleted from the database, we hope to see you again.\nHave a great day!')
    
    # Delete the user
    chat_id = update.message.chat_id
    cursor.execute("delete from club where ids = ('{}')".format(chat_id))
    cursor.commit()

# Translate message
def text(update, context):
    
    # Get message
    text_received = update.message.text
    
    # Check the translation
    if (text_received.strip()[:2].lower() == 'jp'):
        text_received = text_received[2:].strip()
        translate_text = translator.translate(text_received,lang_tgt='en').strip()
        conversion = kks.convert(text_received)
        blank = 'Translation: '+ translate_text
        blank = blank + '\n------------------------------------------\n'
        for koto in conversion:
            blank = blank + ("Original message: {} \nHiragana '{}', katakana '{}', romaji: '{}'\n".format(koto['orig'],
                                                                                       koto['hira'], 
                                                                                       koto['kana'], 
                                                                                       koto['hepburn']))
        update.message.reply_text(blank)
    else:
        translate_text = translator.translate(text_received,lang_tgt='ja').strip()
        conversion = kks.convert(translate_text)
        blank = 'Translation: '+ translate_text
        blank = blank + '\n------------------------------------------\n'
        for koto in conversion:
            blank = blank + ("{}: hiragana '{}', katakana '{}', romaji: '{}'\n".format(koto['orig'],
                                                                                       koto['hira'], 
                                                                                       koto['kana'], 
                                                                                       koto['hepburn']))
        update.message.reply_text(blank)

    
def main():
    
    # Bot token
    # Get token
    with open(r'C:...token_bot.txt') as f:
        token = f.readlines()[0] 

    # Create the updater and dispatcher
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher

    # Handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("teachme", teachme))
    dispatcher.add_handler(CommandHandler("join", join))
    dispatcher.add_handler(CommandHandler("leave", leave))


    # Handler translator
    dispatcher.add_handler(MessageHandler(Filters.text, text))

    # Handler error
    dispatcher.add_error_handler(error)

    # Start bot
    updater.start_polling()

    # Run the bot until Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
