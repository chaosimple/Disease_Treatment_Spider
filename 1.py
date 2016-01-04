#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/11/19
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Table
from sqlalchemy.orm import sessionmaker

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


engine = create_engine('sqlite:///1.db', echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

########################################################################
class User(Base):
    """"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)
    
    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)    



#----------------------------------------------------------------------
def create():
    """该函数用于创建新增表"""
    Base.metadata.create_all(engine)


#----------------------------------------------------------------------
def addUser():
    """"""
    ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
    session.add(ed_user)
    print 'over'




########################################################################
class Address(Base):
    """"""
    __tablename__ = 'addresses'
    
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    user = relationship("User", backref=backref('addresses', order_by=id))

    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return "<Address(email_address='%s')>" %  self.email_address
    


post_keywords = Table('post_keywords', Base.metadata,
                      Column('post_id', Integer, ForeignKey('posts.id')),
                      Column('keyword_id', Integer, ForeignKey('keywords.id'))
                      )


########################################################################
class BlogPost(Base):
    """"""
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    headline = Column(String(255), nullable=False)
    body = Column(Text)
    
    keywords = relationship('Keyword', secondary=post_keywords, backref='posts')
    
    author = relationship('User', backref=backref('posts', lazy='dynamic'))

    #----------------------------------------------------------------------
    def __init__(self, headline, body, author):
        """Constructor"""
        self.author = author
        self.headline = headline
        self.body = body
    
    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return "BlogPost(%r, %r, %r)" % (self.headline, self.body, self.author)


########################################################################
class Keyword(Base):
    """"""
    __tablename__ = 'keywords'
    
    id = Column(Integer, primary_key=True)
    Keyword = Column(String(50), nullable=False, unique=True)

    #----------------------------------------------------------------------
    def __init__(self, Keyword):
        """Constructor"""
        self.Keyword = Keyword
        
    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return "Keyword %s" % Keyword
    
    
        
    
    

#----------------------------------------------------------------------
def getSession():
    """"""
    return session
    

if __name__ == '__main__':
    create()
    #addUser()
    ss = getSession()
    print 'Finished!'
