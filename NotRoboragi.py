__author__ = "jgrondier"
__copyright__ = "Copyright 2017"

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import re, pprint, configparser
from Pymoe import Mal, Anilist
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
conf = configparser.ConfigParser()
conf.read("config")

instance = Anilist()

token = conf['DEFAULT']['TOKEN']

url = {
    'anime': "https://anilist.co/anime",
    'manga': "https://anilist.co/manga"
}


def format_caption(url, medium):
    english_title, romaji_title = '', ''

    try:
        english_title = medium['title']['english']
    except KeyError:
        pass
    try:
        romaji_title = medium['title']['romaji']
    except KeyError:
        pass

    caption = "*{}*\n_{}_ \n{}/{}/".format(romaji_title, english_title, url, medium['id'])

    return caption


def search(bot, update):
    temp_anime = re.search(r'\{\{(.*?)\}\}', update.message.text)

    print(update)

    if temp_anime is not None:
        anime = instance.search.anime(temp_anime.group(1))['data']['Page']['media'][0]

        update.message.reply_photo(photo=anime['coverImage']['large'],
                                   caption=format_caption(url['anime'], anime),
                                   parse_mode="markdown")
        return

    temp_manga = re.search(r'\[\[(.*?)\]\]', update.message.text)

    if temp_manga is not None:
        manga = instance.search.manga(temp_manga.group(1))['data']['Page']['media'][0]
        update.message.reply_photo(photo=manga['coverImage']['large'],
                                   caption=format_caption(url['manga'], manga),
                                   parse_mode="markdown")
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
