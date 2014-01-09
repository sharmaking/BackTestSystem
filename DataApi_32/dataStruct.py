#!/usr/bin/python
# -*- coding: utf-8 -*-
# dataStruct.py
#逐笔成交
import numpy as np
import datetime
import copy
#-----------------------------
#标准解压结构体
#-----------------------------
#单笔逐笔成交
AD_Transaction = {
	"idx" : 0,							#在包中的编号
	"chSecurityCode" : "00000000",		#证券代码
	"b_isHistoryData" : True,
	"nCurDate" : 0,
	"nCurTime" : 0,
	"nDate" : 0,						#成交日期
	"nTime" : 0,						#成交时间
	"nIndex" : 0,						#成交编号
	"nPrice" : 0,						#成交价格
	"nVolume" : 0,						#成交数量
	"nTurnover" : 0 					#成交金额
}
#成交队列
AD_OrderQueue = {
	"b_isHistoryData" : True,
	"nCurDate" : 0,
	"nCurTime" : 0,
	"chSecurityCode" : "00000000",		#证券代码
	"nDate" : 0,
	"nTime" : 0,
	"nSide" : 0,						#买卖方向（B：bid，S：Ask）
	"nPrice" : 0,						#成交价格
	"nOrders" : 0,						#订单数量
	"nABItems" : 0,						#明细个数
	"nABVolume" : []					#订单明细
}
#股票行情数据
MarketDataForTrade = {
	"nindex" : 0,					#行情编号
	"chSecurityCode" : "00000000",	#证券代码
	"b_isHistoryData" : True,		#是否历史数据
	"nCurDate" : 0,					#当前日期
	"nCurTime" : 0,					#当前时间
	"nDate" : 0,					#数据的日期
	"nTime" : 0,					#数据的时间
	"nStatus" : 0,					#行情状态
	"deep" : 10,					#行情长度
	"mConversionRate" : 0,			#折算率
	"nPreClose" : 0,				#昨日收盘价
	"nOpen" : 0,					#开盘价
	"nHigh" : 0,					#最高价
	"nLow" : 0,						#最低价
	"nMatch" : 0,					#最新价
	"nAskPrice" : [0]*10,			#申卖价
	"nAskVol" : [0]*10,				#申卖量
	"nBidPrice" : [0]*10,			#申买价
	"nBidVol" : [0]*10,				#申买量
	"nNumTrades" : 0,				#成交笔数
	"iVolume" : np.int64(0),		#成交总量
	"iTurnover" : np.int64(0),		#成交总金额
	"nTotalBidVol" : np.int64(0),	#委托买入总量
	"nTotalAskVol" : np.int64(0),	#委托卖出总量
	"nWeightedAvgBidPrice" : 0,		#加权平均委买价格
	"nWeightedAvgAskPrice" : 0,		#加权平均委卖价格
	"nIOPV" : 0,					#IOPV净值估值
	"nYieldToMaturity" : 0,			#到期收益率
	"nHighLimited" : 0,				#涨停价
	"nLowLimited" : 0,				#跌停价
	"chPrefix" : 0
}
#期货行情数据
MarketDataForTrade_Future = {
	"chSecurityCode" : "00000000",	#期货代码
	"nIndex" : 0,					#期货编号
	"nDate" : 0,					#日期 yyyymmdd
	"nTime" : 0,					#时间(HHMMSSmmmm)
	"nStatus" : 0,					#状态
	"iPreOpenInterest" : 0,			#昨持仓
	"nPreClose" : 0,				#昨收盘价
	"nPreSettlePrice" : 0,			#昨结算
	"nOpen" : 0,					#开盘价	
	"nHigh" : 0,					#最高价
	"nLow" : 0,						#最低价
	"nMatch" : 0,					#最新价
	"iVolume" : np.int64(0),		#成交总量
	"iTurnover" : np.int64(0),		#成交总金额
	"iOpenInterest" : np.int64(0),	#持仓总量
	"nClose" : 0,					#今收盘
	"nSettlePrice" : 0,				#今结算
	"nHighLimited" : 0,				#涨停价
	"nLowLimited" : 0,				#跌停价
	"nPreDelta": 0,					#昨虚实度
	"nCurrDelta" : 0,				#今虚实度
	"nAskPrice" : [0]*5,			#申卖价
	"nAskVol" : [0]*5,				#申卖量
	"nBidPrice" : [0]*5,			#申买价
	"nBidVol" : [0]*5				#申买量
}
#指数行情数据
AD_Index = {
	"chSecurityCode" : "00000000",	#指数代码
	"nIndex" : 0,					#指数编号
	"nDate" : 0,					#日期 yyyymmdd
	"nTime" : 0,					#时间(HHMMSSmmmm)
	"nOpenIndex" : 0,				#今开盘指数
	"nHighIndex" : 0,				#最高指数
	"nLowIndex" : 0,				#最低指数
	"nLastIndex" : 0,				#最新指数
	"iTotalVolume" : 0,				#参与计算相应指数的交易数量 单位手
	"iTurnover" : 0,				#参与计算相应指数的成交金额 单位万元
	"nPreCloseIndex" : 0			#前收盘指数
}
#-----------------------------
#标准计算结构体
#-----------------------------
#标准行情结构体
StandardMarketData = {
	"stockCode" : "000000",			#合约代码、股票代码、指数代码
	"stockName"	: "",				#合约名称、股票名称
	"dateTime"	: 0,				#行情数据时间, dateime.datetime对象
	"open"		: 0,				#开盘价
	"high"		: 0,				#最高价
	"low"		: 0,				#最低价
	"close"		: 0,				#收盘价，最新价
	"vol"		: 0,				#成交量
	"askPrice"	: [0]*10,			#申卖价
	"askVol"	: [0]*10,			#申卖量
	"bidPrice"	: [0]*10,			#申买价
	"bidVol"	: [0]*10,			#申买量
	"preClose"	: 0,				#昨收
	"highLimited" : 0,				#涨停价
	"lowLimited" : 0,				#跌停价
	"dOpen"		: 0,				#今日开盘
	"dHigh"		: 0,				#今日最高
	"dLow"		: 0 				#今日最低
}
StandardTransaction = {
	"stockCode" : "000000",			#合约代码、股票代码、指数代码
	"stockName"	: "",				#合约名称、股票名称
	"dateTime"	: 0,				#行情数据时间, dateime.datetime对象
	"index" : 0,					#成交编号
	"price" : 0,					#成交价格
	"vol" : 0						#成交数量
}
StandardOrderQueue = {
	"stockCode" : "000000",			#合约代码、股票代码、指数代码
	"stockName"	: "",				#合约名称、股票名称
	"dateTime"	: 0,				#行情数据时间, dateime.datetime对象
	"side" : 0,						#买卖方向（B：bid，S：Ask）
	"price" : 0,					#成交价格
	"orders" : 0,					#订单数量
	"ABItems" : 0,					#明细个数
	"ABVolume" : []					#订单明细
}
#-----------------------------
#获取解压结构体函数
#-----------------------------
#获得逐笔成交包
def getTransactions(nItems):
	pTransactions = []
	for i in range(nItems):
		pTransactions.append(copy.copy(AD_Transaction))
	return pTransactions
