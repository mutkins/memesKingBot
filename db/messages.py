from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData, ForeignKey, exc, DateTime
from sqlalchemy.orm import mapper, relationship, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from logger import log
from sqlalchemy.types import Boolean
from db.db_init import Base, engine
from sqlalchemy import func
from sqlalchemy import desc, asc


class Messages(Base):
    __tablename__ = 'Messages'
    id = Column(String(250), primary_key=True)
    from_chat_id = Column(String(250), ForeignKey("Users.chat_id"))
    message_id = Column(Integer)
    date = Column(DateTime)
    chat_id = Column(String(250))
    count_of_likes = Column(Integer)
    content_type = Column(String(250))
    file_id = Column(String(250))
    new_message_id = Column(Integer)

    def __init__(self, from_chat_id, message_id, date, chat_id, content_type, file_id):
        self.id = str(chat_id) + '_' + str(message_id)
        self.from_chat_id = from_chat_id
        self.message_id = message_id
        self.date = date
        self.chat_id = chat_id
        self.count_of_likes = 0
        self.content_type = content_type
        self.file_id = file_id


def add_msg_to_db(from_chat_id, message_id, date, chat_id, content_type, file_id):
    new_msg = Messages(from_chat_id=from_chat_id, message_id=message_id, date=date, chat_id=chat_id, content_type=content_type, file_id=file_id)

    with Session(engine) as session:
        session.expire_on_commit = False
        try:
            session.add(new_msg)
            session.commit()
            return new_msg.id
        except exc.IntegrityError as e:
            # return error if something went wrong
            session.rollback()
            log.error(e)
            raise e


def get_msg_from_db_by_id(id):
    with Session(engine) as session:
        # session.expire_on_commit = False
        try:
            return session.query(Messages).filter_by(id=id).first()
        except exc.IntegrityError as e:
            # return error if something went wrong
            session.rollback()
            log.error(e)
            raise e


def like_db_message(msg_id):
    with Session(engine) as session:
        # session.expire_on_commit = False
        try:
            msg = session.query(Messages).filter_by(id=msg_id).first()
            msg.count_of_likes += 1
            session.commit()
            return msg.count_of_likes
        except exc.IntegrityError as e:
            # return error if something went wrong
            session.rollback()
            log.info(e)
            raise e


def get_id_user_has_the_most_likes(chat_id, date_from=None):
    with Session(engine) as session:
        # session.expire_on_commit = False
        try:
            if date_from:
                res = session.query(Messages.from_chat_id, func.sum(Messages.count_of_likes)).\
                    filter_by(chat_id=chat_id).filter(Messages.date >= date_from).group_by(Messages.from_chat_id).\
                    order_by(desc(func.sum(Messages.count_of_likes))).first()
            else:
                res = session.query(Messages.from_chat_id, func.sum(Messages.count_of_likes)).\
                    filter_by(chat_id=chat_id).group_by(Messages.from_chat_id).\
                    order_by(desc(func.sum(Messages.count_of_likes))).first()
            return res
        except exc.IntegrityError as e:
            # return error if something went wrong
            session.rollback()
            log.error(e)
            raise e


def get_all_chat_id():
    with Session(engine) as session:
        # session.expire_on_commit = False
        try:
            return session.query(Messages.chat_id).group_by(Messages.chat_id).all()
        except exc.IntegrityError as e:
            # return error if something went wrong
            session.rollback()
            log.error(e)
            raise e


def add_new_message_id(msg_id, new_message_id):
    with Session(engine) as session:
        # session.expire_on_commit = False
        try:
            msg = session.query(Messages).filter_by(id=msg_id).one()
            msg.new_message_id = new_message_id
            session.commit()
            return msg.count_of_likes
        except exc.IntegrityError as e:
            # return error if something went wrong
            session.rollback()
            log.info(e)
            raise e


def get_the_most_liked_message(chat_id, date_from=None):
    with Session(engine) as session:
        # session.expire_on_commit = False
        try:
            msg = session.query(Messages.from_chat_id, Messages.count_of_likes, Messages.new_message_id).filter_by(chat_id=chat_id)
            if date_from:
                msg = msg.filter(Messages.date >= date_from)
            msg = msg.order_by(desc(Messages.count_of_likes)).order_by(desc(Messages.date)).first()

            return msg
        except exc.IntegrityError as e:
            # return error if something went wrong
            session.rollback()
            log.error(e)
            raise e