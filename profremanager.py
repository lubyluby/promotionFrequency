#-*- encoding=utf-8 -*-
import sys, logging, uuid ,redis ,binascii ,ConfigParser, json
import  sqlalchemy
import amiconn
from  datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from basepromanager import BaseProManager
import time
class ProFreManager(BaseProManager):
    def __init__(self,pjId):
         super(ProFreManager,self).__init__(pjId)

    def _loadData(self,jsonData):
        if isinstance(jsonData,dict):
            self.prDict=jsonData
        else:
            self.prDict=json.loads(jsonData)

    def closeConn(self):
        if self.sqlSession!=None:
            self.sqlSession.close()

    def insert(self,jsonData):
        try:
            self.initConn()
            self._insertOrUpdate(jsonData=jsonData,isNew=True)
            self.sqlSession.commit()
        except Exception, e:
            print e.message
            logging.error(e.message)
        finally:
            self.closeConn()

    def update(self,jsonData):
        try:
            self.initConn()
            self._insertOrUpdate(jsonData=jsonData,isNew=False)
            self.sqlSession.commit()
        except Exception, e:
             print e.message
             logging.error(e.message)
        finally:
             self.closeConn()

    def frmanage(self):
        try:
            self.initConn()
            # 创建#temp表
            row=self.sqlSession.execute('select Last_stamp from dbo.Promotion_frequency_stamp;').fetchone()
            if(row !=None):
                lastStamp= row[0]
                sql='select top '+str(self.top)+' * into #temp  from Promotion_history where Stamp >'+str(lastStamp)+' order by Stamp'
                self.sqlSession.execute(sql)
            else:
                sql='select top '+str(self.top)+' * into #temp  from Promotion_history where Stamp >0  order by Stamp'
                self.sqlSession.execute(sql) 
            row=self.sqlSession.execute('select count(*) from #temp;').fetchone()
            if(int(row[0])!=0):
                #分组
                sql='''select * into #tempGroup from(
                    select distinct  Pj_id,'CUPCPL'as Frequency_Cd,Promotion_key_val+'_'+convert(varchar,Promotion_id)+'_'+convert(varchar,Promotion_plan_id) as Frequency_key, count(*)over(partition by Promotion_key_val,Promotion_id,Promotion_plan_id,pj_id )as Frequency,1 as Commit_status,1 as [Status]  from #temp
                )as a'''
                self.sqlSession.execute(sql)

                sql='''insert into #tempGroup (Pj_id,Frequency_Cd,Frequency_key,Frequency,Commit_status,[Status]) select distinct  Pj_id,'CUPC'as Frequency_Cd,Promotion_key_val+'_'+convert(varchar,Promotion_id) as Frequency_key, count(*)over(partition by Promotion_key_val,Promotion_id,pj_id )as Frequency,1 as Commit_status,1 as [Status]  from #temp'''
                self.sqlSession.execute(sql)

                sql='''insert into #tempGroup (Pj_id,Frequency_Cd,Frequency_key,Frequency,Commit_status,[Status])
                    select distinct  Pj_id,'CU'as Frequency_Cd,Promotion_key_val as Frequency_key, count(*)over(partition by Promotion_key_val,pj_id )as Frequency,1 as Commit_status,1 as [Status]  from #temp'''
                self.sqlSession.execute(sql) 

                #分组结果插入#tempGroup
                sql='''merge into dbo.Promotion_frequency as t
                    using #tempGroup as s
                    on t.Pj_id=s.Pj_id and t.Frequency_Cd=s.Frequency_Cd and t.Frequency_key=s.Frequency_key
                    when matched
                    then update set t.Frequency=t.Frequency+s.Frequency 
                    when not matched
                    then insert(Pj_id,Frequency_Cd,Frequency_key,Frequency,Commit_status,[Status]) values(s.Pj_id,s.Frequency_Cd,s.Frequency_key,s.Frequency,s.Commit_status,s.[Status]);'''
                self.sqlSession.execute(sql) 
                #记录读取的最后一张timestamp
                row1=self.sqlSession.execute('select Last_stamp from Promotion_frequency_stamp;').fetchone()
                sql='select top 1  stamp  from #temp order by stamp desc'
                row=self.sqlSession.execute(sql).fetchone()
                strstamp='0x'+binascii.b2a_hex(row[0])
                if(row1 ==None):
                    sql="insert Promotion_frequency_stamp (Last_stamp) values('"+strstamp+"')"
                else:
                    sql="update Promotion_frequency_stamp set Last_stamp='"+strstamp+"'"
                self.sqlSession.execute(sql)
                self.sqlSession.commit()
        except Exception, e:
             print e.message
             logging.error(e.message)
        finally:
             self.closeConn()

    

 


       

    
    
        

   