#!/usr/bin/python
# -*- coding: utf-8 -*-
#matchesDealEngine.py

class CMatchesDealEngine(object):
	def __init__(self, stockCode):
		super(CMatchesDealEngine, self).__init__()
		self.stockCode = stockCode
	#行情数据触发函数
	def onRtnMarketData(self, data):
		pass
	#逐笔成交触发函数
	def onRtnTradeSettlement(self, data):
		pass
	#买一队列触发函数
	def onRtnOrderQueue(self, data):
		pass
	#当日结束
	def dayEnd(self):
		pass

