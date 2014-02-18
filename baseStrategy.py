#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import copy
import os

class CBaseStrategy(object):
	def __init__(self):
		super(CBaseStrategy, self).__init__()
		self.stockCode = ""
		self.customInit()
		#最新数据
		self.currentData = {}
		#连接池，用于发送信号
		self.requesHandlerObjList = []
		#数据缓存
		#当前时间，最近的一个行情数据时间
		self.currentMDDateTime = datetime.datetime(1990,1,1,0,0,0)
		self.MDList = []			#行情数据
		self.TDList = []			#逐笔成交数据
		self.ODList = []			#成交队列数据
	#------------------------------
	#listener 调用接口
	#------------------------------
	#自定义对象初始化
	def init(self, stockCode):
		self.stockCode = stockCode
		self.initCashe()
	#获得连接对象
	def getRequesHandlerObjList(self, requesHandlerObjList):
		self.requesHandlerObjList = requesHandlerObjList
	
	def dataListener(self, dataType, data):
		if dataType == 1:			#逐笔成交数据
			self.onRtnTradeSettlement(data)
			self.saveTradeSettlement(data)
		elif dataType == 2:			#报单队列
			self.onRtnOrderQueue(data)
			self.saveOrderQuene(data)
		else:
			if data["dateTime"] > self.currentMDDateTime:
				self.onRtnMarketData(data)
				self.currentMDDateTime = copy.copy(data["dateTime"])
				self.saveMarketData(data)
		#自动保存缓存触发
		if (datetime.datetime.now() - self.preSaveCacheTime)> datetime.timedelta(minutes = 5):
			self.autosaveCache()
			#self.saveCache(MDList = self.MDList, TDList = self.TDList, ODList = self.ODList)
	#------------------------------
	#cache 相关函数
	#------------------------------
	def initCashe(self):
		self.cacheFilePath = "cache/%s%s.cache" %(self.stockCode, self.name)
		self.preSaveCacheTime = datetime.datetime.now()
		self.loadCache()
	#读取缓存
	def loadCache(self):
		if not os.path.isfile(self.cacheFilePath):
			self.cacheFile = open(self.cacheFilePath, "w")
			self.cacheFile.close
		execfile(self.cacheFilePath)
	#保存缓存
	def saveCache(self, **objDict):
		self.cacheFile = open(self.cacheFilePath, "w")
		content = ""
		for key, value in objDict.items():
			content += "self.%s = %s\n" %(key, str(value))
		self.cacheFile.write(content)
		self.cacheFile.close()
		self.preSaveCacheTime = datetime.datetime.now()
	#------------------------------
	#数据保存相关函数
	#------------------------------
	def saveMarketData(self, data):
		self.MDList.append(copy.copy(data))
		if len(self.MDList) > 300:
			del self.MDList[0]
	def saveTradeSettlement(self, data):
		self.TDList.append(copy.copy(data))
		if len(self.TDList) > 300:
			del self.TDList[0]
	def saveOrderQuene(self, data):
		self.ODList.append(copy.copy(data))
		if len(self.ODList) > 300:
			del self.ODList[0]
	#------------------------------
	#继承重载函数
	#------------------------------
	#自定义初始化函数
	def customInit(self):
		self.name = "baseStrategy"
	#行情数据触发函数
	def onRtnMarketData(self, data):
		pass
	#逐笔成交触发函数
	def onRtnTradeSettlement(self, data):
		pass
	#买一队列触发函数
	def onRtnOrderQueue(self, data):
		pass
	def dayBegin(self):
		pass
	def dayEnd(self):
		pass
	#自动保存缓存触发函数
	def autosaveCache(self):
		#self.saveCache(data = self.data)
		pass