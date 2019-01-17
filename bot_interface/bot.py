import helper
import sys
import logging
import datetime

import textwrap
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

sys.path.insert(0, '..')
import keys

logging.basicConfig(format='BOT: %(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def help_c(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text=textwrap.dedent("""
                     Not implemented yet
                     """))


def about(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text=textwrap.dedent("""
                    Not implemented yet
                    """))


def list_categories(bot, update):
    msg = helper.get_supported_categories()

    if type(msg) == list:
        msg = helper.join_list_into_message(msg)

    bot.send_message(chat_id=update.message.chat_id,
                     text=msg)


def movies(bot, update, args):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Not implemented yet. but your args are: " + str(args))


def tv(bot, update, args):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Not implemented yet. but your args are: " + str(args))


def music(bot, update, args):
    pass


def games(bot, update, args):
    pass


def all_c(bot, update, args):
    pass


def ebooks(bot, update, args):
    pass


def software(bot, update, args):
    pass


def record_of_categories_on(bot, update, args):
    try:
        date = args[0]
        date = [int(x) for x in date.split("-")]
        date = datetime.date(*date)

    except Exception:
        bot.send_message(chat_id=update.message.chat_id,
                     text="You need to specify a date and it should have the following format: YYYY-MM-DD")
        return
    
    msg = helper.get_record_of_categories_on_date(str(date))

    if type(msg) == list and len(msg) > 0:
        msg = helper.join_list_into_message(msg)

    bot.send_message(chat_id=update.message.chat_id,
                     text=msg)



def dates_in_record(bot, update, args):
    try:
        limit = int(args[0]) 
        limit = limit if limit > 0 else 15
    except ValueError:
        limit = 15

    msg = helper.get_dates_in_record(limit)

    if type(msg) == list and len(msg) > 0:
        msg = helper.join_list_into_message(msg)

    bot.send_message(chat_id=update.message.chat_id,
                     text=msg)


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="I don't understand. Please use the `\\help` command to see what functionalities I support.")


####################################


updater = Updater(keys.TELEGRAM_BOT_API_KEY)

updater.dispatcher.add_handler(CommandHandler('help', help_c))
updater.dispatcher.add_handler(
    CommandHandler('list-categories', list_categories))
updater.dispatcher.add_handler(CommandHandler('about', about))

updater.dispatcher.add_handler(
    CommandHandler('movies', movies, pass_args=True))
updater.dispatcher.add_handler(CommandHandler('tv-series', tv, pass_args=True))
updater.dispatcher.add_handler(CommandHandler('music', music, pass_args=True))
updater.dispatcher.add_handler(CommandHandler('games', games, pass_args=True))
updater.dispatcher.add_handler(CommandHandler('all', all_c, pass_args=True))
updater.dispatcher.add_handler(
    CommandHandler('ebooks', ebooks, pass_args=True))
updater.dispatcher.add_handler(CommandHandler(
    'software', software, pass_args=True))

updater.dispatcher.add_handler(CommandHandler(
    'record-of-categories-on', record_of_categories_on, pass_args=True))

updater.dispatcher.add_handler(CommandHandler(
    'dates-in-record', dates_in_record, pass_args=True))


updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))

updater.start_polling()
updater.idle()  # Note that this stops execution

