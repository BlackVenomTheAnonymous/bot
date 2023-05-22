from telegram.ext import CommandHandler

class Bin:
    def handler(self):
        return CommandHandler('bin', self.lookup_bin)

    def lookup_bin(self, update, context):
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
