import re
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging
import subprocess

TOKEN = '6112737138:AAGCOCrvIyf-4TGqd8Nv3OPhxvqFwFuG4uQ'

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

def lookup_bin(update, context):
    """Handle the BIN lookup process."""
    # Extract the BIN number from the user's message
    bin_number = update.message.text.split('/bin ')[1]

    # Perform BIN lookup using the obtained number
    bin_data = perform_bin_lookup(bin_number)
    
    if bin_data:
        # Prepare the response message with custom formatting and emojis
        message = f"✨ BIN: {bin_number}\n\n"
        message += f"💳 Scheme: {bin_data['scheme']}\n"
        message += f"🏢 Brand: {bin_data['brand']}\n\n"
        message += f"🏦 Bank: {bin_data['bank_name']}\n"
        message += f"📞 Phone: {bin_data['bank_phone']}\n\n"
        message += f"🌍 Country: {bin_data['country_name']} {bin_data['country_emoji']}\n"
        message += f"💰 Currency: {bin_data['currency']}"

        # Create an inline button with custom styling
        button = InlineKeyboardButton('🌐 𓆩𝗫𝗲𝗿𝗿𝗼𝘅𓆪「Zone ↯」 🌐', url='https://t.me/xerrox_army')

        # Create an inline keyboard markup with the button
        keyboard = InlineKeyboardMarkup([[button]])

        # Send the response message with the inline button
        update.message.reply_text(message, reply_markup=keyboard)
    else:
        # BIN lookup failed, send an error message
        update.message.reply_text("❌ BIN lookup failed. Please make sure you entered a valid BIN number.")

def perform_bin_lookup(bin_number):
    """Perform the BIN lookup using the provided BIN number."""
    try:
        # Make a GET request to the BIN lookup API with the BIN number
        response = requests.get(f'https://lookup.binlist.net/{bin_number}')

        # Parse the JSON response
        bin_data = response.json()

        # Extract the relevant information from the response
        scheme = bin_data.get('scheme', 'Unknown')
        brand = bin_data.get('brand', 'Unknown')
        bank_name = bin_data.get('bank', {}).get('name', 'Unknown')
        bank_phone = bin_data.get('bank', {}).get('phone', 'Unknown')
        country_name = bin_data.get('country', {}).get('name', 'Unknown')
        country_emoji = bin_data.get('country', {}).get('emoji', '')
        currency = bin_data.get('country', {}).get('currency', 'Unknown')

        # Create a dictionary with the extracted data
        bin_info = {
            'scheme': scheme,
            'brand': brand,
            'bank_name': bank_name,
            'bank_phone': bank_phone,
            'country_name': country_name,
            'country_emoji': country_emoji,
            'currency': currency
        }

        return bin_info
    except requests.exceptions.RequestException:
        return None

def grab_stripe_details(update, context):
    """Handle the /grab command and grab details from a Stripe checkout link."""
    # Prompt the user to enter the Stripe checkout link
    update.message.reply_text("🔗 Please enter the Stripe checkout link:")

    # Set the bot's next step to handle the user's input
    context.user_data['next_step'] = 'grab_stripe_link'

def process_stripe_link(update, context):
    """Process the Stripe checkout link provided by the user."""
    # Get the Stripe checkout link from the user's input
    stripe_link = update.message.text

    # Grab the details from the Stripe checkout link
    stripe_details = grab_stripe_checkout_details(stripe_link)

    if stripe_details:
        # Prepare the response message with the retrieved details
        message = "🔍 Stripe Checkout Details:\n\n"
        message += f"📧 Email: {stripe_details['email']}\n"
        message += f"🆔 Session ID: {stripe_details['session_id']}\n"
        message += f"💲 Amount Due: {stripe_details['amount_due']}\n"
        message += f"💱 Currency: {stripe_details['currency']}\n"
        message += f"🔑 PK: {stripe_details['pk']}"

        # Send the response message
        update.message.reply_text(message)
    else:
        # Failed to grab details from the Stripe checkout link
        update.message.reply_text("❌ Failed to grab details from the Stripe checkout link.")

def grab_stripe_checkout_details(stripe_link):
    """Grab the details from the provided Stripe checkout link."""
    try:
        # Launch Puppeteer and create a new page
        browser = await puppeteer.launch()
        page = await browser.newPage()

        # Set up request interception
        await page.setRequestInterception(True)

        match_found = False
        pk = None
        urlx = None

        page.on('request', request => {
            if not match_found and request.postData and 'pk' in request.postData:
                regex = r'pk_live_[\w-]+'
                match = re.search(regex, request.postData)
                if match:
                    pk = match.group(0)
                    match_found = True
                    urlx = request.url
                    page.off('request', self)
            request.continue()

        # Go to the Stripe checkout link
        await page.goto(stripe_link)

        # Close the browser
        await browser.close()

        # Return the grabbed details as a dictionary
        return {
            'email': email,
            'session_id': session_id,
            'amount_due': amount_due,
            'currency': currency,
            'pk': pk,
            'urlx': urlx
        }
    except Exception as e:
        print(e)
        return None

def main():
    """Start the Telegram bot."""
    # Set up the Telegram bot updater and dispatcher
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("bin", lookup_bin))
    dispatcher.add_handler(CommandHandler("grab", grab_stripe_details))

    # Add message handler to process the Stripe checkout link
    dispatcher.add_handler(MessageHandler(Filters.text & Filters.regex(r'https?://(?:www\.)?stripe\.com/checkout/.+'), process_stripe_link))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
