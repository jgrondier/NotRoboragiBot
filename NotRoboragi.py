__author__ = "jgrondier"
__copyright__ = "Copyright 2017"

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import re, pprint, configparser
from Pymoe import Mal

conf = configparser.ConfigParser()
conf.read("config")

mal_username = conf['DEFAULT']['MAL_USERNAME']
mal_password = conf['DEFAULT']['MAL_PASSWORD']

instance = Mal(mal_username, mal_password)

token = conf['DEFAULT']['TOKEN']


def search(bot, update):
    temp_anime = re.search(r'\{\{(.*?)\}\}', update.message.text)

    if temp_anime is not None:
        anime = instance.anime.search(temp_anime.group(1))[0]
        update.message.reply_text("https://myanimelist.net/anime/{}".format(anime.id))
        return

    temp_manga = re.search(r'\[\[(.*?)\]\]', update.message.text)

    if temp_manga is not None:
        manga = instance.manga.search(temp_manga.group(1))[0]
        update.message.reply_text("https://myanimelist.net/manga/{}".format(manga.id))
        return


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token)

    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text, search))

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
