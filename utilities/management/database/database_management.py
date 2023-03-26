from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utilities.models.database_models import Base

# create engine and session maker
engine = create_engine("mysql://root@127.0.0.1:3306/Atlas")
Session = sessionmaker(bind=engine)

# create tables
Base.metadata.create_all(engine)

# create session
session = Session()


def get_session():
    return session
