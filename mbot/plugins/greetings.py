"""MIT License

Copyright (c) 2022 Daniel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from datetime import datetime
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from pyrogram.raw.functions import Ping
from mbot import LOG_GROUP, OWNER_ID, SUDO_USERS, Mbot,AUTH_CHATS
from os import execvp,sys
from motor.motor_asyncio import AsyncIOMotorClient
from Script import script

Dbclient = AsyncIOMotorClient('mongodb+srv://spotify:spotify@cluster0.m0osiez.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
Cluster = Dbclient['Cluster0']
Data = Cluster['users']
LOG_CHANNEL = int(-1002211141582)


@Mbot.on_message(filters.command("start"))
async def start(client,message):
    reply_markup = [[
        InlineKeyboardButton(
            text="Updates Channel", url="https://t.me/Ak_spotify_updates"),
        InlineKeyboardButton(
            text="Owner",
            url="https://t.me/HELL_GaM"),
        InlineKeyboardButton(text="Help",callback_data="helphome")
        ],
        [
            InlineKeyboardButton(text="Support",
            url="https://t.me/HELL_GaM"),
        ]]
    user_id = message.from_user.id 
    bot_name = 'rebakah'
    if not await Data.find_one({'id': user_id}): await Data.insert_one({'id': user_id}) 
    await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention, message.from_user.username, bot_name))
    if LOG_GROUP:

        invite_link = await client.create_chat_invite_link(chat_id=(int(LOG_GROUP) if str(LOG_GROUP).startswith("-100") else LOG_GROUP))
        reply_markup.append([InlineKeyboardButton("LOG Channel", url=invite_link.invite_link)])
    if message.chat.type != "private" and message.chat.id not in AUTH_CHATS and message.from_user.id not in SUDO_USERS:
        return await message.reply_text("This Bot Will Not Work In Groups Unless It's Authorized.",
                    reply_markup=InlineKeyboardMarkup(reply_markup))
    return await message.reply_text(f"Hello {message.from_user.first_name}, I'm a Music Downloader Bot. I Currently Support Download from \n Youtube, spotify, twitter aka x, fb, insta and many more.",
                    reply_markup=InlineKeyboardMarkup(reply_markup))

@Mbot.on_message(filters.command("restart") & filters.chat(OWNER_ID) & filters.private)
async def restart(_,message):
    await message.delete()
    execvp(sys.executable,[sys.executable,"-m","mbot"])

@Mbot.on_message(filters.command("log") & filters.chat(SUDO_USERS))
async def send_log(_,message):
    await message.reply_document("bot.log")

@Mbot.on_message(filters.command("ping"))
async def ping(client,message):
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    ms = (datetime.now() - start).microseconds / 1000
    await message.reply_text(f"**Pong!**\nResponse time: `{ms} ms`")

HELP = {
    "Youtube": "Send **Youtube** Link in Chat to Download Song.",
    "Spotify": "Send **Spotify** Track/Playlist/Album/Show/Episode's Link. I'll Download It For You.or send an name of the song",
    "Deezer": "Send Deezer Playlist/Album/Track Link. I'll Download It For You.",
    "Jiosaavn": "use /saavan faded",
    "SoundCloud": "just send me an link",
    "Group": "Will add later."
}


@Mbot.on_message(filters.command("help"))
async def help(_,message):
    button = [
        [InlineKeyboardButton(text=i, callback_data=f"help_{i}")] for i in HELP
    ]
    button.append([InlineKeyboardButton(text="back", callback_data=f"backdome")])
    await message.reply_text(f"Hello **{message.from_user.first_name}**, I'm **spotify downloader**.\nI'm Here to download your music.",
                        reply_markup=InlineKeyboardMarkup(button))

@Mbot.on_callback_query(filters.regex(r"backdome"))
async def backdo(_,query):
    button = [
        [InlineKeyboardButton(text=i, callback_data=f"help_{i}")] for i in HELP
    ]
    button.append([InlineKeyboardButton(text="back", callback_data=f"backdome")])
    await query.message.edit(f"Hello **{query.message.from_user.first_name}**, I'm **spotify downloader**.\nI'm Here to download your music.",
                        reply_markup=InlineKeyboardMarkup(button))     
    
@Mbot.on_callback_query(filters.regex(r"help_(.*?)"))
async def helpbtn(_,query):
    i = query.data.replace("help_","")
    button = InlineKeyboardMarkup([[InlineKeyboardButton("Back",callback_data="helphome")]])
    text = f"Help for **{i}**\n\n{HELP[i]}"
    await query.message.edit(text = text,reply_markup=button)

@Mbot.on_callback_query(filters.regex(r"helphome"))
async def help_home(_,query):
    button = [
        [InlineKeyboardButton(text=i, callback_data=f"help_{i}")] for i in HELP
    ]
    await query.message.edit(f"Hello **{query.from_user.first_name}**, I'm **spotify downloader**.\nI'm Here to download your music.",
                        reply_markup=InlineKeyboardMarkup(button))
