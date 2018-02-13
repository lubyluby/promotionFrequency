#-*- encoding=utf-8 -*-
import redis
import ConfigParser
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import amiconn

class BaseProManager(object):
    def __init__(self, pjId):
        self.PjId = pjId
        self.sqlSession = None
        self.configFileName = "config\config.cfg"
        self.readConfig()
    
    def initConn(self):
        # init redis
        # self.redis = redis.Redis(host=self.redisHost, port=self.redisPort, db=self.prdb,password=self.redisPassword)
        #  sql server
        engine = create_engine(self.connstring)
        dbSession = sessionmaker(bind=engine)
        self.sqlSession = dbSession()

    def initRedis(self):
        self.redisMas = redis.Redis(
            host=self.redisMasHost,
            port=self.redisMasPort,
            db=self.redisMasDb,
            password=self.redisMasPassword)
        self.redisPro = redis.Redis(
            host=self.redisProHost,
            port=self.redisMasPort,
            db=self.redisProDb,
            password=self.redisProPassword)

    def readConfig(self):
        #self.tempDict=json.load(self.templateFileName)
        # =============
        cf = ConfigParser.RawConfigParser()
        cf.optionxform = str
        cf.read(self.configFileName)
        self.cf = cf
        section = "sqlserver"
        connName = cf.get(section, "connName").strip()
        clientDriverVer = None if cf.has_option(
            section, "clientdriverver") is False or cf.get(
                section,
                "clientdriverver").strip().lower() == "none" else cf.get(
                    section, "clientdriverver").strip()
        self.connstring = amiconn.GetMsSqlConnStringByConnName(
            connName, clientDriverVer)
        section = "redis_master"
        self.redisMasHost = cf.get(section, "host").strip()
        self.redisMasPort = cf.get(section, "port").strip()
        self.redisMasPassword = cf.get(section, "password").strip()
        # ==========================================================
        self.redisMasDb = int(cf.get(section, "db").strip())
        # ==========================================================
        section = "redis_pro"
        self.redisProHost = cf.get(section, "host").strip()
        self.redisProPort = cf.get(section, "port").strip()
        self.redisProPassword = cf.get(section, "password").strip()
        # ==========================================================
        self.redisProDb = int(cf.get(section, "db").strip())
        # ==========================================================

        section="TopNum"
        self.top=int(cf.get(section, "topnum").strip())

    # def init_db():
    #     Base.metadata.create_all(engine)

