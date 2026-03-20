from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
import enum

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(100), nullable=False)
    lastname: Mapped[str] = mapped_column(String(100), nullable=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)

    posts: Mapped[List['Post']] = relationship(back_populates="author")
    comments: Mapped[List['Comment']] = relationship(back_populates='author')

    followers: Mapped[List['Follower']] = relationship(
        foreign_keys="Follower.user_to_id", back_populates='followed')
    following: Mapped[List['Follower']] = relationship(
        foreign_keys="Follower.user_from_id", back_populates='follower')

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
        }


class Follower(db.Model):
    user_from_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'), primary_key=True)

    follower: Mapped['User'] = relationship(
        foreign_keys=[user_from_id], back_populates='following')
    followed: Mapped['User'] = relationship(
        foreign_keys=[user_to_id], back_populates='followers')

    def serialize(self):
        return {
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id
        }


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    author: Mapped['User'] = relationship(back_populates='posts')
    media: Mapped[List['Media']] = relationship(back_populates='post')
    comments: Mapped[List['Comment']] = relationship(back_populates='post')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
        }


class MediaType(enum.Enum):
    IMAGE = 'image'
    VIDEO = 'video'
    AUDIO = 'audio'


class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MediaType] = mapped_column(
        Enum(MediaType), nullable=False, default=MediaType.IMAGE)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))

    post: Mapped['Post'] = relationship(back_populates='media')

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type.value,
            "url": self.url,
            "post_id": self.post_id
        }


class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))

    author: Mapped['User'] = relationship(back_populates='comments')
    post: Mapped['Post'] = relationship(back_populates='comments')

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id,
        }
