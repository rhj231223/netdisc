# coding:utf-8
from ui import uimethods,uimodules


settings=dict(
    template_path='templates',
    static_path='static',
    debug=True,
    cookie_secret='rhj',
    xsrf_cookies=True,
    login_url='/front/login/',
    ui_methods=uimethods,
    ui_modules=uimodules,

    pycket=dict(
        engine='redis',
        storage=dict(
            host='127.0.0.1',
            port=6379,
            db_sessions=6,
            db_notifications=11,
            max_connections=2**31,
        ),
        cookies=dict(
            max_age=60*60*24
        ),
    ),

)