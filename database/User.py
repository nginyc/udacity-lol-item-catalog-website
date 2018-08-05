import json
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .Base import Base

class User(Base):
  __tablename__ = 'user'

  id = Column(Integer, primary_key=True)
  name = Column(String(128), nullable=False)
  profile_image_url = Column(String(256))
  email = Column(String(128), unique=True)

  def serialize(self):
    return {
      'id': self.id,
      'name': self.name,
      'profile_image_url': self.profile_image_url,
      'email': self.email
    }

  def __str__(self):
    return json.dumps(self.serialize(), indent=2)