#获得买一队列包
def getOrderQueue(nItems):
	pQueues = []
	pIdnums = []
	for i in range(nItems):
		pQueues.append(copy.copy(AD_OrderQueue))
		pIdnums.append(0)
	return pQueues, pIdnums
#获得股票行情数据
def getMarketData():
	return copy.copy(MarketDataForTrade), 0
#获得期货行情数据
def getFutureMarketData():
	return copy.copy(MarketDataForTrade_Future)
#获得指数数据
def getIndexMarketData():
	return copy.copy(AD_Index)
#-----------------------------
#将解压的数据结构体转换成标准的数据结构
#-----------------------------
#转换股票行情数据
def formatStockMarketData(pMarketDataForTrade, chSymbol):
	pStandard = copy.copy(StandardMarketData)
	pStandard["stockCode"]	= pMarketDataForTrade["chSecurityCode"]		#合约代码、股票代码、指数代码
	pStandard["stockName"]	= chSymbol									#合约名称、股票名称
	dateTimeStr = "%s %s" %(str(pMarketDataForTrade["nDate"]), pMarketDataForTrade["nTime"].strftime("%H:%M:%S.%f"))
	pStandard["dateTime"]	= datetime.datetime.strptime(dateTimeStr,"%Y-%m-%d %H:%M:%S.%f")
	pStandard["open"]		= pMarketDataForTrade["nMatch"]				#开盘价
	pStandard["high"]		= pMarketDataForTrade["nMatch"]				#最高价
	pStandard["low"]		= pMarketDataForTrade["nMatch"]				#最低价
	pStandard["close"]		= pMarketDataForTrade["nMatch"]				#收盘价，最新价
	pStandard["vol"]		= pMarketDataForTrade["iVolume"]			#成交总量
	pStandard["askPrice"]	= pMarketDataForTrade["nAskPrice"]			#申卖价
	pStandard["askVol"]		= pMarketDataForTrade["nAskVol"]			#申卖量
	pStandard["bidPrice"]	= pMarketDataForTrade["nBidPrice"]			#申买价
	pStandard["bidVol"]		= pMarketDataForTrade["nBidVol"]			#申买量
	pStandard["preClose"]	= pMarketDataForTrade["nPreClose"]			#昨收
	pStandard["highLimited"] = pMarketDataForTrade["nHighLimited"]		#涨停价
	pStandard["lowLimited"] = pMarketDataForTrade["nLowLimited"]		#跌停价
	pStandard["dOpen"]		= pMarketDataForTrade["nOpen"]				#今日开盘
	pStandard["dHigh"]		= pMarketDataForTrade["nHigh"]				#今日最高
	pStandard["dLow"]		= pMarketDataForTrade["nLow"]				#今日最低
	return pStandard
