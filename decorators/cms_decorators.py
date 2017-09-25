# coding:utf-8
from functools import wraps



from constants import IP_POOL,IP_ADDRESS
from permission.permission import HasPermission


def cms_ip_limit(func):
    @wraps(func)
    def wrapper(self,*args,**kwargs):

        ip=self.request.remote_ip
        if ip not in IP_POOL:
            self.write(u'ip地址不符')
        else:
            return func(self,*args,**kwargs)
    return wrapper

def cms_login_required(func):
    @wraps(func)
    def wrapper(self,*args,**kwargs):
        pre_ip=self.session.get(IP_ADDRESS)
        this_ip=self.request.remote_ip
        next=self.request.path

        if not self.current_user:
            self.redirect('/cms/login/?next=%s' %next)
        elif pre_ip and pre_ip!=this_ip:
            self.writet(u'异地登录')
        else:
            return func(self,*args,**kwargs)
    return wrapper

def cms_handler_permission(func_name,type_name='handler'):
    def outer(func):
        @wraps(func)
        def wrapper(self,*args,**kwargs):
            if not HasPermission()(self.current_user,func_name,type_name):
                self.write(u'您的权限不足')
            else:
                return func(self,*args,**kwargs)
        return wrapper
    return outer