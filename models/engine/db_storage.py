#!/usr/bin/python3
""" new storge database class for sqlAlchemy """

import os
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base

class DBStorage:
    "setting up storage"
    __engine = None
    __session = None

    def __init__(self):
        """Create engine and link to the database."""
        user = os.getenv("HBNB_MYSQL_USER")
        passwd = os.getenv("HBNB_MYSQL_PWD")
        db = os.getenv("HBNB_MYSQL_DB")
        host = os.getenv("HBNB_MYSQL_HOST")
        env = os.getenv("HBNB_ENV")
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, db),
                                      pool_pre_ping=True)

        if os.getenv('HBNB_ENV') == "test":
            Base.metadata.drop_all(self.__engine)
    
    def all(self, cls= None):
        """returns all objects of a specific class or all objects."""
        dictionary = {}
        if cls:
            objs = self.__session.query(cls).all()
        else:
            states = self.__session.query(State).all()
            cities = self.__session.query(City).all()
            users = self.__session.query(User).all()
            places = self.__session.query(Place).all()
            reviews = self.__session.query(Review).all()
            amenities = self.__session.query(Amenity).all()

            objs = states + cities + users + places + reviews + amenities
        for obj in objs:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            dictionary[key] = obj
        return dictionary
    
    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()
    
    def delete(self, obj=None):
        """Delete object from the database."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reloads the database and creates tables."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    