#转换期货行情数据
def formatFutureMarketData(pFutureMarketData, chSymbol):
	pStandard = copy.copy(StandardMarketData)
	pStandard["stockCode"]	= pFutureMarketData["chSecurityCode"]		#合约代码、股票代码、指数代码
	pStandard["stockName"]	= chSymbol									#合约名称、股票名称
	dateTimeStr = "%s %s" %(str(pFutureMarketData["nDate"]), pFutureMarketData["nTime"].strftime("%H:%M:%S.%f"))
	pStandard["dateTime"]	= datetime.datetime.strptime(dateTimeStr,"%Y-%m-%d %H:%M:%S.%f")
	pStandard["open"]		= pFutureMarketData["nMatch"]				#开盘价
	pStandard["high"]		= pFutureMarketData["nMatch"]				#最高价
	pStandard["low"]		= pFutureMarketData["nMatch"]				#最低价
	pStandard["close"]		= pFutureMarketData["nMatch"]				#收盘价，最新价
	pStandard["vol"]		= pFutureMarketData["iVolume"]				#成交总量
	pStandard["askPrice"]	= pFutureMarketData["nAskPrice"]			#申卖价
	pStandard["askVol"]		= pFutureMarketData["nAskVol"]				#申卖量
	pStandard["bidPrice"]	= pFutureMarketData["nBidPrice"]			#申买价
	pStandard["bidVol"]		= pFutureMarketData["nBidVol"]				#申买量
	pStandard["preClose"]	= pFutureMarketData["nPreClose"]			#昨收
	pStandard["highLimited"] = pFutureMarketData["nHighLimited"]		#涨停价
	pStandard["lowLimited"] = pFutureMarketData["nLowLimited"]			#跌停价
	pStandard["dOpen"]		= pFutureMarketData["nOpen"]				#今日开盘
	pStandard["dHigh"]		= pFutureMarketData["nHigh"]				#今日最高
	pStandard["dLow"]		= pFutureMarketData["nLow"]					#今日最低
	return pStandard
