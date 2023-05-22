from telegram.ext import CommandHandler

class HelpCommand:
    def handler(self):
        return CommandHandler("help", self.help)

    def help(self, update, context):
        """Handle the /help command and provide the list of available commands."""
        # Help message with available commands
        message = "📚 Here are the available commands:\n\n"
        message += "/start - Start the bot and get a welcome message.\n"
        message += "/help - View the list of available commands and their usage.\n"
        message += "/bin [BIN] - Lookup information about a specific BIN number.\n\n"
        message += "To perform a BIN lookup, simply send a message with a valid BIN number."

        # Send the help message
        update.message.reply_text(message)
