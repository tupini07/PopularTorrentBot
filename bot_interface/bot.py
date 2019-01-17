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


def categories_handler(category):

    def telegram_handle(bot, update, args):
        date = args[0] if len(args) > 0 else None
        bot.send_message(chat_id=update.message.chat_id,
                         text=helper.get_information_for_category_on_date(category, date))
    return telegram_handle


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
    except Exception:
        limit = 15

    msg = helper.get_dates_in_record(limit)

    if type(msg) == list and len(msg) > 0:
        msg = helper.join_list_into_message(msg, joiner=">")

    bot.send_message(chat_id=update.message.chat_id,
                     text=msg)


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="I don't understand. Please use the `\\help` command to see what functionalities I support.")


####################################


updater = Updater(keys.TELEGRAM_BOT_API_KEY)

updater.dispatcher.add_handler(CommandHandler('help', help_c))
updater.dispatcher.add_handler(
    CommandHandler('list_categories', list_categories))
updater.dispatcher.add_handler(CommandHandler('about', about))

updater.dispatcher.add_handler(
    CommandHandler('movies', categories_handler("movies"), pass_args=True))

updater.dispatcher.add_handler(CommandHandler(
    'tv_series', categories_handler("TV-series"), pass_args=True))

updater.dispatcher.add_handler(CommandHandler(
    'music', categories_handler("music"), pass_args=True))

updater.dispatcher.add_handler(CommandHandler(
    'games', categories_handler("games"), pass_args=True))

updater.dispatcher.add_handler(CommandHandler(
    'all', categories_handler("all"), pass_args=True))

updater.dispatcher.add_handler(
    CommandHandler('ebooks', categories_handler("ebooks"), pass_args=True))

updater.dispatcher.add_handler(CommandHandler(
    'software', categories_handler("software"), pass_args=True))

updater.dispatcher.add_handler(CommandHandler(
    'record_of_categories_on', record_of_categories_on, pass_args=True))

updater.dispatcher.add_handler(CommandHandler(
    'dates_in_record', dates_in_record, pass_args=True))


updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))

updater.start_polling()
updater.idle()  # Note that this stops execution
