import asyncio
import random
from Nistha.config import BOT_USERNAME, OWNER_USERNAME, UPDATE_CHANNEL, SUPPORT_GROUP
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


NISTHA_IMG = (
"https://graph.org/file/6edbec3eac70b422b8669.jpg",
"https://graph.org/file/c453d0cb3b231ab7d260e.jpg",
"https://graph.org/file/a4f85b4cacdd11e6386ec.jpg",
"https://graph.org/file/49df9f64fe4869b465312.jpg",
"https://graph.org/file/011d891e862ebe4e49316.jpg",
"https://graph.org/file/956568bd5872494bfe770.jpg",
"https://graph.org/file/5bde42a02c3b01ca9dc69.jpg",

)





START_TEXT = """
🥀 𝐇𝐞𝐥𝐥𝐨, 𝐈 𝐀𝐦 𝐀𝐧 📀 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐀𝐧𝐝
𝐒𝐮𝐩𝐞𝐫𝐟𝐚𝐬𝐭 𝐕𝐂 𝐏𝐥𝐚𝐲𝐞𝐫 » 𝐅𝐨𝐫 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦
𝐂𝐡𝐚𝐧𝐧𝐞𝐥 𝐀𝐧𝐝 𝐆𝐫𝐨𝐮𝐩𝐬 ✨ ...

💐 𝐅𝐞𝐞𝐥 𝐅𝐫𝐞𝐞 𝐓𝐨 🕊️ 𝐀𝐝𝐝 𝐌𝐞 𝐢𝐧 𝐘𝐨𝐮𝐫
𝐆𝐫𝐨𝐮𝐩, 🌺 𝐀𝐧𝐝 𝐄𝐧𝐣𝐨𝐲 ❥︎ 𝐒𝐮𝐩𝐞𝐫 𝐇𝐢𝐠𝐡
𝐐𝐮𝐚𝐥𝐢𝐭𝐲 𝐀𝐮𝐝𝐢𝐨 𝐀𝐧𝐝 𝐕𝐢𝐝𝐞𝐨 🌷 ...
"""

    
   

@Client.on_message(filters.command(["start"], prefixes=["/", "!"]))
async def start_(client: Client, message: Message):
    await message.reply_photo(
        random.choice(NISTHA_IMG),
        caption=(START_TEXT),
    reply_markup=InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("🌷𝑨𝒅𝒅 𝑴𝒆 𝑻𝒐 𝒀𝒐𝒖𝒓 𝑮𝒓𝒐𝒖𝒑🌷", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
        ],
        [
            InlineKeyboardButton("🥀 𝙎𝙪𝙥𝙥𝙤𝙧𝙩 💥", url="https://t.me/{SUPPORT_GROUP}"),
            InlineKeyboardButton("🥀 𝙐𝙥𝙙𝙖𝙩𝙚𝙨 💥", url="https://t.me/{UPDATE_CHANNEL}")
        ],
        [
            InlineKeyboardButton("💖 𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨 💖", callback_data="help_cmd"),
            InlineKeyboardButton("👑 𝙈𝙖𝙞𝙣𝙩𝙖𝙞𝙣𝙚𝙧", url="https://t.me/{OWNER_USERNAME}"),
        ]
   
     ]
  ),
)
    
    
