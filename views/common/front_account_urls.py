# coding:utf-8
import front_account_views as front_account

front_account_urls=[
    (r'/front/regist/',front_account.FrontRegistHandler),
    (r'/front/login/',front_account.FrontLoginHanlder),
]

