from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:////database/crypto.db', echo=True)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True)
    password = Column(String(24))
    cryptolist = Column(String(2048))  # format: "token:value;..."

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cryptolist = ""

    def __repr__(self):
        return "{}".format(self.username)
