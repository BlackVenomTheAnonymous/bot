from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# ...

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
