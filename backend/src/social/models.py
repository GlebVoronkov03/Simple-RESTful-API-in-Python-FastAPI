import uuid
from datetime import datetime

from sqlalchemy import (TIMESTAMP, UUID, Column, ForeignKey, Integer, String,
                        select)
from sqlalchemy.orm import relationship

from ..db import Base

UUID_ID = uuid.UUID


class Like(Base):
    __tablename__ = "likes"

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", UUID, ForeignKey("users.id"))
    post_id = Column("post_id", Integer, ForeignKey("posts.id"))


class Post(Base):
    __tablename__ = "posts"

    id: int = Column("id", Integer, primary_key=True)
    title: str = Column("title", String)
    text: str = Column("text", String)
    author_id: UUID_ID = Column("author_id", UUID, ForeignKey("users.id"))
    date: datetime = Column("date", TIMESTAMP, default=datetime.now)
    slug: str = Column("slug", String, unique=True)

    author = relationship("User", back_populates="my_posts")
    users = relationship("User", secondary="likes", back_populates="posts")

    async def like_post(self, session, user):

        like = await session.execute(
            select(Like).filter_by(post_id=self.id, user_id=user.id)
        )
        existing_like = like.scalars().first()

        if existing_like:
            await session.delete(existing_like)
            like = False
        else:
            new_like = Like(post_id=self.id, user_id=user.id)
            session.add(new_like)
            like = True
        await session.commit()
        return {'like': like}
