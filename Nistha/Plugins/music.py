import os
import aiofiles
import aiohttp
import ffmpeg
import random
import numpy as np
import textwrap
import requests
from os import path
from asyncio.queues import QueueEmpty
from typing import Callable
from pyrogram import Client, filters
from Nistha.config import SUPPORT_GROUP, UPDATE_CHANNEL, OWNER_USERNAME
from pyrogram.types import Message, Voice, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import UserAlreadyParticipant
from Nistha.Modules.cache.admins import set
from Nistha.Modules.cache import clientbot, queues
from Nistha.Modules.cache.clientbot import client as USER
from Nistha.Modules.helpers.admins import get_administrators
from youtube_search import YoutubeSearch
from Nistha.Modules.cache import converter
from Nistha.Modules.cache import youtube
from Nistha.config import DURATION_LIMIT, que, SUDO_USERS
from Nistha.Modules.cache.admins import admins as a
from Nistha.Modules.helpers.decorators import errors, authorized_users_only
from Nistha.Modules.helpers.errors import DurationLimitError
from Nistha.Modules.helpers.gets import get_url, get_file_name
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from PIL import ImageGrab
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream import InputAudioStream

# plus
chat_id = None
useer = "NaN"

def make_col():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))


def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw", format="s16le", acodec="pcm_s16le", ac=2, ar="48k"
    ).overwrite_output().run()
    os.remove(filename)


# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))

def truncate(text):
    list = text.split(" ")
    text1 = ""
    text2 = ""    
    for i in list:
        if len(text1) + len(i) < 27:        
            text1 += " " + i
        elif len(text2) + len(i) < 25:        
            text2 += " " + i

    text1 = text1.strip()
    text2 = text2.strip()     
    return [text1,text2]


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    image = Image.open(f"./background.png")
    black = Image.open("resource/black.jpg")
    img = Image.open("resource/nistha.png")
    image5 = changeImageSize(1280, 720, img)
    image1 = changeImageSize(1280, 720, image)
    image1 = image1.filter(ImageFilter.BoxBlur(10))
    image11 = changeImageSize(1280, 720, image)
    image1 = image11.filter(ImageFilter.BoxBlur(20))
    image1 = image11.filter(ImageFilter.BoxBlur(20))
    image2 = Image.blend(image1,black,0.6)

    im = image5
    im = im.convert('RGBA')
    color = make_col()

    data = np.array(im)
    red, green, blue, alpha = data.T

    white_areas = (red == 255) & (blue == 255) & (green == 255)
    data[..., :-1][white_areas.T] = color

    im2 = Image.fromarray(data)
    image5 = im2


    # Cropping circle from thubnail
    image3 = image11.crop((280,0,1000,720))
    lum_img = Image.new('L', [720,720] , 0)
    draw = ImageDraw.Draw(lum_img)
    draw.pieslice([(0,0), (720,720)], 0, 360, fill = 255, outline = "white")
    img_arr =np.array(image3)
    lum_img_arr =np.array(lum_img)
    final_img_arr = np.dstack((img_arr,lum_img_arr))
    image3 = Image.fromarray(final_img_arr)
    image3 = image3.resize((600,600))
    
    image2.paste(image3, (50,70), mask = image3)
    image2.paste(image5, (0,0), mask = image5)

    # fonts
    font1 = ImageFont.truetype(r'resource/robot.otf', 30)
    font2 = ImageFont.truetype(r'resource/robot.otf', 60)
    font3 = ImageFont.truetype(r'resource/robot.otf', 49)
    font4 = ImageFont.truetype(r'resource/Mukta-ExtraBold.ttf', 35)

    image4 = ImageDraw.Draw(image2)
    image4.text((10, 10), "VILLIAN MUSIC", fill="white", font = font1, align ="left") 
    image4.text((670, 150), "NOW PLAYING", fill="white", font = font2, stroke_width=2, stroke_fill="white", align ="left") 

    # title
    title1 = truncate(title)
    image4.text((670, 280), text=title1[0], fill="white", font = font3, align ="left") 
    image4.text((670, 332), text=title1[1], fill="white", font = font3, align ="left") 

    # description
    views = f"Views : {views}"
    duration = f"Duration : {duration} minutes"
    channel = f"Channel : T-Series"


    
    image4.text((670, 410), text=views, fill="white", font = font4, align ="left") 
    image4.text((670, 460), text=duration, fill="white", font = font4, align ="left") 
    image4.text((670, 510), text=channel, fill="white", font = font4, align ="left")

    
    image2.save(f"final.png")
    os.remove(f"background.png")
    final = f"temp.png"
    return final


