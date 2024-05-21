from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


# Declarative method
engine = create_engine("sqlite:////etc/tg_bots_data/king_of_memes.db", echo=True)
Base = declarative_base()


