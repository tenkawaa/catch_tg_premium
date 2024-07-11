from datetime import datetime

from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import InviteRequestSent, FloodWait
from pyrogram import filters
from loguru import logger

from database import methods
from config import config


@Client.on_message(filters.giveaway)
async def catch_giveaway(client: Client, message: Message):
    giveaway = message.giveaway
    if giveaway.until_date < datetime.now():
        return
    if giveaway.only_for_countries and "RU" not in giveaway.only_for_countries:
        return
    
    chat_ids = []
    for chat in giveaway.chats:
        if chat.id in [-1001856700643]:
            return

        try:
            await client.join_chat(chat.id)
        except InviteRequestSent:
            pass
        except FloodWait as e:
            logger.error(f"{client.me.username}#{client.me.id} FloodWait {e.value} seconds")
        except Exception:
            for chat_id in chat_ids:
                try:
                    await client.leave_chat(chat_id)
                except: pass
            return

        chat_ids.append(chat.id)

    folder = await client.get_folders(config.FOLDER_ID)
    
    old_chats = [chat.id for chat in folder.included_chats]
    await folder.update(included_chats=old_chats + chat_ids)
    await client.archive_chats(chat_ids)

    await methods.new_chat(chat_ids, client.me.id, giveaway.until_date.timestamp())
    logger.info(f"{client.me.username}#{client.me.id} catched new giveaway; it will end {giveaway.until_date.strftime('%d/%m/%Y %H:%M:%S')}")