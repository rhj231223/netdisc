# coding:utf-8


from tornado.web import RequestHandler
from libs.pycket.session import SessionMixin
from tornado.websocket import WebSocketHandler

from libs.db.db_session import db_session
from libs.cache.redis_cache import redis
from constants import FRONT_SESSION_ID,CMS_SESSION_ID
from models.front_models import User
from models.cms_models import Employee

class BaseHandler(RequestHandler,SessionMixin):
    def initialize(self):
        self.db=db_session
        self.redis=redis
        self.message=[]

class BaseWSHandler(WebSocketHandler,SessionMixin):
    def open(self):
        pass

    def on_message(self, message):
        pass

    def on_close(self):
        pass

    def get_current_user(self):
        id=self.session.get(FRONT_SESSION_ID)
        if not id:
            return None
        else:
            user=User.by_id(id)
            if not user:
                return None
            else:
                self.current_user=user
                return self.current_user


class FrontBaseHandler(BaseHandler):
    def get_current_user(self):
        id=self.session.get(FRONT_SESSION_ID,'')
        if not id:
            return None
        else:
            user = User.by_id(id)
            if not user:
                return None
            else:
                self.current_user=user
                return self.current_user

class CMSBaseHandler(BaseHandler):
    def get_current_user(self):
        id=self.session.get(CMS_SESSION_ID,'')
        if not id:
            return None
        else:
            employee = Employee.by_id(id)
            if not employee:
                return None
            else:
                self.current_user=employee
                return self.current_user