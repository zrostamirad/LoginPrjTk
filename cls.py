from sqlalchemy import create_engine, Column, String, Boolean, Text, Integer, Date, ForeignKey, select, join, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker, declarative_base, relationship

engine = create_engine("sqlite:///db.db", echo=True)
Base = declarative_base()
Sessions = sessionmaker(bind=engine)
session = Sessions()


class user(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    family = Column(String)
    age = Column(Integer)
    sex = Column(Boolean)
    is_admin = Column(Boolean, default=False)
    userpass = relationship("userpass", back_populates="user")

    def __init__(self, name="", family="", age=0, sex=True, is_admin=False):
        self.name = name
        self.family = family
        self.age = age
        self.sex = sex
        self.is_admin = is_admin


class userpass(Base):
    __tablename__ = "userpass"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    user_id = Column(Integer, ForeignKey(user.id), unique=True)
    user = relationship('user', back_populates='userpass')

    def __init__(self, username="", password="",userid=None):
        self.username = username
        self.password = password
        self.user_id=userid


class Repository():
    def Insert(self, obj):
        try:
            session.add(obj)
            session.commit()
            return ("ok")
        except:
            return ("There was an error, please try again later.")

    def SelectAll(self, obj):
        try:
            result = session.query(obj).all()
            if result:
                return result
            else:
                return ("table is Empty")
        except:
            return ("There was an error, please try again later.")

    def SelectById(self, obj, id):
        try:
            result = session.query(obj).filter(obj.id == id).first()
            if result:
                return result
            else:
                return ""
        except:
            return ("There was an error, please try again later.")

    def ShowObj(self, obj, index):
        try:
            list = self.SelectAll(obj)
            if list:
                for item in list:
                    atr = getattr(item, index)
                    return (atr)
            else:
                return ("table is Empty")
        except:
            return ("There was an error, please try again later.")

    def ShowObjById(self, obj, id, index):
        try:
            c = self.SelectById(obj, id)
            if c == "":
                return ("this id is not in table")
            else:
                atr = getattr(c, index)
                return (atr)
        except:
            return ("There was an error, please try again later.")

    def Update(self, obj, id, **keyword):
        try:
            record = self.SelectById(obj, id)
            if record:
                for key, val in keyword.items():
                    setattr(record, key, val)
                session.commit()
                return ("update id " + str(id) + " from " + str(obj.__tablename__) + "'s table is successed!")
            else:
                return ("this id is not in table")
        except:
            return ("There was an error, please try again later.")

    def Delete(self, obj, id):
        try:
            record = self.SelectById(obj, id)
            if record:
                session.delete(record)
                session.commit()
                return ("delete id " + str(id) + " from " + str(obj.__tablename__) + "'s table is successed!")
            else:
                return ("this id is not in table")
        except:
            return ("There was an error, please try again later.")


Base.metadata.create_all(engine)
