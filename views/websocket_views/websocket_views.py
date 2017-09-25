# coding:utf-8
from datetime import datetime


from tornado import escape


from views.base_views.base_views import BaseWSHandler

class MessageWSHandler(BaseWSHandler):
    users=set()
    cache=[]
    cache_size=5


    def get_compression_options(self):
        return {}

    def open(self):
        if self not in MessageWSHandler.users:
            MessageWSHandler.users.add(self)
        print MessageWSHandler.users

    def on_close(self):
        if self in MessageWSHandler.users:
            MessageWSHandler.users.remove(self)

    @classmethod
    def update_cache(cls,message):
        cls.cache.append(message)
        if len(cls.cache)>cls.cache_size:
            cls.cache=cls.cache[-cls.cache_size:]

    @classmethod
    def send_update(cls,message,self):
        for user in cls.users:
            if user!=self:
                try:
                    user.write_message(message)
                except Exception as e:
                    print e

    def on_message(self,message):
        print '--------------onmessage-----------'
        msg=escape.json_decode(message)
        print '---------'
        print msg
        print self.current_user.avatar
        print '---------'
        msg.update({'avatar':'/static/images/useravatars/'+self.current_user.avatar,
                        'datetime':datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
        MessageWSHandler.update_cache(msg)
        MessageWSHandler.send_update(msg,self)

