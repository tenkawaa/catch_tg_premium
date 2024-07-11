from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from sqlalchemy import BigInteger, Column, Table, MetaData

class Base(DeclarativeBase): ...

metadata = MetaData()


class Chat(Base):
    __tablename__ = "chats"

    chat_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    end_time: Mapped[int] = mapped_column(BigInteger)