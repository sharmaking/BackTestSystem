#!/usr/bin/python
# -*- coding: utf-8 -*-
#dataListener.py
import multiprocessing

class CDataListerner(multiprocessing.Process):
	def __init__(self, stocks, actuatorDict):
		super(CDataListerner, self).__init__()
		self.stocks = stocks
		self.actuatorDict = actuatorDict
	#----------------------------
	#主函数，监听数据更新
	#----------------------------
	def run(self):
		while 1:
			for stock in self.stocks:
				self.actuatorDict[stock].checkStack()
