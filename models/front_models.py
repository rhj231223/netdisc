# coding:utf-8
from uuid import uuid4
from datetime import datetime
from string import printable

from sqlalchemy import (Column,
    Integer,String,Text,DateTime,Boolean,ForeignKey)
from sqlalchemy.orm import relationship
from pbkdf2 import PBKDF2

import cms_models
import file_models
from base_models import Base,BaseModel


class User(Base,BaseModel):
    __tablename__='user'

    id=Column(Integer,primary_key=True,autoincrement=True)
    uuid=Column(String(50),unique=True,default=lambda:str(uuid4()))
    username=Column(String(50),nullable=False)
    _password=Column(String(50),nullable=False)
    create_time=Column(DateTime,default=datetime.now)
    last_login=Column(DateTime)
    login_num=Column(Integer,default=0)
    locked=Column(Boolean,default=False)
    _avatar=Column(String(64))

    def _hash_password(self,raw_pwd):
        return PBKDF2.crypt(raw_pwd,iterations=0x2537)

    def check_password(self,raw_pwd):
        if not raw_pwd:
            return None
        return self.password==PBKDF2.crypt(raw_pwd,self.password)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,value):
        self._password=self._hash_password(value)

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

