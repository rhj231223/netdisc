# coding:utf-8
from uuid import uuid4
from datetime import datetime
from string import printable

from sqlalchemy import (Column,
    Integer,String,Text,DateTime,Boolean,ForeignKey)
from sqlalchemy.orm import relationship
from pbkdf2 import PBKDF2

from base_models import Base,BaseModel

class Handler(Base,BaseModel):
    __tablename__='handler'

    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(50),nullable=False)


    permission_id=Column(Integer,ForeignKey('permission.id'),unique=True)
    permission=relationship('Permission',uselist=False)

class Menu(Base,BaseModel):
    __tablename__='menu'

    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(50),nullable=True)

    permission_id=Column(Integer,ForeignKey('permission.id'),unique=True)
    permission=relationship('Permission',uselist=False)


class PermissionToRole(Base,BaseModel):
    __tablename__='permission_to_role'

    permission_id=Column(Integer,ForeignKey('permission.id'),primary_key=True)
    role_id=Column(Integer,ForeignKey('role.id'),primary_key=True)

class Permission(Base,BaseModel):
    __tablename__='permission'

    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(50),nullable=False)
    desc=Column(String(50))
    p_code=Column(String(50),unique=True,nullable=False)

    menu=relationship('Menu',uselist=False)
    handler=relationship('Handler',uselist=False)

class EmployeeToRole(Base,BaseModel):
    __tablename__='employee_to_role'

    employee_id=Column(Integer,ForeignKey('employee.id'),primary_key=True)
    role_id=Column(Integer,ForeignKey('role.id'),primary_key=True)



class Role(Base,BaseModel):
    __tablename__='role'

    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(50),nullable=False)
    desc=Column(String(50))

    employees=relationship('Employee',secondary='employee_to_role',backref='roles')
    permissions=relationship('Permission',secondary='permission_to_role',backref='roles')


class Employee(Base,BaseModel):
    __tablename__='employee'

    id=Column(Integer,primary_key=True,autoincrement=True)
    uuid=Column(String(50),unique=True,default=lambda:str(uuid4()))
    username=Column(String(50),nullable=False)
    _password=Column(String(100),nullable=False)
    create_time=Column(DateTime,default=datetime.now)
    last_login=Column(DateTime)
    login_num=Column(Integer,default=0)
    locked=Column(Boolean,default=False)
    _avatar=Column(String(64))

    def hash_password(self,raw_pwd):
        return PBKDF2.crypt(raw_pwd,iterations=0x2537)

    def check_password(self,raw_pwd):
        if not raw_pwd:
            return None
        return self._password==PBKDF2.crypt(raw_pwd,self.password)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,value):
        self._password=self.hash_password(value)

    @property
    def avatar(self):
        return self._avatar if self._avatar else '/static/images/useravatars/default_avatar.jpeg'

    @avatar.setter
    def avatar(self, image_data):
        class ValidationError(Exception):
            def __init__(self, message):
                super(ValidationError, self).__init__(message)

        if 64 < len(image_data) < 1024 * 1024:
            import imghdr
            import os
            ext = imghdr.what("", h=image_data)
            print ext
            print self.uuid
            if ext in ['png', 'jpeg', 'gif', 'bmp', 'jpg'] and not self.is_xss_image(image_data):
                if self._avatar and os.path.exists("static/images/useravatars/" + self._avatar):
                    os.unlink("static/images/useravatars/" + self._avatar)
                file_path = str("static/images/useravatars/" + self.uuid + '.' + ext)
                with open(file_path, 'wb') as f:
                    f.write(image_data)
                self._avatar = self.uuid + '.' + ext
            else:
                raise ValidationError("not in ['png', 'jpeg', 'gif', 'bmp','jpg']")
        else:
            raise ValidationError("64 < len(image_data) < 1024 * 1024 bytes")

    def is_xss_image(self, data):
        return all([char in printable for char in data[:16]])
