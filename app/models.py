from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import  TIMESTAMP, ForeignKey, text
from datetime import datetime
from typing import List

class Base(DeclarativeBase):
    pass

class Post(Base):
    __tablename__ = "posts"


    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    published: Mapped[bool] = mapped_column(server_default='TRUE', nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True) , server_default=text('now()'), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    owner: Mapped["User"] = relationship(back_populates="posts")

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True) , server_default=text('now()'), nullable=False)

    posts: Mapped[List["Post"]] = relationship(back_populates="owner", cascade="all, delete-orphan")
    phone_number: Mapped[str] = mapped_column()
 
class Vote(Base):
    __tablename__ = "votes"
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), nullable=False, primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id', ondelete='CASCADE'), nullable=False, primary_key=True)