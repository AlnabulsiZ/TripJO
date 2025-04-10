from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import CheckConstraint, func, UniqueConstraint

engine = create_engine('sqlite:///./Tasheh.db', echo=True) # echo=True => debug mode
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Fname = Column(String, nullable=False)
    Lname = Column(String , nullable=False)
    Email = Column(String , unique=True, nullable=False)
    Phone = Column(String, nullable=False)
    Password = Column(String, nullable= False, unique=True)
    Role = Column(String, nullable=False)
    ResetCode = Column(String, default=None)
    NationalId = Column(String, unique=True)
    PersonalImage = Column(String)
    Gender = Column(String)
    Age = Column(Integer)
    Rate = Column(Float, default=0.0)
    CreatedAt = Column(DateTime, default=func.current_timestamp)


    __table_args__ =(
        CheckConstraint("Role IN ('user', 'owner', 'guide')", name='role_check'),
        CheckConstraint("Gender IN ('male', 'female')", name='gender_check'),
        CheckConstraint("age > 0", name='age_check'),
        CheckConstraint("rate >= 0.0 AND rate <= 5.0", name='rate_check'),
    )


class Place(Base):
    __tablename__ = 'places'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String, nullable=False)
    City = Column(String, nullable=False)
    Type = Column(String, nullable=False)
    Description = Column(String)
    Rate = Column(Float, default=0.0)
    OwnerId = Column(Integer, ForeignKey('users.Id', ondelete='CASCADE'), nullable=True)
    OwnerPlaceRelationShip = relationship('place', backref='user')
    images = relationship('Image', back_populates='place', cascade="all, delete-orphan")




    __table_args__ =(
        CheckConstraint("rate >= 0.0 AND rate <= 5.0", name='rate_check'),
    )



class Image(Base):
    __tablename__= 'Images'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    PlaceId = Column(Integer, nullable= False)
    ImagePath = Column(String, nullable=False, unique=True)
    IsMain = Column(Boolean, default= False)
    CreatedAt = Column(DateTime, default=func.current_timestamp)
    PlaceId = Column(Integer, ForeignKey('places.Id', ondelete='CASCADE'), nullable=False)
    place = relationship('Place', back_populates='images')



class Favorites(Base):
    __tablename__ = 'favorites'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    UserId = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    PlaceId = Column(Integer, ForeignKey('places.id', ondelete='CASCADE'), nullable=False)
    GuideId = Column(Integer, ForeignKey('guides.id', ondelete='CASCADE'), nullable=False)
    CreatedAt = Column(DateTime, default=func.current_timestamp)

    User = relationship('User', backref='favorites')
    Place = relationship('Place', backref='favorites')
    Guide = relationship('Guide', backref='favorites')

    __table_args__ = (
        UniqueConstraint('user_id', 'place_id', name='unique_user_place'),
    )


class Comment(Base):
    __tablename__ = 'comments'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    PlaceId = Column(Integer, ForeignKey('places.id', ondelete='CASCADE'), nullable=False)
    Comment = Column(String, nullable=False)

    Place = relationship('Place', backref='comments')


class Message(Base):
    __tablename__ = 'messages'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    ChatId = Column(Integer, ForeignKey('chats.id', ondelete='CASCADE'), nullable=False)
    SenderId = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    Message = Column(String, nullable=False)
    CreatedAt = Column(DateTime, default=func.current_timestamp)

    Chat = relationship('Chat', backref='messages')
    Sender = relationship('User', backref='messages')


class Chat(Base):
    __tablename__ = 'chats'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    UserId = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    GuideId = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    PlaceId = Column(Integer, ForeignKey('places.id', ondelete='CASCADE'))
    CreatedAt = Column(DateTime, default=func.current_timestamp)

    User = relationship('User', backref='chats')
    Guide = relationship('User', backref='guides', foreign_keys=[GuideId])
    Place = relationship('Place', backref='chats')


Session = sessionmaker(bind=engine)
session = Session()


if __name__ == "__main__":
    Base.create_all(engine)