#!/usr/bin/python
# -*- coding: utf-8 -*-
#pairTradeTickSignal
import baseSignal, multiprocessing

class CPairTradeTickSignal(baseSignal.CBaseSignal):
	#自定义初始化函数
	def customInit(self):
		self.name = "pairTradeTickSignal"
		self.tickData = []
	#行情数据触发函数
	def onRtnMarketData(self, data):
		self.getTickData(data)
		print self.stockCode, data["dateTime"], data["close"], self.currentMDDateTime
	def dayEnd(self):
		print "dayEnd", self.stockCode, self.currentMDDateTime
	def autosaveCache(self):
		#self.saveCache(data = self.data)
		pass
	#---------------------------------------
	#具体实现函数
	#---------------------------------------
	def getTickData(self, data):
		self.tickData.append({
				"dateTime"		: data["dateTime"],
				"close"			: data["close"],
				"askPriceOne"	: data['askPrice'][0],
				"bidPriceOne"	: data["bidPrice"][0]
			})
		if len(self.tickData) > 2000000:
			del self.tickData[0]
