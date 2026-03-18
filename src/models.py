from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
import enum

db = SQLAlchemy()

# class User(db.Model):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
#     password: Mapped[str] = mapped_column(nullable=False)
#     is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             # do not serialize the password, its a security breach
#         }

class User(db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)

    posts: Mapped[list['Post']] = relationship(back_populates="author")
    comments: Mapped[list['Comment']] = relationship(back_populates="author")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "post_count": len(self.posts)
        }


class Follower(db.Model):
    __tablename__ = 'follower'

    user_from_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'), primary_key=True)

    def serialize(self):
        return {
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id
        }


class Post(db.Model):
    __tablename__ = 'post'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    author: Mapped["User"] = relationship(back_populates="posts")
    media: Mapped[list['Media']] = relationship(back_populates="post")
    comments: Mapped[list['Comment']] = relationship(back_populates='post')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "media": [m.serialize() for m in self.media]
        }


class MediaType(enum.Enum):
    IMAGE = 'image'
    VIDEO = 'video'
    AUDIO = 'audio'


class Media(db.Model):
    __tablename__ = 'media'

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MediaType] = mapped_column(
        Enum(MediaType), nullable=False, default=MediaType.IMAGE)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))

    post: Mapped["Post"] = relationship(back_populates="media")

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type.value,
            "url": self.url,
            "post_id": self.post_id
        }


class Comment(db.Model):
    __tablename__ = 'comment'

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))

    author: Mapped["User"] = relationship(back_populates='comments')
    post: Mapped["Post"] = relationship(back_populates='comments')

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id,
            "author": self.author.username
        }
