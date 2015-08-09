import sys

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurant'
    name = Column(String(100), nullable = False)
    id = Column(Integer, primary_key = True)
    address = Column(String(120), nullable = True)
    phone = Column(String(14), nullable = True)
    
    @property
    def serialize(self):
        return {
            'name':self.name,
            'id':self.id,
            'address':self.address,
            'phone':self.phone
        }


class MenuItem(Base):
    __tablename__ = 'menu_item'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    course = Column(String(20))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        return {
            'name':self.name,
            'description':self.description,
            'id':self.id,
            'price':self.price,
            'course':self.course
        }

engine = create_engine('sqlite:///restaurant_menu_final_project.db')

Base.metadata.create_all(engine)
