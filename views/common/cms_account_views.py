# coding:utf-8
from views.base_views.base_views import CMSBaseHandler
from models.cms_models import Employee
from constants import CMS_SESSION_ID,CMS_SESSION_ID_2,IP_ADDRESS
from decorators.cms_decorators import cms_login_required,cms_ip_limit

class CMSLoginHandler(CMSBaseHandler):

    def get(self,message=''):
        context=dict(message=message)
        self.render('cms/cms_login.html',**context)


    def post(self):
        user=self._verify_account()
        if not user:
            self.get(message=self.message[-1])
        else:
            self.login_success(user)


    def _verify_account(self):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        graph_captcha = self.get_argument('graph_captcha', '')
        cache_graph_captcha=self.redis.get(graph_captcha)


        user=Employee.by_field_first(username=username)

        if not graph_captcha:
            self.message.append(u'请输入验证码!')
            return False
        elif graph_captcha and graph_captcha.lower()!=cache_graph_captcha:
            self.message.append(u'验证码输入有误！')
            return False
        elif not user:
            self.message.append(u'用户名或密码错误!')
            return False
        elif user and not user.check_password(password):
            self.message.append(u'用户名或密码错误!')
            return False
        else:
            return user

    def login_success(self,user):
        remember = self.get_argument('remember', '')
        next_url=self.get_argument('next','/cms/')

        if remember:
            self.settings['pycket']['cookies']['max_age']=60*86400
        self.session.set(CMS_SESSION_ID, user.id)
        self.session.set(IP_ADDRESS, self.request.remote_ip)
        self.redirect(next_url)

class CMSLockScreenHandler(CMSBaseHandler):
    def get(self,message=''):
        context=dict(message=message)
        id=self.current_user.id
        self.session.set(CMS_SESSION_ID_2,id)
        self.session.delete(CMS_SESSION_ID)
        self.render('cms/cms_lock_screen.html',**context)

    def post(self):
        id=self.session.get(CMS_SESSION_ID_2)
        user=Employee.by_id(id)
        self.session.set(CMS_SESSION_ID, user.id)
        password=self.get_argument('password','')
        if not password:
            self.get(message=u'请输入密码!')
        else:
            if not user.check_password(password):
                self.get(message=u'密码输入有误!')
            else:
                self.session.delete(CMS_SESSION_ID_2)
                self.redirect('/cms/')

class CMSLogoutHandler(CMSBaseHandler):
    @cms_login_required
    def get(self):
        self.session.delete(CMS_SESSION_ID)
        self.redirect('/cms/login/')