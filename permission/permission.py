# coding:utf-8
from models.cms_models import (Employee
,Role,Permission,Handler,Menu)
from models.file_models import File

dic=dict(handler=Handler,menu=Menu,file=File)

class HasPermission(object):
    def __init__(self):
        for k,v in dic.iteritems():
            setattr(self,k,v)
        self.user_permission=set()

    def __call__(self,user,func_name,type_name):
        return self.has_permission(user,func_name,type_name)

    def _user_has_permission(self,user):
        for role in user.roles:
            self.user_permission.update(role.permissions)
        return self.user_permission

    def _func_has_permission(self,func_name,type_name):
        if not hasattr(self,type_name):
            return None
        else:
            func=getattr(self,type_name).by_field_first(name=func_name)
            if not func:
                return None
            else:
                return func.permission

    def has_permission(self,user,func_name,type_name):
        user_permissions=self._user_has_permission(user)
        func_permission=self._func_has_permission(func_name,type_name)
        return func_permission in user_permissions