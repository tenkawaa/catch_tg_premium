import time
import uuid

from sqlalchemy import select, delete

from .db import async_session
from .models import Chat


async def get_chats(user_id: int) -> list[list[int], list[int]]:
    current_time = int(time.time())
    async with async_session as session:
        chats = (await session.execute(
            select(Chat)
            .where(Chat.user_id == user_id, Chat.end_time < current_time)
        )).scalars()
        chat_dont_leave = (await session.execute(
            select(Chat)
            .where(Chat.user_id == user_id, Chat.end_time > current_time)
        )).scalars()
        
        
        return [[i.chat_id for i in chats.all()], [i.chat_id for i in chat_dont_leave.all()]]


async def new_chat(chat_ids: list[int], user_id: int, end_time: int):
    end_time = end_time + 30*60
    async with async_session as session:
        for chat_id in chat_ids:
            chat = Chat(hash_id=str(uuid.uuid4()), user_id=user_id, chat_id=chat_id, end_time=end_time)
            session.add(chat)
        await session.commit()

async def delete_chat(chat_ids: list[int]) -> None:
    current_time = int(time.time())
    for chat in chat_ids:
        print(chat)
        async with async_session as session:
            await session.execute(
                delete(Chat)
                .where(Chat.chat_id == chat, Chat.end_time < current_time)
            )
            await session.commit()

