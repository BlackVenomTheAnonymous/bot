# -*- coding: utf-8 -*-
import re
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

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

    # Inline keyboard button
    button = InlineKeyboardButton('🌐 𓆩𝗫𝗲𝗿𝗿𝗼𝘅𓆪「Zone ↯」 🌐', url='https://t.me/xerrox_army')

    # Create an inline keyboard with the button
    keyboard = InlineKeyboardMarkup([[button]])

    # Send the welcome message with image and inline keyboard
    context.bot.send_photo(chat_id=update.effective_chat.id, photo='https://i.ibb.co/GMCc1VV/XXX.jpg', caption=message, reply_markup=keyboard)


def help_command(update, context):
    """Handle the /help command and provide the list of available commands."""
    # Help message with available commands
    message = "📚 Here are the available commands:\n\n"
    message += "/start - Start the bot and get a welcome message.\n"
    message += "/help - View the list of available commands and their usage.\n"
    message += "/bin [BIN] - Lookup information about a specific BIN number.\n\n"
    message += "To perform a BIN lookup, simply send a message with a valid BIN number."

    # Inline keyboard button
    button = InlineKeyboardButton('🌐 𓆩𝗫𝗲𝗿𝗿𝗼𝘅𓆪「Zone ↯」 🌐', url='https://t.me/xerrox_army')

    # Create an inline keyboard with the button
    keyboard = InlineKeyboardMarkup([[button]])

    # Send the help message with image and inline keyboard
    context.bot.send_photo(chat_id=update.effective_chat.id, photo='https://gifdb.com/images/file/dark-anime-sukuna-jujutsu-kaisen-q0s31n15yngza4mf.gif', caption=message, reply_markup=keyboard)


def lookup_bin(update, context):
    """Handle the /bin command and perform BIN lookup."""
    # Extract the BIN number from the user's message
    message_text = update.message.text
    bin_number = re.findall(r'\d+', message_text)

    if not bin_number:
        # Guide the user on how to use the /bin command
        message = "To perform a BIN lookup, use the /bin command followed by a valid BIN number.\n\n"
        message += "Example: /bin 123456"

        update.message.reply_text(message)
        return

    bin_number = bin_number[0]

    # Construct the API URL with the provided BIN number
    url = f"https://lookup.binlist.net/{bin_number}"

    # Send a GET request to the API
    response = requests.get(url)

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
        message = f"✨ BIN: `{bin_number}`\n\n"
        message += f"💳 Scheme: `{scheme}`\n"
        message += f"🏷️ Brand: `{brand}`\n"
        message += f"🏦 Bank: `{bank_name}`\n"
        message += f"📞 Bank Phone: `{bank_phone}`\n"
        message += f"🌍 Country: `{country_name} {country_emoji}`\n"
        message += f"💰 Currency: `{currency}`"

        # Create a InlineKeyboardMarkup with the button
        button = InlineKeyboardButton('🌐 𓆩𝗫𝗲𝗿𝗿𝗼𝘅𓆪「Zone ↯」 🌐', url='https://t.me/xerrox_army')
        keyboard = InlineKeyboardMarkup([[button]])

        # Send the response message with monospace formatting and GIF
        response_message = f"*{message}*"  # Monospace formatting for the message
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo='https://gifdb.com/images/file/dark-anime-mattis-dovier-animation-jlbiiyihz0wn8ij0.gif',
            caption=response_message,
            parse_mode='Markdown',
            reply_markup=keyboard
        )
    else:
        # Handle API request errors
        update.message.reply_text("An error occurred while performing the BIN lookup. Please try again later.")


def main():
    """Run the bot."""
    # Create the Updater and pass it your bot's token
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('bin', lookup_bin))
    dispatcher.add_handler(MessageHandler(Filters.command, help_command))  # Handle unknown commands

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
