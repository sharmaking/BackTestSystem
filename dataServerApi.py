#!/usr/bin/python
# -*- coding: utf-8 -*-
#dataServerApi.py
from DataApi_32 import CDataApi
import time, copy, datetime

class CDataServerApi(CDataApi):
	#初始化接口
	def init(self, strategyActuatorDict):
		#数据堆栈
		self.bufferStack = {}	#每个合约一个堆栈
		self.strategyActuatorDict = strategyActuatorDict
		self.currentDateTime = datetime.datetime(1990,1,1,0,0,0)
	#数据接收接口
	def onRtnDepthMarketData(self, dataType, data):
		self.bufferStack[data["stockCode"][:6]].append((dataType,data))
		if self.bufferStack.has_key("Multiple"):
			if dataType == 3 or dataType == 4 or dataType == 5:
				self.bufferStack["Multiple"].append((dataType,data))
		if data["dateTime"].date() != self.currentDateTime.date():
			self.onRtnDayEnd()
		self.currentDateTime = copy.copy(data["dateTime"])

	def onRtnDayEnd(self):
		for stock, actuatorObj in self.strategyActuatorDict.items():
			if stock != "Multiple":
				actuatorObj.dayEnd()
		self.strategyActuatorDict["Multiple"].dayEnd()

	def onRtnDataEnd(self):
		print "DataEnd"

