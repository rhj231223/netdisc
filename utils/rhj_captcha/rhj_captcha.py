# coding:utf-8
import random
from string import printable

from PIL import Image,ImageDraw,ImageFont

class Captcha(object):

    number=4

    size=(80,32)

    bgcolor=(255,255,255)

    font_path='utils/rhj_captcha/verdana.ttf'

    font_size=25

    draw_line=True

    draw_point=True

    line_num_range=(2,5)

    point_num_range=(100,500)


    source=printable[:62]

    @classmethod
    def gene_text(cls):
        return ''.join(random.sample(cls.source,cls.number))

    @classmethod
    def font_color(cls):
        return (random.randint(0,100),random.randint(0,100),random.randint(0,100))

    @classmethod
    def line_color(cls):
        return (random.randint(0,220),random.randint(0,255),random.randint(0,100))

    @classmethod
    def __gene_point(cls,draw):
        width, height = cls.size
        for i in xrange(random.randint(*cls.point_num_range)):
            point_range=(random.randint(0,width),random.randint(0,height))
            draw.point(point_range,fill=(0,0,0))

    @classmethod
    def __gene_line(cls, draw):
        width, height = cls.size
        for i in xrange(random.randint(*cls.line_num_range)):
            begin = (random.randint(0, width), random.randint(0, height))
            end = (random.randint(0, width), random.randint(0, height))
            draw.line([begin, end], fill=cls.line_color())

    @classmethod
    def gene_code(cls):
        width,height=cls.size
        image=Image.new('RGB',cls.size,cls.bgcolor)
        font=ImageFont.truetype(font=cls.font_path,size=cls.font_size)
        draw=ImageDraw.Draw(image)
        text=cls.gene_text()
        font_width,font_height=font.getsize(text)
        text_range = ((width - font_width)//2,(height-font_height)//2)
        draw.text(text_range,text,font=font,fill=cls.font_color())

        if cls.draw_line:
            cls.__gene_line(draw)

        if cls.draw_point:
            cls.__gene_point(draw)

        return (text,image)