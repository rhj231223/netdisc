# coding:utf-8
from datetime import datetime
import pickle
import json


from libs.db.db_session import db_session,Base


class BaseModel(object):

    @classmethod
    def all(cls):
        return db_session.query(cls).all()

    @classmethod
    def by_id(cls,id):
        return db_session.query(cls).filter_by(id=id).first()

    @classmethod
    def by_field_first(cls,**kwargs):
        return db_session.query(cls).filter_by(**kwargs).first()

    @classmethod
    def by_field_all(cls, **kwargs):
        return db_session.query(cls).filter_by(**kwargs).all()


    def to_dict(self):
        columns=self.__table__.columns
        dic=[]
        for column in columns:
            value=getattr(self,column.name)
            if isinstance(value,datetime):
                value=value.strftime('%Y-%m-%d %H:%M:%S')
            dic[column.name]=value
        return dic

    def to_pickle(self):
        key=self.__class__.__name__+self.id
        value=pickle.dump(self)
        return {key:value}

