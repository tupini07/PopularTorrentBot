from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import config
import logging
logging.basicConfig(format='BOT: %(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Not implemented yet")


def countries(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Not implemented yet")


def movies(bot, update, args):
    bot.send_message(chat_id=update.message.chat_id, text="Not implemented yet. but your args are: " + str(args))

def tv(bot, update, args):
    bot.send_message(chat_id=update.message.chat_id, text="Not implemented yet. but your args are: " + str(args))


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I don't understand. Please use the `\help` command to see what functionalities I support.")


####################################


updater = Updater(config.TELEGRAM_BOT_API_KEY)

updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('countries', countries))
updater.dispatcher.add_handler(CommandHandler('movies', movies, pass_args=True))
updater.dispatcher.add_handler(CommandHandler('tv', tv, pass_args=True))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))

updater.start_polling()
updater.idle() ############ Note that this stops execution
