import sys
import logging
import datetime

import bot_helper as h

import textwrap
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

sys.path.insert(0, '..')
import keys

logging.basicConfig(format='BOT: %(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def help_c(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text=textwrap.dedent("""
                     Below are the commands that this bot understands 
                     
                     All category commands (`/movies`, `/tv_series`, `/ebooks`, `/music`, `/games`, `/software`, and `/all`) accept an optional `date` \
                     which must be given in the following format `YYYY-MM-DD`. If no date is provided then torrent information for this categories is \
                     provided for `today`. If a date is provided then the bot will check the database to see if there is an entry for that date and \
                     category, if yes this is returned to you, but if no entry is found then an error message will be displayed.

                     This bot uses `pastebin` to save the data, but sometimes pastebin will require a user to fill up a catpcha to see the content of a \
                     paste. In these cases the bot will not be able to read the data automatically so the URL will be provided to you directly and \
                     you'll have to open it and fill the captcha manually if you want to see the content. 


                     Commands:

                     /help - prints this help message

                     /list_categories - lists the torrent categories that the bot supports

                     /movies (optional: date) - get top movies for today or a specific date

                     /tv_series (optional: date) - get top tv-series for today or a specific date

                     /ebooks (optional: date) - get top ebooks for today or a specific date

                     /music (optional: date) - get top music for today or a specific date

                     /games (optional: date) - get top games for today or a specific date
                     
                     /software (optional: date) - get top software for today or a specific date
                     
                     /all (optional: date) - get top torrents for all categories, for today or a specific date

                     /dates_in_record - get a list of dates for which we have information 

                     /record_of_categories_on - get the categories we have information about for a specific date 

                     /about - prints information about this bot
                     """))


def about(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text=textwrap.dedent("""
                    This bot was created as the final project for the course of Introduction to Service Design and Engineering course at UNITN.

                    It uses `torrentapi` to get torrent information, `OMDb API` to get movie and TV series information, and `Pastebin` to save torrent information.

                    This bot is open source and the code can be found here: https://github.com/tupini07/PopularTorrentBot
                    """))


def list_categories(bot, update):
    msg = h.get_supported_categories()

    if type(msg) == list:
        msg = h.join_list_into_message(msg)

    bot.send_message(chat_id=update.message.chat_id,
                     text=msg)


def categories_handler(category):

    def telegram_handle(bot, update, args):
        date = args[0] if len(args) > 0 else None
        bot.send_message(chat_id=update.message.chat_id,
                         text=h.get_information_for_category_on_date(category, date))
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

    msg = h.get_record_of_categories_on_date(str(date))

    if type(msg) == list and len(msg) > 0:
        msg = h.join_list_into_message(msg)

    bot.send_message(chat_id=update.message.chat_id,
                     text=msg)


def dates_in_record(bot, update, args):
    try:
        limit = int(args[0])
        limit = limit if limit > 0 else 15
    except Exception:
        limit = 15

    msg = h.get_dates_in_record(limit)

    if type(msg) == list and len(msg) > 0:
        msg = h.join_list_into_message(msg, joiner=">")

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
