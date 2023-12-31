from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData, UniqueConstraint, exc, DateTime
from sqlalchemy.orm import mapper, relationship, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from logger import log
from sqlalchemy.types import Boolean
from db.db_init import Base, engine


class Users(Base):
    __tablename__ = 'Users'
    chat_id = Column(String(250), primary_key=True)
    first_name = Column(String(250))
    last_name = Column(String(250))
    username = Column(String(250))
    mention = Column(String(250))
    was_a_king = Column(Integer)

    def __init__(self, chat_id, first_name, last_name, username, mention):
        self.chat_id = chat_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.mention = mention
        self.was_a_king = 0

def add_user_to_db(chat_id, first_name, last_name, username, mention):
    new_user = Users(chat_id=chat_id, first_name=first_name, last_name=last_name, username=username, mention=mention)

    with Session(engine) as session:
        session.expire_on_commit = False
        try:
            session.add(new_user)
            session.commit()
            return None
        except exc.IntegrityError as e:
            # return error if something went wrong
            session.rollback()
            log.error(e)
            raise e


def get_user_from_db_by_chat_id(chat_id):
    with Session(engine) as session:
        # session.expire_on_commit = False
        try:
            return session.query(Users).filter_by(chat_id=chat_id).first()
        except exc.IntegrityError as e:
            # return error if something went wrong
            session.rollback()
            log.error(e)
            raise e


def incr_was_a_king(chat_id):
    with Session(engine) as session:
        # session.expire_on_commit = False
        try:
            user = session.query(Users).filter_by(chat_id=chat_id).first()
            user.was_a_king += 1
            session.commit()
        except exc.IntegrityError as e:
            # return error if something went wrong
            session.rollback()
            log.info(e)
            raise e
