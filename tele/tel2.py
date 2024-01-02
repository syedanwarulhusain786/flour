import telebot
from telebot import types
from settings import *

bot = telebot.TeleBot('6892855782:AAGTkmOKGRBCqNfSfVw4I1HGHNY1ttToTU4')

# Placeholder functions for database interactions
def user_exists(user_id):
    # Implement logic to check if the user exists in the database
    # Return True if user exists, False otherwise
    return False  # Placeholder, replace with actual logic

def get_user_orders(user_id):
    # Implement logic to fetch orders from the database based on user_id
    # Return a list of orders
    return [{'order_id': 1}, {'order_id': 2}]  # Placeholder, replace with actual logic

@bot.message_handler(commands=['start'])
def question(message):
    user_id = message.from_user.id
    print(user_id)
    # Check if user exists in the database
    if user_exists(user_id):
        bot.reply_to(message, f'Welcome To {erp}')
    else:
        bot.reply_to(message, 'You are not registered in our system.')

@bot.message_handler(commands=['login'])
def question(message):
    user_id = message.from_user.id
    # Check if user exists in the database
    if user_exists(user_id):
        markup = types.InlineKeyboardMarkup(row_width=2)
        iron = types.InlineKeyboardButton('1 kn Iron', callback_data='answer_iron')
        cotton = types.InlineKeyboardButton('1 kg cotton', callback_data='answer_cotton')
        same = types.InlineKeyboardButton('same weight', callback_data='answer_same')
        no_answer = types.InlineKeyboardButton('no correct answer', callback_data='no_answer')
        markup.add(iron, cotton, same, no_answer)
        bot.send_message(message.chat.id, 'What is lighter?', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'You need to register before using this command.')

@bot.callback_query_handler(func=lambda call: True)
def answer(callback):
    if callback.message:
        bot.send_message(callback.message.chat.id, 'What is lighter?')

bot.polling()
