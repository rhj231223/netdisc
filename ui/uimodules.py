# coding:utf-8
from tornado.web import UIModule

class AlertMessage(UIModule):
    def render(self, message):
        context=dict(message=message)
        return self.render_string('ui_modules/alert_message.html',**context)
