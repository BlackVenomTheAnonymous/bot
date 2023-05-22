from telegram.ext import CommandHandler

from commands.help_command import HelpCommand
from commands.bin_command import BinCommand

def add_handlers(dispatcher):
    """Add command handlers to the dispatcher."""
    help_command = HelpCommand()
    bin_command = BinCommand()

    dispatcher.add_handler(help_command.handler())
    dispatcher.add_handler(bin_command.handler())