@Client.on_message(filters.command(["yt", "play"], prefixes=["/", "!"]))    
async def play(_, message: Message):
    global que
    global useer
    
    lel = await message.reply("**🔎 𝑺𝑬𝑨𝑹𝑪𝑯𝑰𝑵𝑮...**")
   
    bsdk = message.from_user.mention

    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "SumitYadav"
    usar = user
    wew = usar.id
    try:
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "**» 𝘼𝘿𝘿 𝙈𝙀 𝘼𝘿𝙈𝙄𝙉 𝙄𝙉 𝙔𝙊𝙐𝙍 𝙂𝙍𝙊𝙐𝙋 𝙁𝙄𝙍𝙎𝙏.**")
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id, "** ✅ 𝑨𝑺𝑺𝑰𝑺𝑻𝑨𝑵𝑻 𝑱𝑶𝑰𝑵𝑬𝑫 𝑻𝑯𝑰𝑺 𝑮𝑹𝑶𝑼𝑷 𝑭𝑶𝑹 𝑷𝑳𝑨𝒀 𝑴𝑼𝑺𝑰𝑪.**")

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    await lel.edit(
                        f"**𝑷𝑳𝑬𝑨𝑺𝑬 𝑴𝑨𝑵𝑼𝑨𝑳𝑳𝒀 𝑨𝑫𝑫 𝑨𝑺𝑺𝑰𝑺𝑻𝑨𝑵𝑻 𝑶𝑹 𝑪𝑶𝑵𝑻𝑨𝑪𝑻 [𝙑𝙄𝙇𝙇𝙄𝘼𝙉 𝙈𝙐𝙎𝙄𝘾](https://t.me/{OWNER_USERNAME})** ")
    try:
        await USER.get_chat(chid)
    except:
        await lel.edit(
            f"**𝑷𝑳𝑬𝑨𝑺𝑬 𝑴𝑨𝑵𝑼𝑨𝑳𝑳𝒀 𝑨𝑫𝑫 𝑨𝑺𝑺𝑰𝑺𝑻𝑨𝑵𝑻 𝑶𝑹 𝑪𝑶𝑵𝑻𝑨𝑪𝑻 [𝙑𝙄𝙇𝙇𝙄𝘼𝙉 𝙈𝙐𝙎𝙄𝘾](https://t.me/{OWNER_USERNAME})*")
        return
    
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"**» 𝑺𝑶𝑵𝑮 𝑳𝑶𝑵𝑮𝑬𝑹 𝑻𝑯𝑨𝑵 {DURATION_LIMIT} 𝑴𝑰𝑵𝑼𝑻𝑬'𝑺 𝑨𝑹𝑬 𝑵𝑶𝑻 𝑨𝑳𝑳𝑶𝑾𝑬𝑫 𝑻𝑶 𝑷𝑳𝑨𝒀.**"
            )

        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/00411492c1fb4c0a91f18.jpg"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"

        keyboard = InlineKeyboardMarkup(
             [
            [
                InlineKeyboardButton(text=" 𝙎𝙪𝙥𝙥𝙤𝙧𝙩 ", url=f"https://t.me/{SUPPORT_GROUP}"),
                InlineKeyboardButton(text=" 𝙐𝙥𝙙𝙖𝙩𝙚𝙨 ", url=f"https://t.me/{UPDATE_CHANNEL}"),
            ],
            [   InlineKeyboardButton(text=" 𝑪𝑳𝑶𝑺𝑬 ", callback_data="close_play")
            ]
        ]
    )

        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )

    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

            keyboard = InlineKeyboardMarkup(
             [
            [
                InlineKeyboardButton(text=" 𝙎𝙪𝙥𝙥𝙤𝙧𝙩 ", url=f"https://t.me/{SUPPORT_GROUP}"),
                InlineKeyboardButton(text=" 𝙐𝙥𝙙𝙖𝙩𝙚𝙨 ", url=f"https://t.me/{UPDATE_CHANNEL}"),
            ],
            [   InlineKeyboardButton(text=" 𝑪𝑳𝑶𝑺𝑬 ", callback_data="close_play")
            ]
        ]
    )
        except Exception as e:
            title = "NaN"
            thumb_name = "https://telegra.ph/file/00411492c1fb4c0a91f18.jpg"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
             [
            [
                InlineKeyboardButton(text=" 𝙎𝙪𝙥𝙥𝙤𝙧𝙩 ", url=f"https://t.me/{SUPPORT_GROUP}"),
                InlineKeyboardButton(text=" 𝙐𝙥𝙙𝙖𝙩𝙚𝙨 ", url=f"https://t.me/{UPDATE_CHANNEL}"),
            ],
            [   InlineKeyboardButton(text=" 𝑪𝑳𝑶𝑺𝑬 ", callback_data="close_play")
            ]
        ]
    )

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"**» 𝑺𝑶𝑵𝑮 𝑳𝑶𝑵𝑮𝑬𝑹 𝑻𝑯𝑨𝑵 {DURATION_LIMIT} 𝑴𝑰𝑵𝑼𝑻𝑬'𝑺 𝑨𝑹𝑬 𝑵𝑶𝑻 𝑨𝑳𝑳𝑶𝑾𝑬𝑫 𝑻𝑶 𝑷𝑳𝑨𝒀.**"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))
    else:
        if len(message.command) < 2:
            await message.reply_photo(
                     photo=f"https://te.legra.ph/file/71bdd6e8c353398a4034a.jpg",
                     caption="💌 **𝑼𝑺𝑨𝑮𝑬: /play 𝑮𝑰𝑽𝑬 𝑨 𝑻𝑰𝑻𝑳𝑬 𝑺𝑶𝑵𝑮 𝑻𝑶 𝑷𝑳𝑨𝒀 𝑴𝑼𝑺𝑰𝑪**"
                    
            )
        await lel.edit("**⇆ 𝑷𝑹𝑶𝑪𝑬𝑺𝑺𝑰𝑵𝑮.**")
        query = message.text.split(None, 1)[1]
        # print(query)
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

        except Exception as e:
            await lel.edit(
                "**» 𝑵𝑶𝑻 𝑭𝑶𝑼𝑵𝑫, 𝑻𝑹𝒀 𝑺𝑬𝑨𝑹𝑪𝑯𝑰𝑵𝑮 𝑾𝑰𝑻𝑯 𝑻𝑯𝑬 𝑺𝑶𝑵𝑮 𝑵𝑨𝑴𝑬.**"
            )
            print(str(e))
            return

        keyboard = InlineKeyboardMarkup(
             [
            [
                InlineKeyboardButton(text=" 𝙎𝙪𝙥𝙥𝙤𝙧𝙩 ", url=f"https://t.me/{SUPPORT_GROUP}"),
                InlineKeyboardButton(text=" 𝙐𝙥𝙙𝙖𝙩𝙚𝙨 ", url=f"https://t.me/{UPDATE_CHANNEL}"),
            ],
            [   InlineKeyboardButton(text=" 𝑪𝑳𝑶𝑺𝑬 ", callback_data="close_play")
            ]
        ]
    )
        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"**» 𝑺𝑶𝑵𝑮 𝑳𝑶𝑵𝑮𝑬𝑹 𝑻𝑯𝑨𝑵 {DURATION_LIMIT} 𝑴𝑰𝑵𝑼𝑻𝑬'𝑺 𝑨𝑹𝑬 𝑵𝑶𝑻 𝑨𝑳𝑳𝑶𝑾𝑬𝑫 𝑻𝑶 𝑷𝑳𝑨𝒀.**"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))
    ACTV_CALLS = []
    chat_id = message.chat.id
    for x in clientbot.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) in ACTV_CALLS:
        position = await queues.put(chat_id, file=file_path)
        await message.reply_photo(
            photo="final.png",
            caption=f"**➻ 𝑇𝑅𝐴𝐶𝐾 𝐴𝐷𝐷𝐸𝐷 𝑇𝑂 𝑄𝑈𝐸𝑈𝐸 » {position} **\n\n​ 🍒**𝑁𝐴𝑀𝐸 :**[{title[:65]}]({url})\n⏰ ** 𝐷𝑈𝑅𝐴𝑇𝐼𝑂𝑁 :** `{duration}` **𝑀𝐼𝑁𝑈𝑇𝐸𝑆**\n👀 ** 𝑅𝐸𝑄𝑈𝐸𝑆𝑇𝐸𝐷 𝐵𝑌 : **{bsdk}",
            reply_markup=keyboard,
        )
    else:
        await clientbot.pytgcalls.join_group_call(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        file_path,
                    ),
                ),
                stream_type=StreamType().local_stream,
            )

        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption=f"**➻ 𝑆𝑇𝐴𝑅𝑇𝐸𝐷 𝑆𝑇𝑅𝐸𝐴𝑀𝐼𝑁𝐺\n\n🍒 𝑁𝐴𝑀𝐸 : **[{title[:65]}]({url})\n⏰ **𝐷𝑈𝑅𝐴𝑇𝐼𝑂𝑁 :** `{duration}` 𝑀𝐼𝑁𝑈𝑇𝐸𝑆\n👀 **𝑅𝐸𝑄𝑈𝐸𝑆𝑇𝐸𝐷 𝐵𝑌 ​:** {bsdk}\n",
           )

    os.remove("final.png")
    return await lel.delete()
    

