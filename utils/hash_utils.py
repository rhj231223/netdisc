# coding:utf-8
import hashlib

def hash_data(data):
    hash=hashlib.sha1()
    hash.update(data)
    return hash.hexdigest()

print hash_data('123')
