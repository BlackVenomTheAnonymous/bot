# -*- coding: utf-8 -*-
import re
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Define your Telegram bot token here
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
    button = InlineKeyboardButton('🌐 𓆩𝗫𝗲𝗿𝗿𝗼𝘅𓆪「Zone ↯」 🌐', url='https://t.me/xerrox_army')

    # Create an inline keyboard markup with the help button
    button = InlineKeyboardButton('🌐 𓆩𝗫𝗲𝗿𝗿𝗼𝘅𓆪「Zone ↯」 🌐', url='https://t.me/xerrox_army')

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

def lookup_bin(update, context):
    """Handle the BIN lookup process."""
    # Extract the BIN number from the user's message
    bin_number = update.message.text.split('/bin ')[1]

    # Construct the API URL with the provided BIN number
    url = "https://lookup.binlist.net/" + bin_number

    # Set the headers with the desired Accept-Version
    headers = {'Accept-Version': '3'}

    # Send a GET request to the API
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Parse the JSON response
        bin_data = response.json()

        # Extract the relevant information
        scheme = bin_data.get('scheme', 'N/A')
        brand = bin_data.get('brand', 'N/A')
        bank_name = bin_data['bank'].get('name', 'N/A')
        bank_phone = bin_data['bank'].get('phone', 'N/A')
        country_name = bin_data['country'].get('name', 'N/A')
        country_emoji = bin_data['country'].get('emoji', 'N/A')
        currency = bin_data['country'].get('currency', 'N/A')

        # Prepare the response message with custom formatting and emojis
        message = f"✨ BIN: {bin_number}\n\n"
        message += f"💳 Scheme: {scheme}\n"
        message += f"🏢 Brand: {brand}\n\n"
        message += f"🏦 Bank: {bank_name}\n"
        message += f"📞 Phone: {bank_phone}\n\n"
        message += f"🌍 Country: {country_name} {country_emoji}\n"
        message += f"💰 Currency: {currency}"

        # Create an inline button with custom styling
        button = InlineKeyboardButton('🌐 𓆩𝗫𝗲𝗿𝗿𝗼𝘅𓆪「Zone ↯」 🌐', url='https://t.me/xerrox_army')

        # Create an inline keyboard markup with the button
        keyboard = InlineKeyboardMarkup([[button]])

        # Reply to the user with the text message
        update.message.reply_text(message, reply_markup=keyboard)
    else:
        update.message.reply_text("Sorry, an error occurred while looking up the BIN. Please try again later.")

def process_number(update, context):
    """Handle random number messages and trigger BIN lookup."""
    # Extract the number from the user's message
    number = re.findall(r'\d+', update.message.text)
    if number:
        bin_number = number[0]
        # Perform BIN lookup using the obtained number
        lookup_bin(update, context)

def main():
    # Create the Telegram updater and dispatcher
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Register the command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("bin", lookup_bin))

    # Register the message handler to process random number messages
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), process_number))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
