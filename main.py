# (c) @AbirHasan2005 & Jigar Varma & Hemanta Pokharel & Akib Hridoy

import asyncio
from pyrogram import Client, filters
from pyrogram.errors import QueryIdInvalid, FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, InlineQuery, InlineQueryResultArticle, \
    InputTextMessageContent

from configs import Config
from tool import SearchYTS, SearchAnime, Search1337x, SearchPirateBay

TorrentBot = Client(session_name=Config.SESSION_NAME, api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)
DEFAULT_SEARCH_MARKUP = [
                    [InlineKeyboardButton("🎬Search YTS🎬", switch_inline_query_current_chat="!yts "),
                      InlineKeyboardButton("🔝Go Inline🔝", switch_inline_query="!yts ")],
                    [InlineKeyboardButton("💼Search ThePirateBay💼", switch_inline_query_current_chat="!pb "),
                      InlineKeyboardButton("🔝Go Inline🔝", switch_inline_query="!pb ")],
                    [InlineKeyboardButton("⚡Search 1337x🌀", switch_inline_query_current_chat=""),
                      InlineKeyboardButton("🔝Go Inline🔝", switch_inline_query="")],
                    [InlineKeyboardButton("🌀Search Anime🌀", switch_inline_query_current_chat="!a "),
                     InlineKeyboardButton("🌀GO Inline🌀", switch_inline_query_current_chat="!a ")],
                    [InlineKeyboardButton("🔥💥 Developer 💥🔥", url="https://t.me/omindas")]
                ]


@TorrentBot.on_message(filters.command("start"))
async def start_handler(_, message: Message):
    try:
        await message.reply_text(
            text="🥺Hello, 🔥I am Torrent Search Bot!🇱🇰\n"
                 "💠I can search Torrent Magnetic Links from Inline😇😇.\n\n"
                 "Made by @omindas🔥🔥 Powerd By sdprojectupdates 💠💠🇱🇰",
            disable_web_page_preview=True,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(DEFAULT_SEARCH_MARKUP)
        )
    except FloodWait as e:
        print(f"[{Config.SESSION_NAME}] - Sleeping for {e.x}s")
        await asyncio.sleep(e.x)
        await start_handler(_, message)


