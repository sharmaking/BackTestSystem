#!/usr/bin/python
# -*- coding: utf-8 -*-
# decompress.py
import dataStruct
import copy
import ctypes
import datetime

api = ctypes.windll.LoadLibrary("./DataApi_32/decompress32.dll")
#解压逐笔成交数据
def DecompressTransactionData(p, nItems):
	pTransactions = dataStruct.getTransactions(nItems)
	nSize = 0
	iData = ctypes.c_longlong(0)
	nPreTime = 0
	nPreIndex = 0
	nPrePrice = 0
	for i in xrange(nItems):
		#成交时间
		nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
		pTransactions[i]["nTime"] = nPreTime + iData.value 
		nPreTime = pTransactions[i]["nTime"]
		pTransactions[i]["nTime"] = datetime.datetime.strptime(str(nPreTime), "%H%M%S%f").time()
		#成交序号
		nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
		nPreIndex = nPreIndex + int(iData.value)
		pTransactions[i]["nIndex"] = nPreIndex
		#成交价格
		nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
		nPrePrice = nPrePrice + int(iData.value)
		pTransactions[i]["nPrice"] = round(float(nPrePrice)/10000,2)
		#成交数量
		nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
		pTransactions[i]["nVolume"] = int(round(iData.value,-2)/100)

		pTransactions[i]["nTurnover"] = pTransactions[i]["nPrice"] * pTransactions[i]["nVolume"] * 100
	return pTransactions
#解压成交队列
def DecompressOrderQueueData(p, nItems):
	pQueues, pIdnums = dataStruct.getOrderQueue(nItems)
	nSize = 0
	iData = ctypes.c_longlong(0)
	for i in xrange(nItems):
		#本日编号
		nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
		pIdnums[i] = iData.value
		#订单编号
		nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
		pQueues[i]["nTime"] = datetime.datetime.strptime(str(iData.value), "%H%M%S%f").time()
		#买卖方向(A:Ask, B:Bid)
		pQueues[i]["nSide"] = p[nSize]
		nSize = nSize + 1
		#订单价格
		nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
		pQueues[i]["nPrice"] = round(float(iData.value)/10000,2)
		#订单数量
		nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
		pQueues[i]["nOrders"] = int(iData.value)
		#队列个数
		nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
		pQueues[i]["nABItems"] = int(iData.value)
		#订单数量
		nABVolume = []
		for k in xrange(pQueues[i]["nABItems"]):
			nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
			nABVolume.append(int(round(iData.value, -2)/100))
		pQueues[i]["nABVolume"] = nABVolume
	return pQueues, pIdnums
#解压行情数据
def DecompressMarketData(p):
	pMarketData, pIdnum = dataStruct.getMarketData()
	nSize = 0
	iData = ctypes.c_longlong(0)

	nSize = api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pIdnum = iData.value
	#状态
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nStatus"]	= iData.value
	#时间
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nTime"]	= datetime.datetime.strptime(str(iData.value), "%H%M%S%f").time()
	#昨收
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nPreClose"] = round(float(iData.value)/10000,2)
	#开盘价
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nOpen"] = round(float(iData.value)/10000,2) + pMarketData["nPreClose"]
	#最高价
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nHigh"] = round(float(iData.value)/10000,2) + pMarketData["nPreClose"]
	#最低价
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nLow"]  = round(float(iData.value)/10000,2) + pMarketData["nPreClose"]
	#最新价
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nMatch"]= round(float(iData.value)/10000,2) + pMarketData["nPreClose"]
	#竞买价
	nPrice = pMarketData["nMatch"]
	if not nPrice:
		nPrice = pMarketData["nPreClose"]
	for i in xrange(10):
		nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
		pMarketData["nBidPrice"][i] = nPrice - round(float(iData.value)/10000,2)
		nPrice = pMarketData["nBidPrice"][i]
	#竞卖价
	nPrice = pMarketData["nMatch"]
	if not nPrice:
		nPrice = pMarketData["nPreClose"]
	for i in xrange(10):
		nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
		pMarketData["nAskPrice"][i] = nPrice - round(float(iData.value)/10000,2)
		nPrice = pMarketData["nAskPrice"][i]
	#竞买量
	for i in xrange(10):
		nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
		pMarketData["nBidVol"][i] = int(round(iData.value,-2)/100)
	#竞卖量
	for i in xrange(10):
		nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
		pMarketData["nAskVol"][i] = int(round(iData.value,-2)/100)
	#成交笔数
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nNumTrades"] = int(iData.value)
	#成交总量
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["iVolume"]	= int(round(iData.value,-2)/100)
	#成交总金额
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["iTurnover"]	= iData.value
	#委托买入总量
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nTotalBidVol"] = int(round(iData.value,-2)/100)
	#加权平均委买价格
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nWeightedAvgBidPrice"] = round(float(iData.value)/10000,2)
	#委托卖出总量
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nTotalAskVol"] = int(round(iData.value,-2)/100)
	#加权平均委卖价格
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nWeightedAvgAskPrice"] = round(float(iData.value)/10000,2)
	#IOPV净值估值
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nIOPV"] = iData.value
	#到期收益率
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nYieldToMaturity"] = iData.value
	#涨停价
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nHighLimited"] = pMarketData["nPreClose"] + round(float(iData.value)/10000,2)
	#跌停价
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nLowLimited"] = pMarketData["nPreClose"] + round(float(iData.value)/10000,2)
	pMarketData["chPrefix"] = p[nSize:nSize+4]
	nSize = nSize + 4;
	return nSize, pMarketData, pIdnum
