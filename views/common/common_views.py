# coding:utf-8
from views.base_views.base_views import BaseHandler
from utils.rhj_captcha.rhj_captcha import Captcha
from cStringIO import StringIO

class GraphCaptchaHandler(BaseHandler):
    def get(self):
        text,image=Captcha.gene_code()
        self.redis.set(text.lower(),text.lower(),3*60)
        outer=StringIO()
        image.save(outer,'jpeg')
        content=outer.getvalue()
        self.set_header('Content-Type','image/jpg')
        self.write(content)
