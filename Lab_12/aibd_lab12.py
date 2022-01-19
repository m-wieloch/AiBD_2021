# -*- coding: utf-8 -*-
"""
Ćwiczenie
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import dialects
from sqlalchemy import Column, Integer, String, Date, ForeignKey, VARCHAR, Float, SmallInteger

db_string = "postgresql://postgres:postgres@localhost:5432/aibd_1"

engine = create_engine(db_string)

# Base = declarative_base()
#
#
# class Author(Base):
#     __tablename__ = 'authors'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50))
#     surname = Column(String(50))
#     born_date = Column(Date)
#
#     def __repr__(self):
#         return "<authors(id='{0}', name={1}, surname={2}, born_date={3})>".format(
#             self.id, self.name, self.surnamey, self.born_date)
#
#
# class Book(Base):
#     __tablename__ = 'books'
#     id = Column(Integer, primary_key=True)
#     id_author = Column(Integer, ForeignKey('authors.id'))
#     original_title = Column(String, nullable = False)
#     publication_date = Column(Integer, nullable = False)
#     original_language = Column(String(), nullable = False)
#
#
# Base.metadata.create_all(engine)

"""Zadanie"""

Base2 = declarative_base()


class Users(Base2):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(VARCHAR)

    def __repr__(self):
        return "<users(id='{0}', email={1})>".format(
            self.id, self.email)


class Hosts(Base2):
    __tablename__ = 'hosts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return "<users(id='{0}', user_id={1})>".format(
            self.id, self.user_id)
        

class Countries(Base2):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True)
    country_code = Column(VARCHAR)
    name = Column(VARCHAR)

    def __repr__(self):
        return "<users(id='{0}', country_code={1}, name={2})>".format(
            self.id, self.country_code, self.name)


class Cities(Base2):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR)
    country_id = Column(Integer, ForeignKey('countries.id'))

    def __repr__(self):
        return "<users(id='{0}', name={1}, country_id={2})>".format(
            self.id, self.name, self.country_id)


class Places(Base2):
    __tablename__ = 'places'
    id = Column(Integer, primary_key=True)
    host_id = Column(Integer, ForeignKey('hosts.id'))
    name = Column(VARCHAR)
    city_id = Column(Integer, ForeignKey('cities.id'))

    def __repr__(self):
        return "<users(id='{0}', host_id={1}, name={2}, city_id={3})>".format(
            self.id, self.host_id, self.name, self.city_id)


class Bookings(Base2):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    place_id = Column(Integer, ForeignKey('places.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    price_per_night = Column(Float)
    num_nights = Column(Integer)

    def __repr__(self):
        return "<users(id='{0}', user_id={1}, place_id={2}, start_date={3}, end_date={4}, price_per_night={5}, num_nights={6})>".format(
            self.id, self.user_id, self.place_id, self.start_date, self.end_date, self.price_per_night, self.num_nights)


class Reviews(Base2):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey('bookings.id'))
    rating = Column(SmallInteger)
    review_body = Column(String(50))

    def __repr__(self):
        return "<users(id='{0}', booking_id={1}, rating={2}, review_body={3})>".format(
            self.id, self.booking_id, self.rating, self.review_body)


Base2.metadata.create_all(engine)