#!/usr/bin/python3
"""Defines the DBStorage engine."""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import Base
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

class DBStorage:
    """Represents a database storage engine.
    Attributes:
        __engine (sqlalchemy.Engine): The working SQLAlchemy engine.
        __session (sqlalchemy.Session): The working SQLAlchemy session.
    """
    __engine = None
    __session = None

    def __init__(self):
        """Initializes a new DBStorage instance."""
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        HBNB_ENV = getenv("HBNB_ENV")
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(user, passwd, host, db),
                                      pool_pre_ping=True)

        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session."""
        if cls is None:
            objs = self.__session.query(User).all()
            objs += self.__session.query(State).all()
            objs += self.__session.query(City).all()
            objs += self.__session.query(Amenity).all()
            objs += self.__session.query(Place).all()
            objs += self.__session.query(Review).all()
        else:
            objs = self.__session.query(cls).all()
        return {"{}.{}".format(type(o).__name__, o.id): o for o in objs}

    def new(self, obj):
        """Adds obj to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj from the current database session."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database and initializes a new session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Call remove() method on the private session attribute."""
        self.__session.remove()
