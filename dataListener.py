#!/usr/bin/python
# -*- coding: utf-8 -*-
#dataListener.py
import multiprocessing

class CDataListerner(multiprocessing.Process):
	def __init__(self, stocks, actuatorDict, bufferStack):
		super(CDataListerner, self).__init__()
		self.stocks = stocks
		self.actuatorDict = actuatorDict
		self.bufferStack = bufferStack
	#----------------------------
	#主函数，监听数据更新
	#----------------------------
	def run(self):
		while 1:
			for stock in self.stocks:
				self.actuatorDict[stock].checkStack()
			if self.actuatorDict.has_key("Multiple"):
				self.actuatorDict["Multiple"].checkStack()
			#监视系统信息
			if not self.bufferStack["__SystemMessage__"].empty():
				systemMessage = self.bufferStack["__SystemMessage__"].get()
				if systemMessage == "DayEnd":
					for stock, actuator in self.actuatorDict.items():
						actuator.dayEnd()
				if systemMessage == "DataEnd":
					for stock, actuator in self.actuatorDict.items():
						actuator.dataEnd()
