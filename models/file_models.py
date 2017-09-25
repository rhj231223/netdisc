# coding:utf-8
from uuid import uuid4
from datetime import datetime
from string import printable

from sqlalchemy import (Column,
    Integer,String,Text,DateTime,Boolean,ForeignKey)
from sqlalchemy.orm import relationship

from models.base_models import Base,BaseModel,db_session
from utils.hash_utils import hash_data

class File(Base,BaseModel):
    __tablename__='file'

    id=Column(Integer,primary_key=True,autoincrement=True)
    uuid=Column(String(100),unique=True,default=lambda :str(uuid4()))
    name=Column(String(100),nullable=False)
    create_time=Column(DateTime,default=datetime.now)
    content_type=Column(String(50),nullable=False)
    size=Column(String(50),nullable=False)
    _file_hash=Column(String(100),nullable=False,unique=True)
    download_num=Column(Integer,default=0)
    is_removed=Column(Boolean,default=False)
    upload_user=Column(String(50),nullable=False)

    permission_id=Column(Integer,ForeignKey('permission.id'))

    permission=relationship('Permission',backref='files')

    @property
    def file_hash(self):
        return self._file_hash

    @file_hash.setter
    def file_hash(self,value):
        self._file_hash=hash_data(value)

    @classmethod
    def file_existed(cls,other):
        other_hash=hash_data(other)
        return cls.by_field_first(_file_hash=other_hash)

