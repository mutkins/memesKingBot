from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


# Declarative method
engine = create_engine("sqlite:////var/lib/jenkins/jobs_db/king_of_memes.db", echo=True)
Base = declarative_base()


