#!/usr/bin/python3

import os
from sqlalchemy import create_engine
from models.base_model import Base
from sqlalchemy.orm import sessionmaker, scoped_session
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    """database storage engine"""
    __engine = None
    __session = None

    def __init__(self):
        """initialization instance method"""
        USER = os.environ.get('HBNB_MYSQL_USER')
        PWD = os.environ.get('HBNB_MYSQL_PWD')
        DB = os.environ.get('HBNB_MYSQL_DB')
        HOST = os.environ.get('HBNB_MYSQL_HOST')
        ENV = os.environ.get('HBNB_EMV')

        db_url = f'mysql+mysqldb://{USER}:{PWD}@{HOST}/{DB}'

        self.__engine = create_engine(db_url, pool_pre_ping=True)
        if ENV == 'test':
            Base.metadata.drop_all()

    def all(self, cls=None):
        """query on the current database session (self.__session)
        all objects depending of the class name (argument cls)"""
        new_dict = {}
        if cls is None:
            class_list = ['User', 'State', 'City', 'Amenity', 'Review']
            for item in class_list:
                result = self.__session.query(eval(item))
                key = f'{item}.{eval(item).id}'
                new_dict[key] = result
        else:
            result = self.__session.query(cls)
            key = f'{cls.__class__.__name__}.{cls.id}'
            new_dict[key] = result

        return new_dict

    def new(self, obj):
        """adds the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the databas"""
        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)

        Session = scoped_session(session_factory)
        self.__session = Session()
