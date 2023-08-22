import os
import asyncio
import requests
import aiohttp
import yt_dlp
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
from Nistha.Modules.helpers.decorators import authorized_users_only
from Nistha.Modules.cache.clientbot import client as user
from Nistha.config import BOT_USERNAME, STRING_SESSION as SESSION_NAME
from Nistha.Modules.helpers.get_file_id import get_file_id
from youtube_search import YoutubeSearch

# ×=======================> 𝑈𝑆𝐸𝑅𝐵𝑂𝑇 𝐽𝑂𝐼𝑁 𝐶𝑂𝑀𝑀𝐴𝑁𝐷 <==================================× #



@Client.on_message(filters.command(["join", "userbotjoin"], prefixes=["/", "!"]))
@authorized_users_only
async def join_chat(c: Client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    try:
        invite_link = await m.chat.export_invite_link()
        if "+" in invite_link:
            link_hash = (invite_link.replace("+", "")).split("t.me/")[1]
            await user.join_chat(f"https://t.me/joinchat/{link_hash}")
        await m.chat.promote_member(
            (await user.get_me()).id,
            can_manage_voice_chats=True
        )
        return await user.send_message(chat_id, "» 𝐴𝑆𝑆𝐼𝑆𝑇𝐴𝑁𝑇 𝑆𝑈𝐶𝐶𝐸𝑆𝑆𝐹𝑈𝐿𝐿𝑌 𝐽𝑂𝐼𝑁𝐸𝐷 𝑇𝐻𝐸 𝐶𝐻𝐴𝑇.​")
    except UserAlreadyParticipant:
        admin = await m.chat.get_member((await user.get_me()).id)
        if not admin.can_manage_voice_chats:
            await m.chat.promote_member(
                (await user.get_me()).id,
                can_manage_voice_chats=True
            )
            return await user.send_message(chat_id, "» 𝐴𝑆𝑆𝐼𝑆𝑇𝐴𝑁𝑇 𝐴𝐿𝑅𝐸𝐴𝐷𝑌 𝐽𝑂𝐼𝑁𝐸𝐷 𝑇𝐻𝐸 𝐶𝐻𝐴𝑇.​")
        return await user.send_message(chat_id, "» 𝐴𝑆𝑆𝐼𝑆𝑇𝐴𝑁𝑇 𝐴𝐿𝑅𝐸𝐴𝐷𝑌 𝐽𝑂𝐼𝑁𝐸𝐷 𝑇𝐻𝐸 𝐶𝐻𝐴𝑇.​")



# ×=======================> 𝐼𝑁𝐹𝑂 <==================================× #

@Client.on_message(filters.command(["id", "stickerid"], prefixes=["/", "!"]))
async def showid(_, message: Message):
    await message.delete()
    chat_type = message.chat.type

    if chat_type == "private":
        user_id = message.chat.id
        await message.reply_text(f"<code>{user_id}</code>")

    elif chat_type in ["group", "supergroup"]:
        _id = ""
        _id += "<b>𝐶𝐻𝐴𝑇 𝐼𝐷</b>: " f"<code>{message.chat.id}</code>\n"
        if message.reply_to_message:
            _id += (
                "<b>𝑅𝐸𝑃𝐿𝐼𝐸𝐷 𝑈𝑆𝐸𝑅 𝐼𝐷</b>: "
                f"<code>{message.reply_to_message.from_user.id}</code>\n"
            )
            file_info = get_file_id(message.reply_to_message)
        else:
            _id += "<b>𝑈𝑆𝐸𝑅 𝐼𝐷</b>: " f"<code>{message.from_user.id}</code>\n"
            file_info = get_file_id(message)
        if file_info:
            _id += (
                f"<b>{file_info.message_type}</b>: "
                f"<code>{file_info.file_id}</code>\n"
            )
        await message.reply_text(_id)


# ×=======================> 𝑆𝑂𝑁𝐺 𝐷𝑂𝑊𝑁𝐿𝑂𝐴𝐷𝐸𝑅 <==================================× #


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))



@Client.on_message(filters.command(["song", "music"], prefixes=["/", "!"]))
def song(client, message):
    message.delete()
    user_id = message.from_user.id 
    user_name = message.from_user.first_name 
    chutiya = "["+user_name+"](tg://user?id="+str(user_id)+")"

    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply("🔎")
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        #print(results)
        title = results[0]["title"][:40]       
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)


        duration = results[0]["duration"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["views"]

    except Exception as e:
        m.edit(
            "» 𝑁𝑂𝑇 𝐹𝑂𝑈𝑁𝐷, 𝑇𝑅𝑌 𝑆𝐸𝐴𝑅𝐶𝐻𝐼𝑁𝐺 𝑊𝐼𝑇𝐻 𝑇𝐻𝐸 𝑆𝑂𝑁𝐺 𝑁𝐴𝑀𝐸."
        )
        print(str(e))
        return
    m.edit(f"» 𝐷𝑂𝑊𝑁𝐿𝑂𝐴𝐷𝐼𝑁𝐺 𝑆𝑂𝑁𝐺 𝐹𝑅𝑂𝑀 𝑌𝑂𝑈𝑇𝑈𝐵𝐸 𝑆𝐸𝑅𝑉𝐸𝑅.")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"**➠ 𝑈𝑃𝐿𝑂𝐴𝐷𝐸𝐷 𝐵𝑌 » [𝑉𝐼𝐿𝐿𝐼𝐴𝑁 𝑀𝑈𝑆𝐼𝐶](t.me/{BOT_USERNAME}) 🍄\n➠ 𝑅𝐸𝑄𝑈𝐸𝑆𝑇𝐸𝐷 𝐵𝑌 » {chutiya}\n➠ 𝑆𝐸𝐴𝑅𝐶𝐻𝐸𝐷 𝐹𝑂𝑅 » {query}**"
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, thumb=thumb_name, parse_mode='md', title=title, duration=dur)
        m.delete()
    except Exception as e:
        m.edit("**» 𝐷𝑂𝑊𝑁𝐿𝑂𝐴𝐷𝐼𝑁𝐺 𝐸𝑅𝑅𝑂𝑅, 𝑅𝐸𝑃𝑂𝑅𝑇 𝑇𝐻𝐼𝑆 𝐴𝑇 » [𝑇𝐻𝐸 𝑆𝑈𝑃𝑃𝑂𝑅𝑇 𝐵𝑂𝑇𝑆](t.me/villen_012)**")
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
