import subprocess
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging

# Define your Telegram bot token here
TOKEN = '6112737138:AAFAQNHx6v3X1dnbCwju03HCFzGiPeroTp8'

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
    message += "/bin [BIN] - Lookup information about a specific BIN number.\n"
    message += "/grab - Execute the grab process.\n\n"
    message += "To perform a BIN lookup, simply send a message with a valid BIN number."

    # Send the help message
    update.message.reply_text(message)

def lookup_bin(update, context):
    """Handle the BIN lookup process."""
    # Extract the BIN number from the user's message
    bin_number = update.message.text.split('/bin ')[1]

    # Perform BIN lookup logic and prepare the response message
    # ...

def grab_command(update, context):
    """Handle the /grab command and perform the grab process."""
    # Execute the Node.js script
    result = subprocess.run(["node", "grab_script.js"], capture_output=True, text=True)

    if result.returncode == 0:
        # Script execution was successful
        output = result.stdout
        update.message.reply_text(output)
    else:
        # Script execution encountered an error
        error = result.stderr
        update.message.reply_text(f"An error occurred: {error}")

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
    dispatcher.add_handler(CommandHandler("grab", grab_command))

    # Start the bot
    updater.start_polling()
    print("Bot started!")

    # Enable logging for debugging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

if __name__ == '__main__':
    main()
