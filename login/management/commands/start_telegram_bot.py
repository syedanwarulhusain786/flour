# login/management/commands/start_telegram_bot.py

from django.core.management.base import BaseCommand
from django.conf import settings
from login.models import CustomUser
from sales.models import *

from telebot import TeleBot, types

class Command(BaseCommand):
    help = 'Start the Telegram bot'

    def handle(self, *args, **options):
        bot = TeleBot(settings.TELEGRAM_BOT_TOKEN)

        def is_user_authenticated(user_id):
            try:
                CustomUser.objects.get(telegram_id=user_id)
                return True
            except CustomUser.DoesNotExist:
                return False

        # Define states
        STATE_START = "start"
        STATE_VIEW_ALL_ORDERS = "view_all_orders"
        STATE_VIEW_ORDER_BY_NUMBER = "view_order_by_number"

        # Dictionary to store user states
        user_states = {}

        def send_menu(user_id):
            markup = types.InlineKeyboardMarkup(row_width=3)
            markup.add(types.InlineKeyboardButton("View All Orders", callback_data='view_all_orders'))
            markup.add(types.InlineKeyboardButton("View Order By Number", callback_data='view_order_by_number'))
            markup.add(types.InlineKeyboardButton("Logout", callback_data='logout'))
            bot.send_message(user_id, 'Please choose an option:', reply_markup=markup)

        def view_all_orders(user_id):
            # Add logic to view all orders or provide further options
            bot.send_message(user_id, "Here are all your orders or provide further options.")
            markup = types.InlineKeyboardMarkup(row_width=2)
            sales=Sales.objects.all()
            for sale in sales:
                markup.add(types.InlineKeyboardButton(f"Order No {sale.sale_number}", callback_data=f'Order No {sale.sale_number}'))
            bot.send_message(user_id, 'Please choose an Order No:', reply_markup=markup)
            
        def view_order_by_number(user_id):
            # Prompt the user to enter the order number
            bot.send_message(user_id, "Please enter the order number:")
            # Update user state
            user_states
        def handle_logout(user_id):
            # Add logout logic here
            bot.send_message(user_id, "You have been logged out.")

        @bot.message_handler(commands=['start'])
        def start(message):
            user_id = message.from_user.id
            if is_user_authenticated(user_id):
                send_menu(user_id)
                # Set the initial state
                user_states[user_id] = STATE_START
            else:
                bot.reply_to(message, "You are not authenticated. Please register first.")

        @bot.callback_query_handler(func=lambda call: True)
        def handle_callback_query(call):
            user_id = call.from_user.id
            if is_user_authenticated(user_id):
                action = call.data
                if action == "view_all_orders":
                    user_states[user_id] = STATE_VIEW_ALL_ORDERS
                    view_all_orders(user_id)
                elif action == "view_order_by_number":
                    user_states[user_id] = STATE_VIEW_ORDER_BY_NUMBER
                    view_order_by_number(user_id)
                elif action == "logout":
                    handle_logout(user_id)
                else:
                    bot.send_message(user_id, "Invalid option. Please choose a valid option.")
            else:
                bot.send_message(user_id, "You are not authenticated. Please register first.")

        @bot.message_handler(func=lambda message: True)
        def handle_messages(message):
            user_id = message.from_user.id
            state = user_states.get(user_id, STATE_START)

            if is_user_authenticated(user_id):
                if state == STATE_VIEW_ORDER_BY_NUMBER:
                    # Handle user input when in the "view_order_by_number" state
                    order_number = message.text
                    # Add logic to handle the provided order number
                    bot.send_message(user_id, f"Viewing order details for order number: {order_number}")
                    # Reset the state after processing the input
                    user_states[user_id] = STATE_START
                else:
                    bot.send_message(user_id, "Invalid option. Please choose a valid option.")
            else:
                bot.send_message(user_id, "You are not authenticated. Please register first.")
        bot.polling(none_stop=True)
    # Add more message handlers
