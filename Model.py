#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Chaos --<Chaosimpler@gmail.com>
  Purpose: 定义常用模型
  Created: 2015-11-18
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref

#eng = create_engine('sqlite:///test.db')
#Base = declarative_base()   

#Session=sessionmaker(bind=eng)
#ses=Session()   

#engine = create_engine('sqlite:///test.db')
engine = create_engine('sqlite:///:memory:')
Base = declarative_base()
Session = sessionmaker(bind=engine)

#----------------------------------------------------------------------
def createDB():
    """"""
    Base.metadata.create_all(engine)
    
#----------------------------------------------------------------------
def createSession():
    """"""        
    session = Session()
    return session



class RenQun(Base):
    """"""
    __tablename__="RenQun"
    
    
    Id=Column(Integer,primary_key=True)
    Name=Column(String)
    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return "RenQun < %s >" % self.Name
        
    
########################################################################
class KeShi(Base):
    """"""
    __tablename__="KeShi"
    
    
    Id=Column(Integer,primary_key=True)
    Name=Column(String)
    
    #JiBing = relationship
    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return "KeShi < %s >" % self.Name
        
    
    
########################################################################
class BuWei(Base):
    """"""
    __tablename__="BuWei"
    
    
    Id=Column(Integer,primary_key=True)
    Name=Column(String)
    


JiBing_ZhengZhuang_Relation = Table('JZ_Relation', Base.metadata,
                                    Column('JiBing_id', Integer, ForeignKey('JiBing.Id')),
                                    Column('ZhengZhuang_id', Integer, ForeignKey('ZhengZhuang.Id'))
                                    )

JiBing_RenQun_Relation = Table('JR_Relation', Base.metadata,
                               Column('JiBing_id', Integer, ForeignKey('JiBing.Id')),
                               Column('RenQun_id', Integer, ForeignKey('RenQun.Id'))
                               )
JiBing_KeShi_Relation = Table('JK_Relation', Base.metadata,
                              Column('JiBing_id', Integer, ForeignKey('JiBing.Id')),
                              Column('KeShi_id', Integer, ForeignKey('KeShi.Id'))
                              )

ZhengZhuang_RenQun_Relation = Table('ZR_Relation', Base.metadata,
                                    Column('ZhengZhuang_id', Integer, ForeignKey('ZhengZhuang.Id')),
                                    Column('RenQun_id', Integer, ForeignKey('RenQun.Id'))
                                    )


########################################################################
class JiBing(Base):
    """"""
    __tablename__="JiBing"
    
    Id=Column(Integer,primary_key=True)
    Name=Column(String)
    #Keshi=Column(Integer)
    #Zhengzhuang=Column(String)
    Jiancha=Column(Text)
    
    #疾病和科室的关系由1:n修改为n:n
    #Keshi_Id = Column(Integer, ForeignKey('KeShi.Id'))
    #Keshi = relationship('KeShi', backref='JiBing')
    Keshi = relationship('KeShi', secondary=JiBing_KeShi_Relation,
                         backref='JiBing')
    
    Zhengzhuang = relationship('ZhengZhuang', secondary=JiBing_ZhengZhuang_Relation,
                               backref='JiBing')
    Renqun = relationship('RenQun', secondary=JiBing_RenQun_Relation,
                          backref='JiBing')
    
    
    Name_desc=Column(Text)
    Gaishu=Column(Text)
    
    
    Gaishu_desc=Column(Text)  
    Bingyin_desc=Column(Text)
    Zhengzhuang_desc=Column(Text)
    Jianchazhenduan_desc=Column(Text)    
    Zhiliaohuli_desc=Column(Text)
    Yufangbaojian_desc=Column(Text)
    Shiliao_desc=Column(Text)
    Xiangguanwenzhang_desc=Column(Text)
        
    
    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return "JiBing < %s >" % self.Name
        


########################################################################
class ZhengZhuang(Base):
    """"""
    __tablename__="ZhengZhuang"

    Id=Column(Integer,primary_key=True)
    Name=Column(String)    
    #Buwei=Column(Integer)
    #Renqun=Column(Integer)
    
    Renqun = relationship('RenQun', secondary=ZhengZhuang_RenQun_Relation, backref='ZhengZhuang')
    
    Buwei_Id = Column(Integer, ForeignKey("BuWei.Id"))
    Buwei = relationship("BuWei", backref="ZhengZhuang")
    
    
    Name_desc=Column(Text)
    Gaishu=Column(Text)    
    
    Bingyin_desc=Column(Text)
    Xiangguanjibing=Column(Integer)
    Jianchazhenduan_desc=Column(Text)  
    Zhiliaohuli_desc=Column(Text)
    Yufangbaojian_desc=Column(Text)
    Xiangguanwenzhang_desc=Column(Text)    
    
    
    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return "ZhengZhuang < %s >" % self.Name
    


 

#----------------------------------------------------------------------
def getEntity(ss, entity, name):
    """
    该函数用于生成一个新的实体（KeShi,JiBing等）对象，具体方法是：
        如果已经存在则返回该对象，如果不存在则生成一个新的对象；
    
    """
    t = ss.query(entity).filter(entity.Name==name).all()
    if(len(t) > 0):
        return t[0]
    else:
        return entity(Name=name)
    
    
#----------------------------------------------------------------------
def unit_test(ss):
    """"""
    #添加疾病和科室
    J = JiBing(Name='J1', Jiancha='JC1')
    J.Keshi = [KeShi(Name='K1')]
    
    #添加症状和人群
    J.Zhengzhuang = [ZhengZhuang(Name='ZZ1'), ZhengZhuang(Name='ZZ2')]
    J.Renqun = [RenQun(Name='RQ1'), RenQun(Name='RQ2')]
    
    ss.add(J)
    ss.commit()


    J2 = JiBing(Name='J2')
    J2.Keshi = [getEntity(ss, KeShi, 'K1')]
    J2.Zhengzhuang = [getEntity(ss, ZhengZhuang, 'ZZ1'), getEntity(ss, ZhengZhuang, 'ZZ3')]
    J2.Renqun = [getEntity(ss, RenQun, 'RQ1'), getEntity(ss, RenQun, 'RQ3')]
    
    ss.add(J2)
    ss.commit()
    
    z = getEntity(ss, ZhengZhuang, 'ZZ1')
    
    
    #查询症状
    #zz = ss.query(ZhengZhuang).filter(ZhengZhuang.Name=="ZZ1").one()
    #print zz, zz.JiBing
    
    
    
    
    print 'add over'



if __name__ == '__main__':
    
    #Create_All()
    createDB()
    ss = createSession()
    
    unit_test(ss)
    print 'over!'