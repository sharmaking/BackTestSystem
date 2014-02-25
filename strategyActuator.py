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
		while self.bufferStack:
			dataType, data = self.bufferStack[0]
			self.dataListening(dataType, data)
			del self.bufferStack[0]

	def dayEnd(self):
		if self.type:
			for signalName, signalObj in self.signalObjDict.items():
				signalObj.dayEnd()
		else:
			for multipleName, multipleObj in self.multipleObjDict.items():
				multipleObj.dayEnd()