#解压期货行情数据
def DecompressMarketData_Futures(p):
	pMarketData = dataStruct.getFutureMarketData()
	nSize = 0
	iData = ctypes.c_longlong(0)

	nSize = api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nIndex"]	= iData.value
	#状态
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nStatus"]	= iData.value
	#时间
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nTime"]	= datetime.datetime.strptime(str(iData.value), "%H%M%S%f").time()
	#昨持仓
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["iPreOpenInterest"] = int(iData.value)
	#前收盘价
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nPreClose"] = round(float(iData.value)/10000,2)
	#昨日结算
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nPreSettlePrice"] = round(float(iData.value)/10000,2)
	#开盘价
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nOpen"] = round(float(iData.value)/10000,2) + pMarketData["nPreClose"]
	#最高价
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nHigh"] = round(float(iData.value)/10000,2) + pMarketData["nPreClose"]
	#最低价
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nLow"]  = round(float(iData.value)/10000,2) + pMarketData["nPreClose"]
	#最新价
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nMatch"]= round(float(iData.value)/10000,2) + pMarketData["nPreClose"]
	#成交总量
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["iVolume"]	= int(iData.value)
	#成交总金额
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["iTurnover"] = round(float(iData.value)/10000,2)
	#持仓
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["iOpenInterest"] = int(iData.value)
	#收盘价
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nClose"] = round(float(iData.value)/10000,2)
	#结算价
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nSettlePrice"] = round(float(iData.value)/10000,2)
	#涨停价
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nHighLimited"] = round(float(iData.value)/10000,2)
	#跌停价
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nLowLimited"] = round(float(iData.value)/10000,2)
	#昨虚实度
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nPreDelta"] = iData.value
	#今虚实度
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nCurrDelta"] = iData.value
	#竞买价
	nPrice = pMarketData["nMatch"]
	if not nPrice:
		nPrice = pMarketData["nPreClose"]
	for i in xrange(5):
		nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
		pMarketData["nBidPrice"][i] = nPrice - round(float(iData.value)/10000,2)
		pMarketData["nBidPrice"][i] = round(pMarketData["nBidPrice"][i], 2)
		nPrice = pMarketData["nBidPrice"][i]
	#竞卖价
	nPrice = pMarketData["nMatch"]
	if not nPrice:
		nPrice = pMarketData["nPreClose"]
	for i in xrange(5):
		nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
		pMarketData["nAskPrice"][i] = nPrice - round(float(iData.value)/10000,2)
		pMarketData["nAskPrice"][i] = round(pMarketData["nBidPrice"][i], 2)
		nPrice = pMarketData["nAskPrice"][i]
	#竞买量
	for i in xrange(5):
		nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
		pMarketData["nBidVol"][i] = int(iData.value)
	#竞卖量
	for i in xrange(5):
		nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
		pMarketData["nAskVol"][i] = int(iData.value)
	return nSize, pMarketData
#解压指数数据
def DecompressIndexData(p):
	pMarketData = dataStruct.getIndexMarketData()
	nSize = 0
	iData = ctypes.c_longlong(0)
	#本日编号
	nSize = api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nIndex"] = iData.value
	#时间
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nTime"]  = datetime.datetime.strptime(str(iData.value), "%H%M%S%f").time()
	#今日开盘指数
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nOpenIndex"] = round(float(iData.value)/10000,2)
	#今日最高指数
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nHighIndex"] = round(float(iData.value)/10000,2) + pMarketData["nOpenIndex"]
	#今日最低指数
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nLowIndex"]  = round(float(iData.value)/10000,2) + pMarketData["nOpenIndex"]
	#今日最新指数
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nLastIndex"] = round(float(iData.value)/10000,2) + pMarketData["nOpenIndex"]
	#参与计算相应指数的交易数量
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["iTotalVolume"]	= int(iData.value)
	#参与计算相应指数的成交金额
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["iTurnover"]	= round(float(iData.value)/100,2)
	#前收指数
	nSize = nSize + api.decompressData(ctypes.addressof(iData), ctypes.c_char_p(p[nSize:]))
	pMarketData["nPreCloseIndex"] = round(float(iData.value)/10000,2) + pMarketData["nOpenIndex"]
	return nSize, pMarketData