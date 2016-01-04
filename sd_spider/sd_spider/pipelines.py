# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import items
import json
import Model
from Model import JiBing, ZhengZhuang, KeShi

########################################################################
class InvalidPipeline(object):
    """
    如果该项目名称为空，则直接丢弃
    因为数据表中是以名字来进行查询等操作
    """

    #----------------------------------------------------------------------
    def process_item(self, item, spider):
        """"""
        if item['name'] == "":
            print '.........................Invalid Found........................'
            raise DropItem("Invalid item found: %s" % item)
        else:
            return item
        
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        
        
    
    

class SdSpiderPipeline(object):
    def __init__(self):
            #self.file = open('items.txt', 'w')
        self.txtname = 'items.txt'
        print '.........................init........................'
        
        # 创建数据库
        #Model.createDB()
        self.session = Model.createSession()
        
    
    #----------------------------------------------------------------------
    def writefile(self, item):
        """"""
        line = json.dumps(dict(item)) + "\n"
        with open(self.txtname, 'a') as f:
            f.write(line)        
    
    
    def process_item(self, item, spider):
        
        if type(item) == items.JibingItem:
            print '.........................save Jibing........................'
            jb = Model.getEntity(self.session, JiBing, item['name'])
            jb.Name_desc = item['jibing']
            jb.Gaishu = item['gaishu']
            
            kss = item['keshi']
            KS = []
            for ks in kss:
                KS.append(Model.getEntity(self.session, KeShi, ks))
            jb.Keshi = KS
            
            zzs = item['zhengzhuang']
            ZZ = []
            for zz in zzs:
                ZZ.append(Model.getEntity(self.session, ZhengZhuang, zz))
            jb.Zhengzhuang = ZZ
            
            jb.Jiancha = item['jiancha']
            
            self.session.add(jb)
            self.session.commit()
                
        elif type(item) == items.ZhengzhuangItem:
            print '.........................Save Zhengzhuang........................'
            zz = Model.getEntity(self.session, Model.ZhengZhuang, item['name'])
            zz.Name_desc = item['zhengzhuang']
            zz.Gaishu = item['gaishu']
            zz.Buwei = Model.getEntity(self.session, Model.BuWei, item['buwei'])
            
            rqs = item['renqun']
            RQ = []
            for rq in rqs:
                RQ.append(Model.getEntity(self.session, Model.RenQun, rq))
            zz.Renqun = RQ
            
            self.session.add(zz)
            self.session.commit()
            
        else:
            pass
        return item
    
    #----------------------------------------------------------------------
    def open_spider(self, spider):
        """"""
        print '.........................open spider........................'
        
    
    #----------------------------------------------------------------------
    def close_spider(self):
        """"""
        print '.........................close spider........................'