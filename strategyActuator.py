#!/usr/bin/python
# -*- coding: utf-8 -*-
#strategyActuator.py

class CStrategyActuator(object):
	def __init__(self, bufferStack):
		super(CStrategyActuator, self).__init__()
		self.bufferStack = bufferStack
		#策略对象
		self.type = True     		#监听类型： True 单股票策略监听，False 多股票策略监听
		self.signalObjDict = {}		#但股票策略对象列表
		self.multipleObjDict = {}
	#----------------------------
	#获得策略对象
	#----------------------------
	#单股票策略
	def getSignalStrategyObj(self, signalObjDict):
		self.signalObjDict.update(signalObjDict.items())
		self.type = True
	#多股票策略
	def getmultipleStrategyObj(self, multipleObjDict):
		self.multipleObjDict.update(multipleObjDict.items())
		self.type = False
	#----------------------------
	#主函数
	#----------------------------
	def dataListening(self, dataType, data):
		if self.type:
			for signalName, signalObj in self.signalObjDict.items():
				signalObj.dataListener(dataType, data)
		else:
			for multipleName, multipleObj in self.multipleObjDict.items():
				multipleObj.dataListener(dataType, data)
		
	def checkStack(self):
		while not self.bufferStack.empty():
			dataType, data = self.bufferStack.get()
			self.dataListening(dataType, data)
	#当日数据结束，进入下一天，也是当日开始
	def dayEnd(self):
		if self.type:
			for signalName, signalObj in self.signalObjDict.items():
				signalObj.dayEnd()
		else:
			for multipleName, multipleObj in self.multipleObjDict.items():
				multipleObj.dayEnd()
	#数据结束
	def dataEnd(self):
		self.dayEnd()
		if self.type:
			for signalName, signalObj in self.signalObjDict.items():
				signalObj.dataEnd()
		else:
			for multipleName, multipleObj in self.multipleObjDict.items():
				multipleObj.dataEnd()