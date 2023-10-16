from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData, UniqueConstraint, exc, DateTime, ForeignKey
from sqlalchemy.orm import mapper, relationship, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from logger import log
from sqlalchemy.types import Boolean
from db.db_init import Base, engine


class Likes(Base):
    __tablename__ = 'Likes'
    id = Column(Integer, primary_key=True)
    from_user_chat_id = Column(String(250), ForeignKey("Users.chat_id"))
    msg_id = Column(String(250), ForeignKey("Messages.id"))
    __table_args__ = (UniqueConstraint('msg_id', 'from_user_chat_id', name='unique_msg_id_from_user_chat_id'),)

    def __init__(self, from_user_chat_id, msg_id):
        self.from_user_chat_id = from_user_chat_id
        self.msg_id = msg_id


def add_like_to_db(from_user_chat_id, msg_id):
    new_like = Likes(from_user_chat_id=from_user_chat_id, msg_id=msg_id)

    with Session(engine) as session:
        session.expire_on_commit = False
        try:
            session.add(new_like)
            session.commit()
            return None
        except exc.IntegrityError as e:
            # return error if something went wrong
            session.rollback()
            log.warning(f'User {from_user_chat_id} already liked message {msg_id}')
            raise e

