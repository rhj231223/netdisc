# coding:utf-8

from permission.permission import HasPermission

def cms_user(self):
    return self.current_user if self.current_user else None

def cms_has_permission(self,func_name,type_name):
    return HasPermission()(self.current_user,func_name,type_name)