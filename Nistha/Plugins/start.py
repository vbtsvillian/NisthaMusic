import asyncio
import random
from Nistha.config import BOT_USERNAME, OWNER_USERNAME, UPDATE_CHANNEL, SUPPORT_GROUP
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


NISTHA_IMG = (
"https://te.legra.ph/file/29efe52db5e67ee6d4fd0.jpg",
"https://te.legra.ph/file/ec4ea51f5722d95c1fb10.jpg",
"https://te.legra.ph/file/0c99b0ca4dc059b5f4972.jpg",
"https://te.legra.ph/file/23564f55fcef37840bbfa.jpg",
"https://te.legra.ph/file/d0dc7068544b8e81c606e.jpg",
"https://te.legra.ph/file/fbf66543cd3fe8a41b2ad.jpg",
"https://te.legra.ph/file/dc728b557a1cd7a74fc42.jpg",
"https://te.legra.ph/file/4107e97e94adab62c267d.jpg",
"https://te.legra.ph/file/c57bba14be21bb6631815.jpg",
"https://te.legra.ph/file/5d51b83e489de2f7a8293.jpg",
"https://te.legra.ph/file/e851855a8390a373b23d0.jpg",
"https://te.legra.ph/file/3174338955c559a894ec7.jpg",
"https://te.legra.ph/file/c706b4ae35156a292c740.jpg",
"https://te.legra.ph/file/05492cb1a8318471ea307.jpg",
"https://te.legra.ph/file/fcdbd3fde29d45399d150.jpg",
"https://te.legra.ph/file/454680582a1faa939f58e.jpg",
"https://te.legra.ph/file/ab7fed7efde246918eeb8.jpg",
"https://te.legra.ph/file/51a9be7257158184c353f.jpg",
"https://te.legra.ph/file/13dfbd0773465b8e527af.jpg",
"https://te.legra.ph/file/1308473f7a47df9168f41.jpg",
"https://te.legra.ph/file/f194514cca6cacda701ae.jpg",
"https://te.legra.ph/file/a59c584da4af0c87e5e31.jpg",
"https://te.legra.ph/file/fac2e3033d2bc5a728afd.jpg",
"https://te.legra.ph/file/b507247de16b6b3686772.jpg",
"https://te.legra.ph/file/0d3a504686402a2a90c7e.jpg",
"https://te.legra.ph/file/11960860ef8e4a55a7910.jpg",
"https://te.legra.ph/file/ad52fb8a64a713dd84412.jpg",
"https://te.legra.ph/file/cb77a02e0f58f8ca9eae0.jpg",
"https://te.legra.ph/file/fc93e08268212a4e4250d.jpg",
"https://te.legra.ph/file/c7ecdbdece963f490bfb9.jpg",
"https://te.legra.ph/file/6778f0f74f7786a6fb9fb.jpg",

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
    
    
