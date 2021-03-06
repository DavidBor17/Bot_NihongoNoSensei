#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
import telebot
import xlrd
import random
import pyodbc 
from datetime import datetime

# Get timestamp
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

# Connect the bot
token = '1579262164:AAHttoRJtCtgSlZEe53vv4nIxBTulDfKpFg'
bot = telebot.TeleBot(token)

# Import the vocabulary
teach_voc = pd.read_excel(r'C:\Users\calab\Desktop\VocabJapanese.xls')
teach_voc = teach_voc.fillna('-')

# Connect the database / SQL Server
name = 'DESKTOP-989ACLI\DAVID'
database = 'telegram_bot'

cnxn = pyodbc.connect(driver='{SQL Server}', server= name, database= database,               
               trusted_connection='yes')
cursor = cnxn.cursor()

# Create the initial log
cursor.execute("insert into teach_logs values('{}', '0')".format(dt_string))
cursor.commit()

# Create the message
rand = random.randint(0,len(teach_voc))
teach_1 = 'Let´s learn a new word!.\n'
teach_2 = 'Kanji: {}, Hiragana: {}, Meaning: {}'.format(teach_voc.iloc[rand][3],teach_voc.iloc[rand][4],teach_voc.iloc[rand][5])
teach_full = teach_1 + teach_2

# Import the ids
sql_query = pd.read_sql_query('select distinct ids from club',cnxn)

# Create a log
count = 0

bot.config['api_key'] = token
# Send the message
for i in range(len(sql_query)):
    bot.send_message(chat_id = str(sql_query.ids[i]), text = teach_full)
    count+=1

# Creating a log, how many people got the word
cursor.execute("update teach_logs set numb = '{}' where date = '{}' ".format(str(count),dt_string))
cursor.commit()

