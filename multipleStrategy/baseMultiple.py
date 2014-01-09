#!/usr/bin/python
# -*- coding: utf-8 -*-
#baseMultiple.py
import sys
sys.path.append("..")
import baseStrategy
import copy
import datetime

class CBaseMultiple(baseStrategy.CBaseStrategy):
	#------------------------------
	#继承重载函数
	#------------------------------
	#自定义初始化函数
	def customInit(self):
		self.name = "baseMultiple"
	#行情数据触发函数
	def onRtnMarketData(self, data):
		print self.name, "onRtnMarketData", len(data)
	def dayBegin(self):
		pass
	def dayEnd(self):
		pass
	#自动保存缓存触发函数
	def autosaveCache(self):
		#self.saveCache(data = self.data)
		pass