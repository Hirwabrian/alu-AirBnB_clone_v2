#!/usr/bin/python3
""" State Module for HBNB project """
import models
from models import city
from models.base_model import BaseModel,Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

class State(BaseModel, Base):
    """ State class """
    name =Column(String(128), nullable=False)
    cities = relationship('City', backref='state', cascade='all, delete')

    @property
    def cities(self):
        values_city = models.storage.all("City").values()
        list= []
        for city in values_city:
            if city.state_id == self.id:
                list.append(city)
        return list