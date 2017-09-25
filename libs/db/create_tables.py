# coding:utf-8

from db_session import db_session,engine
from models.front_models import Base

def run():
    print '--------create_start----------'
    Base.metadata.create_all(engine)
    print '--------create_end------------'

if __name__=='__main__':
    run()