# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class SdSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

########################################################################
class JibingItem(scrapy.Item):
    """"""
    name = Field()
    jibing = Field()
    zhengzhuang = Field()
    gaishu = Field()
    jiancha = Field()
    keshi = Field()
    
    bingyin_desc = Field()
    zhengzhuang_desc = Field()
    jianchazhenduan_desc = Field()
    zhiliaohuli_desc = Field()
    

########################################################################
class ZhengzhuangItem(scrapy.Item):
    """"""
    name = Field()
    zhengzhuang = Field()
    gaishu = Field()
    buwei = Field()
    renqun = Field()
    
    
    
    