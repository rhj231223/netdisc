# coding:utf-8
import os



from views.base_views.base_views import CMSBaseHandler
from decorators.cms_decorators import cms_login_required,\
    cms_handler_permission,cms_ip_limit
from models.file_models import File
from utils.size_calculator import SizeCalculator
from utils import xtjson
from models.cms_models import Permission
from utils.pagination import pagination
from constants import SINGLE_PAGE_NUM,SHOW_PAGE

class CMSIndexHandler(CMSBaseHandler):

    @cms_login_required
    @cms_ip_limit
    @cms_handler_permission('CMSIndexHandler',type_name='handler')
    def get(self):
        self.render('cms/cms_index.html')

class CMSFileTable(CMSBaseHandler):
    @cms_login_required
    def get(self,page):
        files = self.db.query(File).order_by(File.is_removed,File.create_time.desc()).all()
        current_page=int(page)
        total_page,start,end,page_list,pre_page,next_page=pagination(
            current_page=current_page,total_num=len(files),
            sing_page_num=SINGLE_PAGE_NUM,show_page=SHOW_PAGE,
        )

        context=dict(files=files[start:end],current_page=current_page,
                     total_page=total_page,page_list=page_list,
                     pre_page=pre_page,next_page=next_page,
                     show_page=SHOW_PAGE)
        self.render('cms/cms_file_table.html',**context)


class CMSUploadFileHandler(CMSBaseHandler):
    @cms_login_required
    def get(self,message=''):
        context=dict(message=message)
        self.render('cms/cms_upload_file.html',**context)

    @cms_login_required
    def post(self):
        files=self.request.files.get('upload_file','')
        if not files:
            self.get(message=u'必须指定上传的文件')
        else:
            for file in files:
                file_body = file.get('body', '')
                f1 = File
                if f1.file_existed(file_body):
                    continue
                self.save(file)
            self.get(message=u'上传成功!')


    def save(self,file):
        file_name=file.get('filename','')
        file_body=file.get('body','')
        content_type=file.get('content_type','')
        file_hash=file_body
        upload_user=self.current_user.username



        url='files/upload_files/%s' %file_name.encode('utf8')


        with open(url,'wb') as f:
            f.write(file_body)


        size = os.path.getsize(url)
        size=SizeCalculator.get_size(size)

        f2=File(name=file_name,content_type=content_type,
                file_hash=file_hash,size=size,
                upload_user=upload_user)
        self.db.add(f2)
        self.db.commit()

class CMSDownloadFileHnadler(CMSBaseHandler):

    def get(self,uuid):
        if not uuid:
            self.write(u'必须指定uuid')
        else:
            file=File.by_field_first(uuid=uuid)
            if not file:
                self.write(u'没有找到该文件')
            else:
                path='files/upload_files/%s' %file.name.encode('utf-8')
                self.set_header('Content-Type','application/octet-stream')
                self.set_header('Content-Disposition','attachment;filename=%s' %file.name)

                with open(path,'rb') as f:
                    while 1:
                        data=f.read(2048)
                        if not data:
                            break
                        self.write(data)
                self.finish()

class CMSDeleteFileHandler(CMSBaseHandler):
    def post(self):
        uuid=self.get_argument('uuid','')
        want_remove=self.get_argument('want_remove','')

        if not uuid:
            message=xtjson.json_params_error(message=u'必须指定文件uuid!')
            self.write(message)
        else:
            file=File.by_field_first(uuid=uuid)
            if not file:
                message = xtjson.json_params_error(message=u'没有找到该文件!')
                self.write(message)
            else:
                if not file.is_removed:
                    if want_remove=='1':
                        file.is_removed=True
                        self.db.commit()
                        self.write(xtjson.json_result())
                    else:
                        message = xtjson.json_params_error(message=u'该文件没有被删除,无需取消删除!')
                        self.write(message)

                else:
                    if want_remove=='0':
                        file.is_removed=False
                        self.db.commit()
                        self.write(xtjson.json_result())
                    else:
                        message=xtjson.json_params_error(message=u'该文件已删除,无需重复删除!')
                        self.write(message)

class CMSEditFileHandler(CMSBaseHandler):
    def get(self,uuid):
        file=File.by_field_first(uuid=uuid)
        permissions=Permission.all()
        if not file:
            self.write(u'没有找到该文件')
        else:
            context=dict(file=file,permissions=permissions)
            self.render('cms/cms_edit_file.html',**context)


    def post(self,uuid):
        name=self.get_argument('name','')
        permission_id=self.get_argument('permission_id','')

        if not uuid:
            self.write(xtjson.json_params_error(message=u'必须指定uuid'))
        elif not name:
            self.write(xtjson.json_params_error(message=u'文件名不能为空!'))
        else:
            file=File.by_field_first(uuid=uuid)
            if not file:
                self.write(xtjson.json_params_error(message=u'没有找到该文件!'))
            else:
                file.name=name
                if permission_id:
                    permission=Permission.by_id(permission_id)
                    if permission:
                        file.permission=permission
                        self.db.commit()
                        self.write(xtjson.json_result())
                    else:
                        self.write(xtjson.json_params_error(message=u'没有找到该权限!'))

