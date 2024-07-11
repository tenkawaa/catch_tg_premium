import os
import asyncio

from pyrogram import Client, idle
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from loguru import logger

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
        logger.warning("no sessions found, let's create a new one")
        if 0 in (config.api_hash, config.api_id):
            logger.warning("the api_id and api_hash fields are missing")
            logger.info("please get them using https://my.telegram.org/apps")
            config.api_id = input("Api Id: ")
            config.api_hash = input("Api Hash: ")

        phone_number = input("enter the phone number: ")
        if phone_number.startswith("7"): phone_number = "+" + phone_number
        if phone_number.startswith("8"): phone_number = "+7" + phone_number[1:]

        new_session = Client(
            name="sessions/first_session",
            api_id=config.api_id,
            api_hash=config.api_hash,
            phone_number=phone_number,
            device_model="HUAWEISTK-LX1",
            system_version="SDK 29",
            app_version="10.5.0 (42285)",
            lang_pack="android",
            hide_password=True,
            plugins=dict(root="plugins")
        )
        await new_session.start()
        await new_session.stop()
        sessions.append("first_session")
        
        

    scheduler.add_job(
        func=check_giveaway,
        trigger=IntervalTrigger(minutes=15)
    )
    scheduler.start()

    await asyncio.gather(*[start(session) for session in sessions])
    await idle()


if __name__ == "__main__":
    asyncio.run(main())