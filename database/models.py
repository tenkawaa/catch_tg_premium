from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from sqlalchemy import BigInteger, MetaData, String

class Base(DeclarativeBase): ...

metadata = MetaData()


class Chat(Base):
    __tablename__ = "chats"

    hash_id: Mapped[str] = mapped_column(String, primary_key=True)
    chat_id: Mapped[int] = mapped_column(BigInteger)
    user_id: Mapped[int] = mapped_column(BigInteger)
    end_time: Mapped[int] = mapped_column(BigInteger)