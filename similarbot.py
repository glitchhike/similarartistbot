#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This is a code patchwork
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from db import insert_suggestion
import similar
from config import bot_api

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi!')


def help(bot, update):
    update.message.reply_text('Help!')


def suggest_similar_artist(bot, update):
    print update.message.text
    if update.message.text == '/similarto':
        update.message.reply_text('usage: /similarto artistname')
    else:
        new_similar = similar.find(update.message.text[11:])
        # update.message.reply_text('\n'.join('%s' % i for k, i in enumerate(new_similar[0])))
        if len(new_similar)==1:
           update.message.reply_text(new_similar[0])
        else:
            update.message.reply_photo(new_similar[1], new_similar[0][0])

def record_suggestion(bot, update):
    if ' - ' in update.message.text:
        insert_suggestion(update.message)
        update.message.reply_text('suggestion recorded in the database')
    else:
        update.message.reply_text('usage: /suggest Artist - Album')

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(bot_api)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("similarto", suggest_similar_artist))
    dp.add_handler(CommandHandler("suggest", record_suggestion))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
