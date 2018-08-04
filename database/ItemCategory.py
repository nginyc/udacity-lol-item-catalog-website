from .Base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class ItemCategory(Base):
  __tablename__ = 'item_category'

  id = Column(Integer, primary_key=True)
  name = Column(String(128), nullable=False, unique=True)

  @property
  def serialize(self):
    return {
      'id': self.id,
      'name': self.name,
    }