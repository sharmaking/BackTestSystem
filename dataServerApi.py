#!/usr/bin/python
# -*- coding: utf-8 -*-
#dataServerApi.py
from DataApi_32 import CDataApi
import time, copy

class CDataServerApi(CDataApi):
	#初始化接口
	def init(self):
		#数据堆栈
		self.bufferStack = {}	#每个合约一个堆栈
	#数据接收接口
	def onRtnDepthMarketData(self, dataType, data):
		self.bufferStack[data["stockCode"][:6]].put((dataType,data))
		if self.bufferStack.has_key("Multiple"):
			if dataType == 3 or dataType == 4 or dataType == 5:
				self.bufferStack["Multiple"].put((dataType,data))

	def onRtnDataEnd(self):
		print "DataEnd"

