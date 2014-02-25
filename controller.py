#!/usr/bin/python
# -*- coding: utf-8 -*-
#controller.py
import copy, datetime
import dataServerApi, dataListener, strategyActuator
#载入策略
import signalStrategy, multipleStrategy
#-----------------------
#定义全局变量
#-----------------------
#数据监听对象
g_listenerList = []			#总共3个对象
#策略执行器对象列表
g_StrategyActuatorDict = {}	#每个股票一个对象
#订阅股票列表
g_subStocks = []
#-----------------------
#注册策略
#-----------------------
#单只股票策略对象池
g_SSDict = {}
g_SSDict["baseSingal"] = signalStrategy.CBaseSignal
g_SSDict["pairTradeTickSignal"] = signalStrategy.CPairTradeTickSignal
#多只股票策略对象池
g_MSDict = {}
g_MSDict["baseMultiple"] = multipleStrategy.CBaseMultiple
g_MSDict["pairTradeParaMultiple"] = multipleStrategy.CPairTradeParaMultiple
#-----------------------
#实现函数
#-----------------------
#读取设置参数
execfile("config.ini")
#读取订阅股票
def loadSubStocks():
	global g_subStocks
	_fileReader  = open("./subStock.csv","r")
	while 1:
		line = _fileReader.readline()
		line = line.replace("\n","")
		if not line:
			break
		g_subStocks.append(line)
#创建数据连接对象
def creatDataServerLink():
	dataServerInstance = dataServerApi.CDataServerApi(HOST,PORT)
	dataServerInstance.init(g_StrategyActuatorDict)
	dataServerInstance.connectServer()
	return dataServerInstance
#创建策略对象
def creatStrategyObject(needSignal, stock):
	strategyObjDict = {}
	if needSignal:	#单信号策略
		if not SUB_SIGNALS:		#如果没有订阅
			return False
		for signalName in SUB_SIGNALS:
			strategyObjDict[signalName] = g_SSDict[signalName](stock)
		return strategyObjDict
	else:			#多信号策略
		if not SUB_MULTIPLES:	#如果没有订阅
			return False
		for multipeName in SUB_MULTIPLES:
			strategyObjDict[multipeName] = g_MSDict[multipeName]("Multiple")
			strategyObjDict[multipeName].getActuatorDict(g_StrategyActuatorDict)
		return strategyObjDict
#创建监听对象
def creatListener(bufferStack):
	global g_listenerList
	listenersNum = 3
	if len(g_subStocks) >= listenersNum:
		perListenerStocksNum = len(g_subStocks)/listenersNum
		for i in xrange(listenersNum):
			if listenersNum - i == 1:
				actuatorDict = creatActuators(g_subStocks[i*perListenerStocksNum:], bufferStack, True)
				listener = dataListener.CDataListerner(g_subStocks[i*perListenerStocksNum:], actuatorDict)
				listener.start()
			else:
				actuatorDict = creatActuators(g_subStocks[i*perListenerStocksNum:i*perListenerStocksNum+perListenerStocksNum], bufferStack, False)
				listener = dataListener.CDataListerner(g_subStocks[i*perListenerStocksNum:i*perListenerStocksNum+perListenerStocksNum], actuatorDict)
				listener.start()
			g_listenerList.append(listener)
	else:
		actuatorDict = creatActuators(g_subStocks, bufferStack, True)
		listener = dataListener.CDataListerner(g_subStocks, actuatorDict)
		listener.start()
		g_listenerList.append(listener)
#创建监听对象
def creatActuators(stocks, bufferStack, isLast):
	global g_StrategyActuatorDict
	actuatorDict = {}
	#单股票策略监听
	for stock in stocks:
		strategyObjDict = creatStrategyObject(True, stock)
		if strategyObjDict:
			bufferStack[stock]				= []
			newActuator						= strategyActuator.CStrategyActuator(bufferStack[stock])
			newActuator.getSignalStrategyObj(strategyObjDict)
			g_StrategyActuatorDict[stock]	= newActuator
			actuatorDict[stock] 			= newActuator
	if isLast:	#多股票策略监听
		strategyObjDict = creatStrategyObject(False, "Multiple")
		if strategyObjDict:
			bufferStack["Multiple"]				= []
			newActuator							= strategyActuator.CStrategyActuator(bufferStack["Multiple"])
			newActuator.getmultipleStrategyObj(strategyObjDict)
			g_StrategyActuatorDict["Multiple"]	= newActuator
			actuatorDict["Multiple"] 			= newActuator
	return actuatorDict

#主入口
def main():
	#注册策略
	#载入订阅股票代码
	loadSubStocks()
	#创建数据连接对象
	dataServerInstance = creatDataServerLink()
	#创建数据监听器
	creatListener(dataServerInstance.bufferStack)
	#订阅股票代码
	dataServerInstance.subscibeStock(SUB_ALL_STOCK, g_subStocks)
	#请求数据
	dataServerInstance.requestData(
		REQUEST_TYPE,
		REQUEST_FLAG,
		datetime.datetime.strptime(START_TIME,"%Y-%m-%d %H:%M:%S"),
		datetime.datetime.strptime(END_TIME,"%Y-%m-%d %H:%M:%S"))
	while 1:
		pass
	