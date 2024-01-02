import telebot
from telebot import types
from settings import *

bot=telebot.TeleBot('6892855782:AAGTkmOKGRBCqNfSfVw4I1HGHNY1ttToTU4')

@bot.message_handler(commands=['start'])
def question(message):
    bot.reply_to(message,f'Welcome To {erp}')
    
    
    


@bot.message_handler(commands=['login'])
def question(message):
    markup=types.InlineKeyboardMarkup(row_width=2)
    iron=types.InlineKeyboardButton('1 kn Iron',callback_data='answer_iron')
    cotton=types.InlineKeyboardButton('1 kg cotton',callback_data='answer_cotton')
    same=types.InlineKeyboardButton('same weight',callback_data='answer_same')
    no_answer=types.InlineKeyboardButton('no correct answer',callback_data='no_answer')
    markup.add(iron,cotton,same,no_answer)
    bot.send_message(message.chat.id,'what is lighter?',reply_markup=markup)
    

@bot.callback_query_handler(func=lambda call:True)
def answer(callback):
    if callback.message:
        bot.send_message(callback.message.chat.id,'what is lighter?')
        
    
    
bot.polling()