@Client.on_message(filters.command(["pause"], prefixes=["/", "!"]))    
@errors
@authorized_users_only
async def pause(_, message: Message):
    await clientbot.pytgcalls.pause_stream(message.chat.id)
    await message.reply_text("**» 𝑀𝑈𝑆𝐼𝐶 𝑃𝐿𝐴𝑌𝐸𝑅 𝑁𝑂𝑇𝐻𝐼𝑁𝐺 𝐼𝑆 𝑃𝐿𝐴𝑌𝐼𝑁𝐺.**")
    


@Client.on_message(filters.command(["resume"], prefixes=["/", "!"]))
@errors
@authorized_users_only
async def resume(_, message: Message):
    await clientbot.pytgcalls.resume_stream(message.chat.id)
    await message.reply_text("**» 𝑀𝑈𝑆𝐼𝐶 𝑃𝐿𝐴𝑌𝐸𝑅 𝑆𝑈𝐶𝐶𝐸𝑆𝑆𝐹𝑈𝐿𝐿𝑌 𝑅𝐸𝑆𝑈𝑀𝐸𝐷.**")
    
    

@Client.on_message(filters.command(["skip", "next"], prefixes=["/", "!"]))
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    ACTV_CALLS = []
    chat_id = message.chat.id
    for x in clientbot.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALLS:
        await message.reply_text("**» 𝑀𝑈𝑆𝐼𝐶 𝑃𝐿𝐴𝑌𝐸𝑅 𝑁𝑂𝑇𝐻𝐼𝑁𝐺 𝐼𝑆 𝑃𝐿𝐴𝑌𝐼𝑁𝐺 𝑇𝑂 𝑆𝐾𝐼𝑃.**")
        
    else:
        queues.task_done(chat_id)
        
        if queues.is_empty(chat_id):
            await clientbot.pytgcalls.leave_group_call(chat_id)
        else:
            await clientbot.pytgcalls.change_stream(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        clientbot.queues.get(chat_id)["file"],
                    ),
                ),
            )


    await message.reply_text("**» 𝑀𝑈𝑆𝐼𝐶 𝑃𝐿𝐴𝑌𝐸𝑅 𝑆𝐾𝐼𝑃𝑃𝐸𝐷 𝑇𝐻𝐸 𝑆𝑂𝑁𝐺.**")
    