#转换指数行情数据
def formatIndexMarketData(pIndexMarketData, chSymbol):
	pStandard = copy.copy(StandardMarketData)
	pStandard["stockCode"]	= pIndexMarketData["chSecurityCode"]		#合约代码、股票代码、指数代码
	pStandard["stockName"]	= chSymbol									#合约名称、股票名称
	dateTimeStr = "%s %s" %(str(pIndexMarketData["nDate"]), pIndexMarketData["nTime"].strftime("%H:%M:%S.%f"))
	pStandard["dateTime"]	= datetime.datetime.strptime(dateTimeStr,"%Y-%m-%d %H:%M:%S.%f")
	pStandard["open"]		= pIndexMarketData["nLastIndex"]			#开盘价
	pStandard["high"]		= pIndexMarketData["nLastIndex"]			#最高价
	pStandard["low"]		= pIndexMarketData["nLastIndex"]			#最低价
	pStandard["close"]		= pIndexMarketData["nLastIndex"]			#收盘价，最新价
	pStandard["vol"]		= pIndexMarketData["iTotalVolume"]			#成交总量
	pStandard["preClose"]	= pIndexMarketData["nPreCloseIndex"]		#昨收
	pStandard["dOpen"]		= pIndexMarketData["nOpenIndex"]			#今日开盘
	pStandard["dHigh"]		= pIndexMarketData["nHighIndex"]			#今日最高
	pStandard["dLow"]		= pIndexMarketData["nLowIndex"]				#今日最低
	return pStandard
#转换逐笔成绩数据
def formatTransaction(pTransaction, chSymbol):
	pStandard = copy.copy(StandardTransaction)
	pStandard["stockCode"]	= pTransaction["chSecurityCode"]		#合约代码、股票代码、指数代码
	pStandard["stockName"]	= chSymbol								#合约名称、股票名称
	dateTimeStr = "%s %s" %(str(pTransaction["nDate"]), pTransaction["nTime"].strftime("%H:%M:%S.%f"))
	pStandard["dateTime"]	= datetime.datetime.strptime(dateTimeStr,"%Y-%m-%d %H:%M:%S.%f")
	pStandard["index"]		= pTransaction["nIndex"]				#成交编号
	pStandard["price"]		= pTransaction["nPrice"]				#成交价格
	pStandard["vol"]		= pTransaction["nVolume"]				#成交数量
	return pStandard
#转换买一队列
def formatOrderQueue(pOrderQueue, chSymbol):
	pStandard = copy.copy(StandardOrderQueue)
	pStandard["stockCode"]	= pOrderQueue["chSecurityCode"]		#合约代码、股票代码、指数代码
	pStandard["stockName"]	= chSymbol								#合约名称、股票名称
	dateTimeStr = "%s %s" %(str(pOrderQueue["nDate"]), pOrderQueue["nTime"].strftime("%H:%M:%S.%f"))
	pStandard["dateTime"]	= datetime.datetime.strptime(dateTimeStr,"%Y-%m-%d %H:%M:%S.%f")
	pStandard["side"]		= pOrderQueue["nSide"]				#买卖方向（B：bid，S：Ask）
	pStandard["price"]		= pOrderQueue["nPrice"]				#成交价格
	pStandard["orders"]		= pOrderQueue["nOrders"]			#订单数量
	pStandard["ABItems"]	= pOrderQueue["nABItems"]			#明细个数
	pStandard["ABVolume"]	= pOrderQueue["nABVolume"]			#订单明细
	return pStandard