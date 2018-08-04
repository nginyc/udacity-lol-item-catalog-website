from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker, scoped_session
from .Base import Base
from .Item import Item
from .ItemCategory import ItemCategory
from .ItemToItemCategory import ItemToItemCategory
from .User import User

class Database():
  def __init__(self, db_url):
    engine = create_engine(db_url)
    Base.metadata.bind = engine
    self._engine = engine

  def connect(self):
    '''
    Creates and maintains a connection to the database defined by DB_URL
    '''
    DBSession = scoped_session(sessionmaker(bind=self._engine))
    self.session = DBSession()

  def setup(self):
    '''
    Creates the database schema
    '''
    Base.metadata.create_all(self._engine)

  def disconnect(self):
    '''
    Destroys an ongoing connection to the database
    '''
    if self.session is None:
      self.session.close()
      self.session = None