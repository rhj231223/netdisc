# coding:utf-8

from tornado.web import StaticFileHandler


import cms_views as cms
from views.common.cms_account_urls import cms_account_urls
from views.websocket_views.websocket_urls import websocket_urls
from views.common.common_urls import common_urls
from views.common.front_account_urls import front_account_urls

cms_urls=[
    (r'^/cms/$',cms.CMSIndexHandler),
    (r'^/cms/file_table/(?P<page>\d+)/$',cms.CMSFileTable),
    (r'^/cms/upload_file/$',cms.CMSUploadFileHandler),
    (r'^/cms/download_file/(?P<uuid>[\w\-]+)/$',cms.CMSDownloadFileHnadler),
    (r'^/cms/delete_file/$',cms.CMSDeleteFileHandler),
    (r'^/cms/edit_file/(?P<uuid>[\w\-]+)/$',cms.CMSEditFileHandler),

    (r'/preview/(.*)',StaticFileHandler,dict(path='files/upload_files/')),
]

cms_urls+=cms_account_urls
cms_urls+=websocket_urls
cms_urls+=common_urls
cms_urls+=front_account_urls