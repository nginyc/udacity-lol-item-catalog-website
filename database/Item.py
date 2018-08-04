from .Base import Base
from .User import User
from .ItemCategory import ItemCategory 
from sqlalchemy import Column, Integer, Text, String, ForeignKey
from sqlalchemy.orm import relationship

class Item(Base):
  __tablename__ = 'item'

  id = Column(Integer, primary_key=True)
  name = Column(String(128), nullable=False, unique=True)
  description = Column(Text(), nullable=False)
  owner_id = Column(Integer, ForeignKey('user.id'))

  @property
  def serialize(self):
    return {
      'id': self.id,
      'name': self.name,
      'description': self.description,
      'owner_id': self.owner_id
    }