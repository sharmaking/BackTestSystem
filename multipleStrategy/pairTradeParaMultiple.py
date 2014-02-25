#!/usr/bin/python
# -*- coding: utf-8 -*-
#pairTradeParaMultiple
import baseMultiple

class CPairTradeParaMultiple(baseMultiple.CBaseMultiple):
	#------------------------------
	#继承重载函数
	#------------------------------
	#自定义初始化函数
	def customInit(self):
		self.name = "pairTradeParaMultiple"
	#行情数据触发函数
	def onRtnMarketData(self, data):
		pass
		#print self.name, "onRtnMarketData", len(data)
	def dayEnd(self):
		print "pairTradeParaMultiple"
		pass
	#自动保存缓存触发函数
	def autosaveCache(self):
		#self.saveCache(data = self.data)
		pass