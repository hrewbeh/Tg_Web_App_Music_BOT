from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Model(DeclarativeBase):
    pass


class User(Model):
    __tablename__ = 'user_muse'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)


class Muse(Model):
    __tablename__ = 'muse_muse'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(primary_key=True)
    muse_id: Mapped[int] = mapped_column(primary_key=True)
