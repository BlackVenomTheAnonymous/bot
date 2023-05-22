import re
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os

TOKEN = '6112737138:AAGVMf3FtbLSsyETATGJR2zslIHohnVlUyQ'

def start(update, context):
    """Handle the /start command and send a welcome message."""
    # Welcome message with formatting
    message = "🌟 Welcome to the BIN lookup bot! 🌟\n\n"
    message += "This bot helps you retrieve information about BIN (Bank Identification Number) numbers.\n\n"
    message += "Here's how to use the bot:\n"
    message += "1️⃣ Send a BIN number to get its information.\n"
    message += "2️⃣ Use the /help command to see the list of available commands and their usage.\n"
    message += "3️⃣ Enjoy exploring BIN information with the bot! 😊"

    # Create an inline button for the /help command
    help_button = InlineKeyboardButton('📚 Help', callback_data='help')

    # Create an inline keyboard markup with the help button
    keyboard = InlineKeyboardMarkup([[help_button]])

    # Send the welcome message with image and inline button
    context.bot.send_photo(chat_id=update.effective_chat.id, photo='https://i.ibb.co/GMCc1VV/XXX.jpg', caption=message, reply_markup=keyboard)

def help_command(update, context):
    """Handle the /help command and provide the list of available commands."""
    # Help message with available commands
    message = "📚 Here are the available commands:\n\n"
    message += "/start - Start the bot and get a welcome message.\n"
    message += "/help - View the list of available commands and their usage.\n"
    message += "/bin [BIN] - Lookup information about a specific BIN number.\n\n"
    message += "To perform a BIN lookup, simply send a message with a valid BIN number."

    # Send the help message
    update.message.reply_text(message)

def main():
    """Start the Telegram bot."""
    # Set up the Telegram bot updater and dispatcher
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register the command handlers from the 'commands' folder
    commands_folder = 'commands'
    for filename in os.listdir(commands_folder):
        if filename.endswith('.py'):
            module_name = filename[:-3]  # Remove the '.py' extension
            module = __import__(f'{commands_folder}.{module_name}', fromlist=[module_name])
            command_class = getattr(module, module_name.capitalize())
            command_instance = command_class()
            dispatcher.add_handler(command_instance.handler())

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
