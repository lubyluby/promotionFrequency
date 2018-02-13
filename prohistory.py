#-*- encoding=utf-8 -*-
import datetime
import sys
import uuid
import redis
import sqlalchemy
import amiconn
import binascii
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

reload(sys)
sys.setdefaultencoding("gbk")

Base = declarative_base()

class PromotionHistoryMod(Base):
    __tablename__ = "Promotion_history"
    Promotion_history_id = Column("Promotion_history_id", BigInteger, primary_key=True,autoincrement=True)
    PjId = Column("Pj_id",BigInteger,default=0)
    PromotionId = Column("Promotion_id", BigInteger,default=0)
    PromotionPlanId=Column("Promotion_plan_id",BigInteger,default=0)
    OrderKey=Column("Order_key",String)
    PromotionKeyType=Column("Promotion_key_type",String)
    PromotionKeyVal=Column("[Promotion_key_val]",String)
    PromotionDate=Column("Promotion_date",DateTime,default=func.getdate())
    OperateTime = Column("operate_time",DateTime,onupdate=datetime.now(),default=func.getdate())
    Stamp = Column(TIMESTAMP, server_default=func.now())
   
class PromotionFrequencyMod(Base):
    __tablename__ = "Promotion_frequency"
    Id = Column("Id", BigInteger, primary_key=True,autoincrement=True)
    PjId = Column("Pj_id",BigInteger,default=0)
    FrequencyCd=Column("Frequency_Cd",String,default="")
    FrequencyKey=Column("Frequency_key",String,default="")
    Frequency=Column("Frequency",Integer)
    Commit_status=Column("Commit_status",SMALLINT)
    Status=Column("Status",SMALLINT)
    CreateTime = Column("Create_time", DateTime, default=func.getdate())
    OperateTime = Column("operate_time",DateTime,onupdate=datetime.now(),default=func.getdate())
    Stamp = Column(TIMESTAMP, server_default=func.now())

class PromotionFrequencyStampMod(Base):
    __tablename__ = "Promotion_frequency_stamp"
    Id = Column("Id", BigInteger, primary_key=True,autoincrement=True)
    LastStamp = Column("Last_stamp",String,default="")
    CreateTime = Column("Create_time", DateTime, default=func.getdate())
    OperateTime = Column("operate_time",DateTime,onupdate=datetime.now(),default=func.getdate())


# class PromotionTempHistoryMod(Base):
#     __tablename__ = "#temp"
#     Promotion_history_id = Column("Promotion_history_id", BigInteger, primary_key=True,autoincrement=True)
#     PjId = Column("Pj_id",BigInteger,default=0)
#     PromotionId = Column("Promotion_id", BigInteger,default=0)
#     PromotionPlanId=Column("Promotion_plan_id",BigInteger,default=0)
#     OrderKey=Column("Order_key",String)
#     PromotionKeyType=Column("Promotion_key_type",String)
#     PromotionKeyVal=Column("[Promotion_key_val]",String)
#     PromotionDate=Column("Promotion_date",DateTime,default=func.getdate())
#     OperateTime = Column("operate_time",DateTime,onupdate=datetime.now(),default=func.getdate())
#     Stamp = Column(TIMESTAMP, server_default=func.now())
   
