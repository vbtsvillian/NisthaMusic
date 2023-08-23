import asyncio
from pyrogram import filters
from pyrogram.types import Message
from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from Nistha.config import BOT_USERNAME, OWNER_USERNAME, SUPPORT_GROUP, UPDATE_CHANNEL
from pyrogram.errors import MessageNotModified



HOME_TEXT = """
🥀 𝐇𝐞𝐥𝐥𝐨, 𝐈 𝐀𝐦 𝐀𝐧 📀 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐀𝐧𝐝
𝐒𝐮𝐩𝐞𝐫𝐟𝐚𝐬𝐭 𝐕𝐂 𝐏𝐥𝐚𝐲𝐞𝐫 » 𝐅𝐨𝐫 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦
𝐂𝐡𝐚𝐧𝐧𝐞𝐥 𝐀𝐧𝐝 𝐆𝐫𝐨𝐮𝐩𝐬 ✨ ...

💐 𝐅𝐞𝐞𝐥 𝐅𝐫𝐞𝐞 𝐓𝐨 🕊️ 𝐀𝐝𝐝 𝐌𝐞 𝐢𝐧 𝐘𝐨𝐮𝐫
𝐆𝐫𝐨𝐮𝐩, 🌺 𝐀𝐧𝐝 𝐄𝐧𝐣𝐨𝐲 ❥︎ 𝐒𝐮𝐩𝐞𝐫 𝐇𝐢𝐠𝐡
𝐐𝐮𝐚𝐥𝐢𝐭𝐲 𝐀𝐮𝐝𝐢𝐨 𝐀𝐧𝐝 𝐕𝐢𝐝𝐞𝐨 🌷 ...
"""

SUDO_CMD = """
🌾 **𝑺𝑼𝑫𝑶 𝑪𝑶𝑴𝑴𝑨𝑵𝑫𝑺 :**
๏ /gcast : 𝐵𝑅𝑂𝐴𝐷𝐶𝐴𝑆𝑇 𝐴 𝑀𝐸𝑆𝑆𝐴𝐺𝐸 𝑇𝑂 𝑆𝐸𝑅𝑉𝐸𝐷 𝐶𝐻𝐴𝑇𝑆 𝑂𝐹 𝑇𝐻𝐸 𝐵𝑂𝑇.
๏ /eval or /sh : 𝑅𝑈𝑁𝑆 𝑇𝐻𝐸 𝐺𝐼𝑉𝐸𝑁 𝐶𝑂𝐷𝐸 𝑂𝑁 𝑇𝐻𝐸 𝐵𝑂𝑇'𝑆 𝑇𝐸𝑅𝑀𝐼𝑁𝐴𝐿.
๏ /rmw : 𝐶𝐿𝐸𝐴𝑅𝑆 𝐴𝐿𝐿 𝑇𝐻𝐸 𝐶𝐴𝐶𝐻𝐸 𝑃𝐻𝑂𝑇𝑂𝑆 𝑂𝑁 𝑇𝐻𝐸 𝐵𝑂𝑇'𝑆 𝑆𝐸𝑅𝑉𝐸𝑅.
๏ /rmp : 𝐶𝐿𝐸𝐴𝑅𝑆 𝑇𝐻𝐸 𝑅𝐴𝑊 𝐹𝐼𝐿𝐸𝑆 𝑂𝐹 𝑇𝐻𝐸 𝐵𝑂𝑇.
๏ /rmd : 𝐶𝐿𝐸𝐴𝑅𝑆 𝑇𝐻𝐸 𝐷𝑂𝑊𝑁𝐿𝑂𝐴𝐷𝐸𝐷 𝐹𝐼𝐿𝐸𝑆 𝑂𝑁 𝑇𝐻𝐸 𝐵𝑂𝑇'𝑆 𝑆𝐸𝑅𝑉𝐸𝑅.

"""



