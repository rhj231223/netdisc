# coding:utf-8

from views.base_views.base_views import FrontBaseHandler

class FrontRegistHandler(FrontBaseHandler):
    def get(self):
        self.render('front/front_regist.html')

    def post(self):
        pass


class FrontLoginHanlder(FrontBaseHandler):
    def get(self):
        self.render('front/front_login.html')