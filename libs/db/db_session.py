# coding:utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



#数据库配置常量
ENGINE='mysql'
CONNECTION='pymysql'

USER='root'
PASSWORD='2312231223'

HOST='127.0.0.1'
PORT='3306'

DATABASE='friend_home_again_server'
CHARSET='charset=utf8'

DB_URI='{}+{}://{}:{}@{}:{}/{}?{}' .format(
    ENGINE,CONNECTION,USER,PASSWORD,HOST,PORT,DATABASE,CHARSET
)

engine=create_engine(DB_URI,echo=True)

Session=sessionmaker(bind=engine)
db_session=Session()

Base=declarative_base(engine)
