__author__ = "jgrondier"
__copyright__ = "Copyright 2017"

import configparser
import logging
import re
from uuid import uuid4

from Pymoe import Anilist
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater, InlineQueryHandler
from telegram.ext.dispatcher import run_async

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
conf = configparser.ConfigParser()
conf.read("config")

instance = Anilist()

token = conf['DEFAULT']['TOKEN']

url = {
    'anime': "https://anilist.co/anime",
    'manga': "https://anilist.co/manga"
}


@run_async
def inlinequery(bot, update):
    query = update.inline_query.query
    results = list()

    animes = instance.search.anime(query)['data']['Page']['media']

    print([anime['title'] for anime in animes])

    for anime in animes:
        t = "{}/{}".format(url['anime'], anime['id'])

        results.append(InlineQueryResultArticle(id=uuid4(),
                                                title=anime['title']['romaji'],
                                                input_message_content=InputTextMessageContent(t),
                                                url=t,
                                                thumb_url=anime['coverImage']['large'],
                                                description=anime['title']['english']))

    update.inline_query.answer(results)

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
    dp.add_handler(InlineQueryHandler(inlinequery))
    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
