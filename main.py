import os
import asyncio

from pyrogram import Client, idle
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from loguru import logger
from sqlalchemy import text

from config import config
from database import methods
from database.db import engine
from database.models import Base


async def check_giveaway():
    clients: list[Client] = config.clients

    for client in clients:
        chat_ids = await methods.get_chats(client.me.id)

        for chat in chat_ids[0]:
            try:
                if chat in chat_ids[1]: continue
                
                await client.leave_chat(chat)
                logger.info(f"{client.me.username}#{client.me.id} leave from {chat}")
            except: pass

        await methods.delete_chat(chat_ids[0])


async def start(session_name: str):
    client = Client("sessions/" + session_name, plugins=dict(root="plugins"))
    config.clients.append(client)

    await client.start()
    folder = await client.get_folders(config.FOLDER_ID)
    if folder is None:
        await client.update_folder(folder_id=config.FOLDER_ID, title="PremiumChats", included_chats="me", emoji="🗑")

    logger.debug(f"{client.me.username}#{client.me.id} started")


async def main():
    async with engine.connect() as session:
        await session.run_sync(Base.metadata.create_all)

    logger.add("debug.log")
    files = os.listdir("sessions")
    scheduler = AsyncIOScheduler()
    sessions = []

    for file in files:
        if file.endswith(".session"):
            sessions.append(file.replace(".session", ""))

    if not files:
        exit("No sessions found")

    scheduler.add_job(
        func=check_giveaway,
        trigger=IntervalTrigger(minutes=15)
    )
    scheduler.start()

    await asyncio.gather(*[start(session) for session in sessions])
    await idle()


if __name__ == "__main__":
    asyncio.run(main())