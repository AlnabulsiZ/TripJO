from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import CheckConstraint, func, UniqueConstraint

engine = create_engine('sqlite:///./Tasheh.db', echo=True) # echo=True => debug mode
Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fname = Column(String, nullable=False)
    lname = Column(String , nullable=False)
    email = Column(String , unique=True, nullable=False)
    phone = Column(String, nullable=False)
    password = Column(String, nullable= False, unique=True)
    role = Column(String, nullable=False)
    reset_code = Column(String, default=None)
    national_id = Column(String, unique=True)
    personal_image = Column(String)
    gender = Column(String)
    age = Column(Integer)
    rate = Column(Float, default=0.0)
    created_at = Column(DateTime, default=func.current_timestamp)


    __table_args__ =(
        CheckConstraint("role IN ('user', 'owner', 'guide')", name='role_check'),
        CheckConstraint("gender IN ('male', 'female')", name='gender_check'),
        CheckConstraint("age > 0", name='age_check'),
        CheckConstraint("rate >= 0.0 AND rate <= 5.0", name='rate_check'),
    )


class Place(Base):
    __tablename__ = 'Places'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    type = Column(String, nullable=False)
    description = Column(String)
    rate = Column(Float, default=0.0)
    owner_id = Column(Integer, ForeignKey('users.Id', ondelete='CASCADE'), nullable=True)
    owner_place_relationship = relationship('Place', backref='User')
    images = relationship('Image', back_populates='Place', cascade="all, delete-orphan")




    __table_args__ =(
        CheckConstraint("rate >= 0.0 AND rate <= 5.0", name='rate_check'),
    )



class Image(Base):
    __tablename__= 'Images'
    id = Column(Integer, primary_key=True, autoincrement=True)
    place_id = Column(Integer, nullable= False)
    image_path = Column(String, nullable=False, unique=True)
    is_main = Column(Boolean, default= False)
    created_at = Column(DateTime, default=func.current_timestamp)
    place_id = Column(Integer, ForeignKey('places.Id', ondelete='CASCADE'), nullable=False)
    place = relationship('Place', back_populates='Image')



class Favorites(Base):
    __tablename__ = 'Favorites'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    place_id = Column(Integer, ForeignKey('places.id', ondelete='CASCADE'), nullable=False)
    guide_id = Column(Integer, ForeignKey('guides.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=func.current_timestamp)

    User = relationship('User', backref='Favorites')
    Place = relationship('Place', backref='Favorites')
    Guide = relationship('Guide', backref='Favorites')

    __table_args__ = (
        UniqueConstraint('user_id', 'place_id', name='unique_user_place'),
    )


class Comment(Base):
    __tablename__ = 'Comments'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    place_id = Column(Integer, ForeignKey('place.id', ondelete='CASCADE'), nullable=False)
    comment = Column(String, nullable=False)
    place = relationship('Place', backref='Comments')

Session = sessionmaker(bind=engine)
session = Session()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