USERS_CMMD = """
𝑨𝑽𝑨𝑰𝑳𝑨𝑩𝑳𝑬 𝑪𝑶𝑴𝑴𝑨𝑵𝑫𝑺 𝑰𝑵 𝑴𝑼𝑺𝑰𝑪 𝑩𝑶𝑻 :
๏ /play : 𝑆𝑇𝐴𝑅𝑇𝑆 𝑆𝑇𝑅𝐸𝐴𝑀𝐼𝑁𝐺 𝑇𝐻𝐸 𝑅𝐸𝑄𝑈𝐸𝑆𝑇𝐸𝐷 𝑇𝑅𝐴𝐶𝐾 𝑂𝑁 𝑉𝐼𝐷𝐸𝑂𝐶𝐻𝐴𝑇.
๏ /pause : 𝑃𝐴𝑈𝑆𝐸 𝑇𝐻𝐸 𝐶𝑈𝑅𝑅𝐸𝑁𝑇 𝑃𝐿𝐴𝑌𝐼𝑁𝐺 𝑆𝑇𝑅𝐸𝐴𝑀.
๏ /resume : 𝑅𝐸𝑆𝑈𝑀𝐸 𝑇𝐻𝐸 𝑃𝐴𝑈𝑆𝐸𝐷 𝑆𝑇𝑅𝐸𝐴𝑀.
๏ /skip : 𝑆𝐾𝐼𝑃 𝑇𝐻𝐸 𝐶𝑈𝑅𝑅𝐸𝑁𝑇 𝑃𝐿𝐴𝑌𝐼𝑁𝐺 𝑆𝑇𝑅𝐸𝐴𝑀 𝐴𝑁𝐷 𝑆𝑇𝐴𝑅𝑇 𝑆𝑇𝑅𝐸𝐴𝑀𝐼𝑁𝐺 𝑇𝐻𝐸 𝑁𝐸𝑋𝑇 𝑇𝑅𝐴𝐶𝐾 𝐼𝑁 𝑄𝑈𝐸𝑈𝐸.
๏ /end : 𝐶𝐿𝐸𝐴𝑅𝑆 𝑇𝐻𝐸 𝑄𝑈𝐸𝑈𝐸 𝐴𝑁𝐷 𝐸𝑁𝐷 𝑇𝐻𝐸 𝐶𝑈𝑅𝑅𝐸𝑁𝑇 𝑃𝐿𝐴𝑌𝐼𝑁𝐺 𝑆𝑇𝑅𝐸𝐴𝑀.
๏ /ping : 𝑆𝐻𝑂𝑊 𝑇𝐻𝐸 𝑃𝐼𝑁𝐺 𝐴𝑁𝐷 𝑆𝑌𝑆𝑇𝐸𝑀 𝑆𝑇𝐴𝑇𝑆 𝑂𝐹 𝑇𝐻𝐸 𝐵𝑂𝑇.
๏ /join : 𝑅𝐸𝑄𝑈𝐸𝑆𝑇 𝑇𝐻𝐸 𝐴𝑆𝑆𝐼𝑆𝑇𝐴𝑁𝑇 𝑇𝑂 𝐽𝑂𝐼𝑁 𝑌𝑂𝑈𝑅 𝐶𝐻𝐴𝑇.
๏ /id : 𝑆𝐸𝑁𝐷𝑆 𝑌𝑂𝑈 𝑇𝐻𝐸 𝐼𝐷 𝑂𝐹 𝑇𝐻𝐸 𝑈𝑆𝐸𝑅 𝑂𝑅 𝑅𝐸𝑃𝐿𝐼𝐸𝐷 𝐹𝐼𝐿𝐸.
๏ /song : 𝐷𝑂𝑊𝑁𝐿𝑂𝐴𝐷𝑆 𝑇𝐻𝐸 𝑅𝐸𝑄𝑈𝐸𝑆𝑇𝐸𝐷 𝑆𝑂𝑁𝐺 𝐴𝑁𝐷 𝑆𝐸𝑁𝐷 𝐼𝑇 𝑇𝑂 𝑌𝑂𝑈.
๏ /search : 𝑆𝐸𝐴𝑅𝐶𝐸𝑆 𝑇𝐻𝐸 𝐺𝐼𝑉𝐸𝑁 𝑄𝑈𝐸𝑅𝑌 𝑂𝑁 𝑌𝑂𝑈𝑇𝑈𝐵𝐸 𝐴𝑁𝐷 𝑆𝐻𝑂𝑊 𝑌𝑂𝑈 𝑇𝐻𝐸 𝑅𝐸𝑆𝑈𝐿𝑇.

"""


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data=="home":
        buttons = [
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
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                HOME_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass


    elif query.data=="help_cmd":
        get_me = await client.get_me()
        USERNAME = get_me.username
        buttons = [
                [
                    InlineKeyboardButton(
                        "💖 𝑺𝑼𝑫𝑶 𝑪𝑴𝑫 💖", callback_data="sudo_users"),
                    InlineKeyboardButton(
                        "🌷 𝑼𝑺𝑬𝑹𝑺 𝑪𝑴𝑫 🌷", callback_data="users_cmd"),
                ],
                [
                    InlineKeyboardButton(
                        "👑 𝙈𝙖𝙞𝙣𝙩𝙖𝙞𝙣𝙚𝙧", url="https://t.me/{OWNER_USERNAME}"),
                    InlineKeyboardButton("⟲ 𝑩𝑨𝑪𝑲 ⟳", callback_data="home")
                ]
           ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                HOME_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass



      

    elif query.data=="users_cmd":
        buttons =  [              
                [
                    InlineKeyboardButton("⟲ 𝑩𝑨𝑪𝑲 ⟳", callback_data="help_cmd")
                ]
           ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                USERS_CMMD.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass


    elif query.data=="sudo_users":
        buttons =  [              
                [
                    InlineKeyboardButton("⟲ 𝑩𝑨𝑪𝑲 ⟳", callback_data="help_cmd")
                ]
           ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                SUDO_CMD.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass
 
    elif query.data=="close_play":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            pass  
 
