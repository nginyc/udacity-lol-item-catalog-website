from .Base import Base
from .User import User
from .ItemCategory import ItemCategory 
from sqlalchemy import Column, Integer, Text, String, ForeignKey
from sqlalchemy.orm import relationship

class ItemToItemCategory(Base):
  __tablename__ = 'item_to_item_category'

  item_id = Column(Integer, ForeignKey('item.id'), primary_key=True)
  item_category_id = Column(Integer, ForeignKey('item_category.id'), primary_key=True)

  @property
  def serialize(self):
    return {
      'item_id': self.item_id,
      'item_category_id': self.item_category_id
    }