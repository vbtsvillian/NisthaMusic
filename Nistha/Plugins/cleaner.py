import os
from pyrogram import Client, filters
from pyrogram.types import Message
from Nistha.Modules.helpers.decorators import sudo_users_only, errors

downloads = os.path.realpath("downloads")
raw_files = os.path.realpath("raw_files")

@Client.on_message(filters.command(["rmd", "clear"], prefixes=["/", "!"]))
@errors
@sudo_users_only
async def clear_downloads(_, message: Message):
    ls_dir = os.listdir(downloads)
    if ls_dir:
        for file in os.listdir(downloads):
            os.remove(os.path.join(downloads, file))
        await message.reply_text("✅ **𝐷𝐸𝐿𝐸𝑇𝐸𝐷 𝐴𝐿𝐿 𝐷𝑂𝑊𝑁𝐿𝑂𝐴𝐷 𝐹𝐼𝐿𝐸𝑆**")
    else:
        await message.reply_text("❌ **𝑁𝑂 𝐹𝐼𝐿𝐸𝑆 𝐷𝑂𝑊𝑁𝐿𝑂𝐴𝐷𝐸𝐷**")

        
@Client.on_message(filters.command(["rmw", "clean"], prefixes=["/", "!"]))
@errors
@sudo_users_only
async def clear_raw(_, message: Message):
    ls_dir = os.listdir(raw_files)
    if ls_dir:
        for file in os.listdir(raw_files):
            os.remove(os.path.join(raw_files, file))
        await message.reply_text("✅ **𝐷𝐸𝐿𝐸𝑇𝐸𝐷 𝐴𝐿𝐿 𝑅𝐴𝑊 𝐹𝐼𝐿𝐸𝑆**")
    else:
        await message.reply_text("❌ **𝑁𝑂 𝑅𝐴𝑊 𝐹𝐼𝐿𝐸𝑆**")


@Client.on_message(filters.command(["cleanup"], prefixes=["/", "!"]))
@errors
@sudo_users_only
async def cleanup(_, message: Message):
    pth = os.path.realpath(".")
    ls_dir = os.listdir(pth)
    if ls_dir:
        for dta in os.listdir(pth):
            os.system("rm -rf *.webm *.jpg")
        await message.reply_text("✅ **𝐶𝐿𝐸𝐴𝑁𝐸𝐷**")
    else:
        await message.reply_text("✅ **𝐴𝐿𝑅𝐸𝐴𝐷𝑌 𝐶𝐿𝐸𝐴𝑁𝐸𝐷**")
