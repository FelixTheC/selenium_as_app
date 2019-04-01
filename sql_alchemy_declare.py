#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: felix
"""
from sqlalchemy import Column, ForeignKey, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import PasswordType, ChoiceType

Base = declarative_base()


class Credentials(Base):
    __tablename__ = 'credentials'
    id = Column(Integer, primary_key=True)
    login_url = Column(String(500), nullable=False)
    username = Column(String(250), unique=True, nullable=False)
    password = Column(PasswordType(
        schemes=[
            'pbkdf2_sha512',
            'md5_crypt'
        ],

        deprecated=['md5_crypt']
    ), nullable=False)


class TestUrls(Base):
    __tablename__ = 'test_urls'
    id = Column(Integer, primary_key=True)
    url = Column(String(500), nullable=False)


class TestObjects(Base):
    OBJECTS = [
        (u'button', u'button'),
        (u'form', u'form'),
        (u'link', u'link'),
        (u'text', u'text'),
    ]
    OPTIONS = [
        (u'---', u'---'),
        (u'exists', u'exists'),
        (u'clickable', u'clickable'),
    ]
    __tablename__ = 'test_objects'
    id = Column(Integer, primary_key=True)
    test_object = Column(ChoiceType(OBJECTS))
    should_be = Column(ChoiceType(OPTIONS))
    compares_to = Column(String(500), nullable=False, default='-')
    test_form_values = Column(JSON(none_as_null=True))
    url_id = Column(Integer, ForeignKey('test_urls.id'))


engine = create_engine('sqlite:///selenium_tests.db', echo=True)
Base.metadata.create_all(engine)
# to write changes to the database run python sql_alchemy_declare.py
