#!/usr/bin/python
# -*- coding: utf-8 -*-
#baseSignal.py
import sys
sys.path.append("..")
import baseStrategy

class CBaseSignal(baseStrategy.CBaseStrategy):
	#------------------------------
	#继承重载函数
	#------------------------------
	#自定义初始化函数
	def customInit(self):
		self.name = "baseSignal"
	#行情数据触发函数
	def onRtnMarketData(self, data):
		#self.sendMessageToClient("onRtnMarketData")
		pass #print self.name, "onRtnMarketData", self.stockCode, len(data)
	#逐笔成交触发函数
	def onRtnTradeSettlement(self, data):
		pass #print self.name, "onRtnTradeSettlement", self.stockCode, len(data)
	#买一队列触发函数
	def onRtnOrderQueue(self, data):
		pass #print self.name, "onRtnOrderQueue", self.stockCode, len(data)
	def dayBegin(self):
		pass
	def dayEnd(self):
		pass
	#自动保存缓存触发函数
	def autosaveCache(self):
		#self.saveCache(data = self.data)
		pass