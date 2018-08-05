from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
import json
from .Base import Base

class ItemCategory(Base):
  __tablename__ = 'item_category'

  id = Column(Integer, primary_key=True)
  name = Column(String(128), nullable=False, unique=True)

  def serialize(self):
    return {
      'id': self.id,
      'name': self.name,
    }

  def __str__(self):
    return json.dumps(self.serialize(), indent=2)
    