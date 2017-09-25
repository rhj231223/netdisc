# coding:utf-8
class SizeCalculator(object):
    dic ={1:'Bytes',2:'KB',3:'MB',4:'GB',5:'TB'}

    @classmethod
    def get_size(cls, num,type_size=1):


        if type_size not in cls.dic:
            return u'超出范围'
        else:
            size = float(num / 1024)
            if size >= 1:
                return cls.get_size(size, type_size+1)
            else:
                return (str(round(num,2)) +' ' +cls.dic[type_size])

