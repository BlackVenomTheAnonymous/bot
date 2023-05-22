import re
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler
import logging
import os

TOKEN = '6112737138:AAGVMf3FtbLSsyETATGJR2zslIHohnVlUyQ'

def start(update, context):
    """Handle the /start command and send a welcome message with a photo."""
    # Welcome message with formatting
    message = "🌟 Welcome to the BIN lookup bot! 🌟\n\n"
    message += "This bot helps you retrieve information about BIN (Bank Identification Number) numbers.\n\n"
    message += "Here's how to use the bot:\n"
    message += "1️⃣ Send a BIN number to get its information.\n"
    message += "2️⃣ Use the /help command to see the list of available commands and their usage.\n"
    message += "3️⃣ Enjoy exploring BIN information with the bot! 😊"

    # Send the welcome message with photo
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('welcome_photo.jpg', 'rb'), caption=message)

    # Create an inline button for the /help command
    help_button = InlineKeyboardButton('📚 Help', callback_data='help')

    # Create an inline keyboard markup with the help button
    keyboard = InlineKeyboardMarkup([[help_button]])

    # Send the inline keyboard with the welcome message
    context.bot.send_message(chat_id=update.effective_chat.id, text="You can also use the following command:", reply_markup=keyboard)

def main():
    """Start the Telegram bot."""
    # Set up the Telegram bot updater and dispatcher
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Set up logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # Get the list of command files in the commands folder
    command_files = os.listdir('commands')

    # Import and add command handlers from the command files
    for file in command_files:
        if file.endswith('.py') and file != '__init__.py':
            module_name = file[:-3]
            module = __import__('commands.' + module_name, fromlist=[module_name])
            command_instance = getattr(module, module_name.capitalize())()
            dispatcher.add_handler(command_instance.handler())

    # Add the start command handler separately
    dispatcher.add_handler(CommandHandler("start", start))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