@TorrentBot.on_inline_query()
async def inline_handlers(_, inline: InlineQuery):
    search_ts = inline.query
    answers = []
    if search_ts == "":
        answers.append(
            InlineQueryResultArticle(
                title="🔎Search Something ...🔎",
                description="📍Search For Torrents ...📍",
                input_message_content=InputTextMessageContent(
                    message_text="👨‍💻Search for Torrents from Inline👨‍💻!",
                    parse_mode="Markdown"
                ),
                reply_markup=InlineKeyboardMarkup(DEFAULT_SEARCH_MARKUP)
            )
        )
    elif search_ts.startswith("!pb"):
        query = search_ts.split(" ", 1)[-1]
        if (query == "") or (query == " "):
            answers.append(
                InlineQueryResultArticle(
                    title="!pb [text]",
                    description="🔎Search For Torrent in ThePirateBay ...🔎",
                    input_message_content=InputTextMessageContent(
                        message_text="`!pb [text]`\n\🔎nSearch ThePirateBay Torrents from Inline🔎!",
                        parse_mode="Markdown"
                    ),
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✳️Search Again✳️", switch_inline_query_current_chat="!pb ")]])
                )
            )
        else:
            torrentList = await SearchPirateBay(query)
            if not torrentList:
                answers.append(
                    InlineQueryResultArticle(
                        title="🤖No Torrents Found in ThePirateBay🤖!",
                        description=f"🌟Can't find torrents for {query} in ThePirateBay🌟 !!",
                        input_message_content=InputTextMessageContent(
                            message_text=f"🤖No Torrents Found For `{query}` in ThePirateBay🤖 !!",
                            parse_mode="Markdown"
                        ),
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔎Try Again🔎", switch_inline_query_current_chat="!pb ")]])
                    )
                )
            else:
                for i in range(len(torrentList)):
                    answers.append(
                        InlineQueryResultArticle(
                            title=f"{torrentList[i]['Name']}",
                            description=f"Seeders: {torrentList[i]['Seeders']}, Leechers: {torrentList[i]['Leechers']}\nSize: {torrentList[i]['Size']}",
                            input_message_content=InputTextMessageContent(
                                message_text=f"**Category:** `{torrentList[i]['Category']}`\n"
                                             f"**Name:** `{torrentList[i]['Seeders']}`\n"
                                             f"**Size:** `{torrentList[i]['Size']}`\n"
                                             f"**Seeders:** `{torrentList[i]['Seeders']}`\n"
                                             f"**Leechers:** `{torrentList[i]['Leechers']}`\n"
                                             f"**Uploader:** `{torrentList[i]['Uploader']}`\n"
                                             f"**Uploaded on {torrentList[i]['Date']}**\n\n"
                                             f"**Magnet:**\n`{torrentList[i]['Magnet']}`\n\nPowered By @AHToolsBot",
                                parse_mode="Markdown"
                            ),
                            reply_markup=InlineKeyboardMarkup(
                                [[InlineKeyboardButton("🔎Search Again🔎", switch_inline_query_current_chat="!pb ")]])
                        )
                    )
    elif search_ts.startswith("!yts"):
        query = search_ts.split(" ", 1)[-1]
        if (query == "") or (query == " "):
            answers.append(
                InlineQueryResultArticle(
                    title="!yts [text]",
                    description="✳️Search For Torrent in YTS ...✳️",
                    input_message_content=InputTextMessageContent(
                        message_text="`!yts [text]`\n\nSearch YTS Torrents from Inline!",
                        parse_mode="Markdown"
                    ),
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("🔎Search Again🔎", switch_inline_query_current_chat="!yts ")]])
                )
            )
        else:
            torrentList = await SearchYTS(query)
            if not torrentList:
                answers.append(
                    InlineQueryResultArticle(
                        title="✳️No Torrents Found✳️!",
                        description=f"🤖Can't find YTS torrents for {query} !!",
                        input_message_content=InputTextMessageContent(
                            message_text=f"✳️No YTS Torrents Found For `{query}`",
                            parse_mode="Markdown"
                        ),
                        reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton("🔎Try Again🔎", switch_inline_query_current_chat="!yts ")]])
                    )
                )
            else:
                for i in range(len(torrentList)):
                    dl_links = "- " + "\n\n- ".join(torrentList[i]['📩Downloads📩'])
                    answers.append(
                        InlineQueryResultArticle(
                            title=f"{torrentList[i]['Name']}",
                            description=f"Language: {torrentList[i]['Language']}\nLikes: {torrentList[i]['Likes']}, Rating: {torrentList[i]['Rating']}",
                            input_message_content=InputTextMessageContent(
                                message_text=f"**Genre:** `{torrentList[i]['Genre']}`\n"
                                             f"**Name:** `{torrentList[i]['Name']}`\n"
                                             f"**Language:** `{torrentList[i]['Language']}`\n"
                                             f"**Likes:** `{torrentList[i]['Likes']}`\n"
                                             f"**Rating:** `{torrentList[i]['Rating']}`\n"
                                             f"**Duration:** `{torrentList[i]['Runtime']}`\n"
                                             f"**Released on {torrentList[i]['ReleaseDate']}**\n\n"
                                             f"**Torrent Download Links:**\n{dl_links}\n\nPowered By @AHToolsBot",
                                parse_mode="Markdown",
                                disable_web_page_preview=True
                            ),
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔎Search Again🔎", switch_inline_query_current_chat="!yts ")]]),
                            thumb_url=torrentList[i]["Poster"]
                        )
                    )
    elif search_ts.startswith("!a"):
        query = search_ts.split(" ", 1)[-1]
        if (query == "") or (query == " "):
            answers.append(
                InlineQueryResultArticle(
                    title="!a [text]",
                    description="😋Search For Torrents for Anime ...😋",
                    input_message_content=InputTextMessageContent(
                        message_text="`!a [text]`\n\nSearch Anime Torrents from Inline🔎!",
                        parse_mode="Markdown"
                    ),
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("✳️Search Again✳️", switch_inline_query_current_chat="!a ")]])
                )
            )
        else:
            torrentList = await SearchAnime(query)
            if not torrentList:
                answers.append(
                    InlineQueryResultArticle(
                        title="🌟No Anime Torrents Found🌟!",
                        description=f"✳️Can't find Anime torrents for {query} !!",
                        input_message_content=InputTextMessageContent(
                            message_text=f"✳️No Anime Torrents Found For `{query}`",
                            parse_mode="Markdown"
                        ),
                        reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton("🔎Try Again🔎", switch_inline_query_current_chat="!a ")]])
                    )
                )
            else:
                for i in range(len(torrentList)):
                    answers.append(
                        InlineQueryResultArticle(
                            title=f"{torrentList[i]['Name']}",
                            description=f"Seeders: {torrentList[i]['Seeder']}, Leechers: {torrentList[i]['Leecher']}\nSize: {torrentList[i]['Size']}",
                            input_message_content=InputTextMessageContent(
                                message_text=f"**Category:** `{torrentList[i]['Category']}`\n"
                                             f"**Name:** `{torrentList[i]['Name']}`\n"
                                             f"**Seeders:** `{torrentList[i]['Seeder']}`\n"
                                             f"**Leechers:** `{torrentList[i]['Leecher']}`\n"
                                             f"**Size:** `{torrentList[i]['Size']}`\n"
                                             f"**Upload Date:** `{torrentList[i]['Date']}`\n\n"
                                             f"**Magnet:** \n`{torrentList[i]['Magnet']}`\n\nPowered By @AHToolsBot",
                                parse_mode="Markdown"
                            ),
                            reply_markup=InlineKeyboardMarkup(
                                [[InlineKeyboardButton("🔎Search Again🔎", switch_inline_query_current_chat="!a ")]]
                            )
                        )
                    )
    else:
        torrentList = await Search1337x(search_ts)
        if not torrentList:
            answers.append(
                InlineQueryResultArticle(
                    title="✳️No Torrents Found✳️!",
                    description=f"✳️Can't find torrents for {search_ts} !!",
                    input_message_content=InputTextMessageContent(
                        message_text=f"🏜️No Torrents Found For `{search_ts}`",
                        parse_mode="Markdown"
                    ),
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("🔎Try Again🔎", switch_inline_query_current_chat="")]])
                )
            )
        else:
            for i in range(len(torrentList)):
                answers.append(
                    InlineQueryResultArticle(
                        title=f"{torrentList[i]['Name']}",
                        description=f"Seeders: {torrentList[i]['Seeders']}, Leechers: {torrentList[i]['Leechers']}\nSize: {torrentList[i]['Size']}, Downloads: {torrentList[i]['Downloads']}",
                        input_message_content=InputTextMessageContent(
                            message_text=f"**Category:** `{torrentList[i]['Category']}`\n"
                                         f"**Name:** `{torrentList[i]['Name']}`\n"
                                         f"**Language:** `{torrentList[i]['Language']}`\n"
                                         f"**Seeders:** `{torrentList[i]['Seeders']}`\n"
                                         f"**Leechers:** `{torrentList[i]['Leechers']}`\n"
                                         f"**Size:** `{torrentList[i]['Size']}`\n"
                                         f"**Downloads:** `{torrentList[i]['Downloads']}`\n"
                                         f"__Uploaded by {torrentList[i]['UploadedBy']}__\n"
                                         f"__Uploaded {torrentList[i]['DateUploaded']}__\n"
                                         f"__Last Checked {torrentList[i]['LastChecked']}__\n\n"
                                         f"**Magnet:**\n`{torrentList[i]['Magnet']}`\n\nPowered By @AHToolsBot",
                            parse_mode="Markdown"
                        ),
                        reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton("😇Search Again😇", switch_inline_query_current_chat="")]]
                        ),
                        thumb_url=torrentList[i]['Poster']
                    )
                )
    try:
        await inline.answer(
            results=answers,
            cache_time=0
        )
        print(f"[{Config.SESSION_NAME}] - Answered Successfully - {inline.from_user.first_name}")
    except QueryIdInvalid:
        print(f"[{Config.SESSION_NAME}] - Failed to Answer - {inline.from_user.first_name} - Sleeping for 5s")
        await asyncio.sleep(5)
        try:
            await inline.answer(
                results=answers,
                cache_time=0,
                switch_pm_text="Error: Search timed out!",
                switch_pm_parameter="start",
            )
        except QueryIdInvalid:
            print(f"[{Config.SESSION_NAME}] - Failed to Answer Error - {inline.from_user.first_name} - Sleeping for 5s")
            await asyncio.sleep(5)


TorrentBot.run()
