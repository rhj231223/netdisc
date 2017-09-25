# coding:utf-8
import  cms_account_views as cms_account

cms_account_urls=[
    (r'^/cms/login/$', cms_account.CMSLoginHandler),
    (r'^/cms/lock_screen/$', cms_account.CMSLockScreenHandler),
    (r'^/cms/logout/$', cms_account.CMSLogoutHandler),
]