import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


db_name = 'peliculas.sqlite'
base_dir = os.path.dirname(os.path.realpath(__file__))
db_url = f"sqlite:///{os.path.join(base_dir, db_name)}"

engine = create_engine(db_url, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()