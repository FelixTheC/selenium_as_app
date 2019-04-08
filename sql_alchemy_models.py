#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: felix
"""
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.attributes import InstrumentedAttribute
import re
import gc

from sql_alchemy_declare import Base, Credentials, TestObjects, TestUrls


class MetaModel(type):
    def __new__(cls, name, bases, dct):
        try:
            obj = dct['Meta'].obj
        except KeyError:
            pass
        try:
            obj = dct['obj']
        except KeyError:
            pass
        fields = list([i for i in dir(obj) if '__' not in i and i[0] != '_' and isinstance(getattr(obj, i), InstrumentedAttribute)])
        new_obj = super().__new__(cls, name, bases, dct)
        new_obj.fields = fields
        new_obj.session = sessionmaker()
        new_obj.obj = obj
        engine = create_engine('sqlite:///selenium_tests.db')
        new_obj.session.configure(bind=engine)
        for field in fields:
            setattr(new_obj, field, None)
        return new_obj


class ModelBase(metaclass=MetaModel):
    obj = None

    def __init__(self, **kwargs):
        if len(kwargs) != 0:
            try:
                self._create(**kwargs)
            except KeyError as e:
                raise ValueError(f'{e} can\'t be None')
            except IntegrityError as e:
                raise KeyError(e)
        super(ModelBase, self).__init__()

    def __setattr__(self, key, value):
        super(ModelBase, self).__setattr__(key, value)

    def __str__(self):
        if self.__check_values__() > 0:
            return f'{self.obj.__class__.__name__}: {self.obj}'
        else:
            return ''

    def __repr__(self):
        if self.__check_values__() > 0:
            return f'{self.obj}'
        else:
            return ''

    def __check_values__(self):
        return sum(list([1 for field in self.fields if getattr(self.obj, field) is not None]))

    def _create(self, **kwargs):
        session = self.session()
        new_obj = self.obj()
        for field in self.fields:
            if field != 'id':
                setattr(self, field, kwargs.__getitem__(field))
                setattr(new_obj, field, kwargs.__getitem__(field))
        session.add(new_obj)
        session.commit()

    def _update(self):
        session = self.session()
        # do magic
        session.commit()

    def _delete(self):
        session = self.session()
        # do magic
        session.commit()

    def get(self, **kwargs):
        session = self.session()
        query = session.query(self.obj).filter_by(**kwargs)
        params = {}
        counter = 1
        for i in range(1):
            for key, val in kwargs.items():
                params[f'{key}_{counter}'] = val
            counter += 1
        result = session.execute(text(str(query.__clause_element__())), params=params)
        pattern = f'{self.obj.__tablename__}_'
        fields = list([re.sub(pattern, '', i) for i in result.keys()])
        for row in result:
            for index, r in enumerate(row):
                setattr(self, fields[index], r)
        session.commit()
        return self

    def filter(self, **kwargs):
        session = self.session()
        query = session.query(self.obj).filter_by(**kwargs)
        params = {}
        counter = 1
        for i in range(1):
            for key, val in kwargs.items():
                params[f'{key}_{counter}'] = val
            counter += 1
        result = session.execute(text(str(query.__clause_element__())), params=params)
        pattern = f'{self.obj.__tablename__}_'
        fields = list([re.sub(pattern, '', i) for i in result.keys()])
        objs = []
        for row in result:
            data = {'obj': self.obj}
            for index, r in enumerate(row):
                data[fields[index]] = r
            objs.append(type('ModelBase', (), data))
        session.commit()
        return objs

    def all(self):
        session = self.session()
        _all = session.query(self.obj).all()
        session.commit()
        objs = []
        for a in _all:
            data = {f: a.__getattribute__(f) for f in self.fields}
            data['obj'] = self.obj
            obj = type('ModelBase', (), data)
            objs.append(obj)
        return objs

    def save(self):
        kwargs = {field: self.__getattribute__(field) for field in self.fields}
        self._create(**kwargs)


class CredentialsModel(ModelBase):
    class Meta:
        obj = Credentials

    def login(self, username, password):
        session = self.session()
        new_obj = session.query(self.obj).filter(self.obj.username == username).one()
        session.commit()
        if new_obj.password == password:
            for field in self.fields:
                setattr(self, field, new_obj.__getattribute__(field))
            return self
        else:
            return None

    def logout(self):
        for field in self.fields:
            setattr(self, field, None)
            setattr(self.obj, field, None)
        del self
        gc.collect()
        return None


class TestUrlsModel(ModelBase):
    class Meta:
        obj = TestUrls


class TestObjectsModel(ModelBase):
    class Meta:
        obj = TestObjects
