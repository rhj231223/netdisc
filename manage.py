# coding:utf-8



from tornado import httpserver,ioloop
from tornado.web import RequestHandler,Application
from tornado.options import options,define,parse_command_line


from configs import settings
from libs.db.create_tables import run,db_session
from views.cms_views.cms_urls import cms_urls
from models.cms_models import Employee


define('port',default=21000,type=int,help='port')
define('tables',default=False,type=bool,help='create_tables')
define('create_user',default=False,type=bool,help='create_super_user')


def create_user():
    username='rhj231223'
    password='2312231223'

    db_emp=Employee.by_field_first(username=username)
    if not db_emp:
        admin_user=Employee(username=username,password=password)
        db_session.add(admin_user)
        db_session.commit()
        print u'恭喜 %s 用户创建成功' %username
    else:
        print u'该用户已存在'


if __name__=='__main__':
    parse_command_line()

    if options.tables:
        run()
    if options.create_user:
        create_user()


    app=Application(
        handlers=cms_urls,**settings
    )

    http_server=httpserver.HTTPServer(app)
    http_server.listen(options.port)
    ioloop.IOLoop.instance().start()

