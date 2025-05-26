import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqlite_file_name = "../database.sqlite"

# Estamos letenfo el directorio actual que es databse.py
base_dir = os.path.dirname(os.path.realpath(__file__))

# Creamos la url de la base de datos uniendo las 2 variables anteriores
database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"

engine = create_engine(database_url, echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()