@Client.on_message(filters.command(["end", "stop"], prefixes=["/", "!"]))
@errors
@authorized_users_only
async def stop(_, message: Message):
    try:
        clientbot.queues.clear(message.chat.id)
    except QueueEmpty:
        pass

    await clientbot.pytgcalls.leave_group_call(message.chat.id)
    await message.reply_text("**» 𝑀𝑈𝑆𝐼𝐶 𝑃𝐿𝐴𝑌𝐸𝑅 𝑁𝑂𝑇𝐻𝐼𝑁𝐺 𝐼𝑆 𝑆𝑇𝑅𝐸𝐴𝑀𝐼𝑁𝐺.**")
    

@Client.on_message(filters.command(["reload", "refresh"], prefixes=["/", "!"]))
@errors
@authorized_users_only
async def admincache(client, message: Message):
    set(
        message.chat.id,
        (
            member.user
            for member in await message.chat.get_members(filter="administrators")
        ),
    )

    await message.reply_photo(
                              photo="https://telegra.ph/file/fa8358cbb060a1b92339a.jpg",
                              caption="**✅ 𝐵𝑂𝑇 𝑅𝐸𝐿𝑂𝐴𝐷𝐸𝐷 𝐶𝑂𝑅𝑅𝐸𝐶𝑇𝐿𝑌 !\n✅ 𝐴𝐷𝑀𝐼𝑁 𝐿𝐼𝑆𝑇 𝐻𝐴𝑆 𝑈𝑃𝐷𝐴𝑇𝐸𝐷 !**")
                               
