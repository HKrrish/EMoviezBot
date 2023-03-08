import os
import re
from os import environ

from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from helper.utils import extract_user, get_file_id, get_poster, last_online
import time
from datetime import datetime
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", "<b>🎬 Title:</b> <a href={url}>{title}</a> [{year}] —<b>{kind}</b>\n\n<b>📆 Release:</b> <a href={url}/releaseinfo>{release_date}</a>\n<b>🌟 Rating:</b> <a href={url}/ratings>{rating} / 10</a>\n(based on <code>{votes}</code> user ratings.)\n\n<b>🎭 Genres:</b> #{genres}\n<b>📀 Runtime:</b> <code>{runtime} minutes</code>\n\n<b>☀️ Languages:</b> #{languages}\n<b>🌎 Country of Origin:</b> #{countries}\n<b>🎥 Director:</b> {director}\n\n<b><a href='https://t.me/+q9NMdy0rY10zZWZl'>© IMDb (Series & Movie) Studio</a></b>\n\n<b>✍️ Note:</b> <s>This message will be Auto-deleted after 10 hours to avoid copyright issues.</s>")

@Client.on_message(filters.command("imdb"))
async def imdb_search(client, message):
    if ' ' in message.text:
        k = await message.reply('`Searching...`')
        r, title = message.text.split(None, 1)
        movies = await get_poster(title, bulk=True)
        if not movies:
            return await message.reply("No results Found")
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{movie.get('title')} - {movie.get('year')}",
                    callback_data=f"imdb#{movie.movieID}",
                )
            ]
            for movie in movies
        ]
        await k.edit('Here is what i found on IMDb', reply_markup=InlineKeyboardMarkup(btn))
    else:
        await message.reply('Give me a movie / series Name')

@Client.on_callback_query(filters.regex('^imdb'))
async def imdb_callback(bot: Client, quer_y: CallbackQuery):
    i, movie = quer_y.data.split('#')
    imdb = await get_poster(query=movie, id=True)
    btn = [
            [
                InlineKeyboardButton(
                    text=f"{imdb.get('title')} - {imdb.get('year')}",
                    url=imdb['url'],
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"Channel",
                    url="https://t.me/The_Entertainment"
                )
            ],
        ]
    message = quer_y.message.reply_to_message or quer_y.message
    if imdb:
        caption = IMDB_TEMPLATE.format(
            title = imdb['title'],
            votes = imdb['votes'],
            aka = imdb["aka"],
            seasons = imdb["seasons"],
            box_office = imdb['box_office'],
            localized_title = imdb['localized_title'],
            kind = imdb['kind'],
            imdb_id = imdb["imdb_id"],
            cast = imdb["cast"],
            runtime = imdb["runtime"],
            countries = imdb["countries"],
            certificates = imdb["certificates"],
            languages = imdb["languages"],
            director = imdb["director"],
            writer = imdb["writer"],
            producer = imdb["producer"],
            composer = imdb["composer"],
            cinematographer = imdb["cinematographer"],
            music_team = imdb["music_team"],
            distributors = imdb["distributors"],
            release_date = imdb['release_date'],
            year = imdb['year'],
            genres = imdb['genres'],
            poster = imdb['poster'],
            plot = imdb['plot'],
            rating = imdb['rating'],
            url = imdb['url'],
            **locals()
        )
    else:
        caption = "No Results"
    if imdb.get('poster'):
        try:
            await quer_y.message.reply_photo(photo=imdb['poster'], caption=caption, reply_markup=InlineKeyboardMarkup(btn))
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg")
            await quer_y.message.reply_photo(photo=poster, caption=caption, reply_markup=InlineKeyboardMarkup(btn))
        except Exception as e:
            logger.exception(e)
            await quer_y.message.reply(caption, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=False)
        await quer_y.message.delete()
    else:
        await quer_y.message.edit(caption, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=False)
    await quer_y.answer()
