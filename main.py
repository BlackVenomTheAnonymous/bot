import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Define your bot token
TOKEN = '6112737138:AAG9lqNyne9byVJWUXZYloGHstzEJ6NcrcM'

# Create an instance of the Updater class
updater = Updater(TOKEN, use_context=True)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher


def start(update, context):
    """Send a welcome message when the command /start is issued."""
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! I'm your bot. Send /help for assistance.")


def help_command(update, context):
    """Send a help message when the command /help is issued."""
    help_text = "You can use the following commands:\n\n"
    help_text += "/start - Start the bot\n"
    help_text += "/help - Display this help message\n"
    help_text += "/bin - Lookup information about a BIN number\n"
    help_text += "/grab - Process a Stripe link\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)


def lookup_bin(update, context):
    """Handle the BIN lookup process."""
    # Extract the BIN number from the user's message
    bin_number = update.message.text.split('/bin', 1)[-1].strip()

    # Perform BIN lookup using the obtained number
    bin_data = perform_bin_lookup(bin_number)

    if bin_data:
        message = f"🔍 BIN Lookup Result:\n\n"
        message += f"💳 Brand: {bin_data['brand']}\n"
        message += f"🏦 Bank: {bin_data['bank']}\n"
        message += f"🌍 Country: {bin_data['country']}\n"
        message += f"🔒 Type: {bin_data['type']}"
        update.message.reply_text(message)
    else:
        update.message.reply_text("❌ Failed to lookup BIN information.")


def perform_bin_lookup(bin_number):
    """Perform the BIN lookup using an API."""
    # Make a request to the BIN lookup API with the provided BIN number
    response = requests.get(f"https://api.example.com/bin/{bin_number}")

    if response.status_code == 200:
        bin_data = response.json()
        return bin_data
    else:
        return None


def process_stripe_link(update, context):
    """Process the link provided by the user."""
    # Get the link from the user's input
    link = update.message.text.split('/grab', 1)[-1].strip()

    # Process the link based on its type
    if link.startswith('https://checkout.stripe.com/') or link.startswith('https://stripe.com/payments/'):
        stripe_details = grab_stripe_checkout_details(link)
        if stripe_details:
            message = "🔍 Stripe Checkout Details:\n\n"
            message += f"📧 Email: {stripe_details['email']}\n"
            message += f"🆔 Session ID: {stripe_details['session_id']}\n"
            message += f"💲 Amount Due: {stripe_details['amount_due']}\n"
            message += f"💱 Currency: {stripe_details['currency']}\n"
            message += f"🔑 PK: {stripe_details['pk']}"
            update.message.reply_text(message)
        else:
            update.message.reply_text("❌ Failed to grab details from the link.")
    else:
        update.message.reply_text("ℹ️ Link type not supported.")


def grab_stripe_checkout_details(link):
    """Grab the Stripe checkout details from the provided link."""
    # Make a request to grab the Stripe details using the link
    response = requests.get(f"https://api.example.com/grab/{link}")

    if response.status_code == 200:
        stripe_details = response.json()
        return stripe_details
    else:
        return None


# Register the command handlers
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help_command))
dispatcher.add_handler(CommandHandler('bin', lookup_bin))
dispatcher.add_handler(CommandHandler('grab', process_stripe_link))


def main():
    """Start the bot."""
    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process is stopped
    updater.idle()


if __name__ == '__main__':
    main()
