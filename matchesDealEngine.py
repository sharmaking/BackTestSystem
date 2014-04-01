#!/usr/bin/python
# -*- coding: utf-8 -*-
#matchesDealEngine.py
import os, random

class CMatchesDealEngine(object):
	def __init__(self, stockCode, stragety):
		super(CMatchesDealEngine, self).__init__()
		self.stockCode		= stockCode
		self.stragety		= stragety
		self.currentMDData	= 0
		self.dealHistory	= []	#成交历史
		self.dealDict		= {}	#当前报单
		self.positions 		= []	#当前持仓
		#撮合日志文件
		self.logFile		= "./log/matchesDeal_%s.csv"%self.stockCode
	#行情数据触发函数
	def onRtnMarketData(self, data):
		self.currentMDData	= data
	#逐笔成交触发函数
	def onRtnTradeSettlement(self, data):
		if self.dealDict:
			for tradeId, dealObj in self.dealDict.items():
				self.matchesTD(dealObj, data)
	#------------------------------
	#交易方法
	#------------------------------
	#买报单
	def buy(self, mode, price, vol, dateTime):
		#生成交易ID
		tradeId = "%s_%d"%(dateTime.time(),random.randint(0, 100))
		#mode 1 限价委托，2市价委托(自动改成能成交的价格)(普通)，3市价委托(激进)
		self.saveTradeLog("%s,%s,%s,请求报单,买,%f,%d,0,报单成功\n"%(
			tradeId, self.stockCode, str(self.currentMDData["dateTime"]),price, vol))
		preVol = 0
		if mode == 2:
			price = self.currentMDData["bidPrice"][0]
			preVol = self.currentMDData["bidVol"][0]
			self.saveTradeLog("%s,%s,%s,改价买一,买,%f,%d,0,成功\n"%(
				tradeId, self.stockCode, str(self.currentMDData["dateTime"]),price, vol))
		elif mode == 3:
			price = self.currentMDData["askPrice"][0]
			self.saveTradeLog("%s,%s,%s,改价卖一,买,%f,%d,0,成功\n"%(
				tradeId, self.stockCode, str(self.currentMDData["dateTime"]),price, vol))
		self.dealDict[tradeId] = {
			"tradeId"	: tradeId,
			"requstTime": dateTime,
			"direction"	: "buy",
			"price"		: price,
			"vol"		: vol,
			"preVol"	: preVol,	#排单量
			"status"	: "quoted",	#quoted 已报, failed 废单, partial 步成, successed 成交
			"dealVol"	: 0,
			"dealDetail" : []		#成交明细
		}
		if mode == 3:
			self.matchesMD(self.dealDict[tradeId])
		return tradeId
	def sell(self, mode, price, vol, dateTime):
		#生成交易ID
		tradeId = "%s_%d"%(dateTime.time(),random.randint(0, 100))
		#mode 1 限价委托，2市价委托(自动改成能成交的价格)(普通)，3市价委托(激进)
		self.saveTradeLog("%s,%s,%s,请求报单,卖,%f,%d,0,报单成功\n"%(
			tradeId, self.stockCode, str(self.currentMDData["dateTime"]),price, vol))
		preVol = 0
		if mode == 2:
			price = self.currentMDData["askPrice"][0]
			preVol = self.currentMDData["askVol"][0]
			self.saveTradeLog("%s,%s,%s,改价卖一,卖,%f,%d,0,成功\n"%(
				tradeId, self.stockCode, str(self.currentMDData["dateTime"]),price, vol))
		elif mode == 3:
			price = self.currentMDData["bidPrice"][0]
			self.saveTradeLog("%s,%s,%s,改价买一,卖,%f,%d,0,成功\n"%(
				tradeId, self.stockCode, str(self.currentMDData["dateTime"]),price, vol))
		self.dealDict[tradeId] = {
			"tradeId"	: tradeId,
			"requstTime": dateTime,
			"direction"	: "buy",
			"price"		: price,
			"vol"		: vol,
			"preVol"	: preVol,	#排单量
			"status"	: "quoted",	#quoted 已报, failed 废单, partial 步成, successed 成交
			"dealVol"	: 0,
			"dealDetail" : []		#成交明细
		}
		#if mode == 3:
		#	self.matchesMD(self.dealDict[tradeId])
		return tradeId
	#检查交易状态
	def checkTradeStatus(self, tradeId):
		if self.dealDict.has_key(tradeId):
			return self.dealDict[tradeId]
		else:
			for dealObj in self.dealHistory[::-1]:
				if dealObj["tradeId"] == tradeId:
					return dealObj
	#撤单
	def cancelTrade(self, tradeId):
		if not self.dealDict.has_key(tradeId):
			return False
		self.saveTradeLog("%s,%s,%s,撤单,买,%f,%d,%d,成功\n"%(
			tradeId, self.stockCode, str(self.currentMDData["dateTime"]), self.dealDict[tradeId]["price"], self.dealDict[tradeId]["vol"], self.dealDict[tradeId]["vol"] - self.dealDict[tradeId]["dealVol"]))
		self.dealDict[tradeId]["vol"] = self.dealDict[tradeId]["dealVol"]
		self.dealHistory.append(self.dealDict[tradeId])
		del self.dealDict[tradeId]
		return True
	#改价格
	def changePrice(self, tradeId):
		if not self.dealDict.has_key(tradeId):
			return False
		else:
			if self.dealDict[tradeId]["direction"] == "sell":
				self.dealDict[tradeId]["price"] = self.currentMDData["bidPrice"][0]
				vol = self.currentMDData["bidVol"][0]
				dealVol = vol
				if dealObj["vol"] - dealObj["dealVol"] <= vol:
					dealVol = dealObj["vol"] - dealObj["dealVol"]
				dealObj["dealVol"] += dealVol
				dealObj["dealDetail"].append((self.currentMDData["dateTime"], dealObj["price"], dealVol))
				#更新持仓
				self.updatePositions("sell", dealVol)
				#记录交易日志
				self.saveTradeLog("%s,%s,%s,改价行情撮合,卖,%f,%d,%d,成功\n"%(
					tradeId, self.stockCode, str(self.currentMDData["dateTime"]), dealObj["price"], dealObj["vol"], dealVol))
				#通知完全成交
				if dealObj["dealVol"] == dealObj["vol"]:
					self.dealHistory.append(dealObj)
					self.dealed(dealObj, self.currentMDData["dateTime"])
					del self.dealDict[dealObj["tradeId"]]
		return True
	#------------------------------
	#报单回调
	#------------------------------
	#报单成交明细
	def dealed(self, dealObj, dateTime):				#成交明细
		vol = 0
		price = 0
		for _dateTime, _price, _vol in dealObj["dealDetail"]:
			vol += _vol
			price += _price*_vol
		price = price/vol
		self.stragety.dealed(dealObj, price, vol, dateTime)
	#报单失败
	def quotedFailed(self, failedCode):			#失败原因
		self.stragety.quotedFailed(failedCode)
	#------------------------------
	#撮合仿佛
	#------------------------------
	#行情报价撮合
	def matchesMD(self, dealObj):
		if dealObj["direction"] == "buy":
			vol = self.currentMDData["askVol"][0]
			dealVol = vol
			if dealObj["vol"] - dealObj["dealVol"] <= vol:
				dealVol = dealObj["vol"] - dealObj["dealVol"]
			dealObj["dealVol"] += dealVol
			dealObj["dealDetail"].append((self.currentMDData["dateTime"], dealObj["price"], dealVol))
			#更新持仓
			self.updatePositions("buy", dealVol)
			#记录交易日志
			self.saveTradeLog("%s,%s,%s,行情撮合,买,%f,%d,%d,成功\n"%(
				dealObj["tradeId"], self.stockCode, str(self.currentMDData["dateTime"]), dealObj["price"], dealObj["vol"], dealVol))
			#通知完全成交
			if dealObj["dealVol"] == dealObj["vol"]:
				self.dealHistory.append(dealObj)
				self.dealed(dealObj, self.currentMDData["dateTime"])
				del self.dealDict[dealObj["tradeId"]]
	#逐笔成交撮合
	def matchesTD(self, dealObj, tdData):
		if dealObj["direction"] == "buy":
			if tdData["price"] == dealObj["price"]:
				vol = tdData["vol"]
				dealVol = 0
				#计算是否能成交到自己
				if dealObj["preVol"]:
					dealObj["preVol"] = dealObj["preVol"] - vol
					vol = vol - dealObj["preVol"]
					if dealObj["preVol"] < 0:
						dealObj["preVol"] = 0
					else:
						vol = 0
				dealVol = vol
				#更新持仓
				self.updatePositions("buy", dealVol)
				#计算是否全部成交
				if dealVol:
					if dealObj["vol"] - dealObj["dealVol"] <= vol:
						dealVol = dealObj["vol"] - dealObj["dealVol"]
					dealObj["dealVol"] += dealVol
					dealObj["dealDetail"].append((tdData["dateTime"], tdData["price"], dealVol))
					self.saveTradeLog("%s,%s,%s,逐笔撮合,买,%f,%d,%d,成功\n"%(
						dealObj["tradeId"], self.stockCode, str(tdData["dateTime"]), tdData["price"], dealObj["vol"], dealVol))
			elif tdData["price"] < dealObj["price"]:
				#将剩下的全部成交
				dealObj["preVol"] = 0
				dealVol = dealObj["vol"] - dealObj["dealVol"]
				dealObj["dealVol"] += dealVol
				#更新持仓
				self.updatePositions("buy", dealVol)
				dealObj["dealDetail"].append((tdData["dateTime"], dealObj["price"], dealVol))
				self.saveTradeLog("%s,%s,%s,逐笔撮合,买,%f,%d,%d,成功\n"%(
					dealObj["tradeId"], self.stockCode, str(tdData["dateTime"]), dealObj["price"], dealObj["vol"], dealVol))
			#通知完全成交
			if dealObj["dealVol"] == dealObj["vol"]:
				self.dealHistory.append(dealObj)
				self.dealed(dealObj, tdData["dateTime"])
				del self.dealDict[dealObj["tradeId"]]
		elif dealObj["direction"] == "sell":
			if tdData["price"] == dealObj["price"]:
				vol = tdData["vol"]
				dealVol = 0
				#计算是否能成交到自己
				if dealObj["preVol"]:
					dealObj["preVol"] = dealObj["preVol"] - vol
					vol = vol - dealObj["preVol"]
					if dealObj["preVol"] < 0:
						dealObj["preVol"] = 0
					else:
						vol = 0
				dealVol = vol
				#更新持仓
				self.updatePositions("sell", dealVol)
				#计算是否全部成交
				if dealVol:
					if dealObj["vol"] - dealObj["dealVol"] <= vol:
						dealVol = dealObj["vol"] - dealObj["dealVol"]
					dealObj["dealVol"] += dealVol
					dealObj["dealDetail"].append((tdData["dateTime"], tdData["price"], dealVol))
					self.saveTradeLog("%s,%s,%s,逐笔撮合,卖,%f,%d,%d,成功\n"%(
						dealObj["tradeId"], self.stockCode, str(tdData["dateTime"]), tdData["price"], dealObj["vol"], dealVol))
			elif tdData["price"] > dealObj["price"]:
				#将剩下的全部成交
				dealObj["preVol"] = 0
				dealVol = dealObj["vol"] - dealObj["dealVol"]
				dealObj["dealVol"] += dealVol
				#更新持仓
				self.updatePositions("sell", dealVol)
				dealObj["dealDetail"].append((tdData["dateTime"], dealObj["price"], dealVol))
				self.saveTradeLog("%s,%s,%s,逐笔撮合,卖,%f,%d,%d,成功\n"%(
					dealObj["tradeId"], self.stockCode, str(tdData["dateTime"]), dealObj["price"], dealObj["vol"], dealVol))
			#通知完全成交
			if dealObj["dealVol"] == dealObj["vol"]:
				self.dealHistory.append(dealObj)
				self.dealed(dealObj, tdData["dateTime"])
				del self.dealDict[dealObj["tradeId"]]
	#更新持仓状态
	def updatePositions(self, direction, dealVol):
		if not self.positions:
			self.positions = [direction, dealVol]
		else:
			if self.positions[0] == "buy":
				if direction == "buy":
					self.positions[1] += dealVol
				else:
					self.positions[1] -= dealVol
					if self.positions[1] < 0:
						self.positions[0] = "sell"
						self.positions[1] = 0 - self.positions[1]
			elif self.positions[0] == "sell":
				if direction == "sell":
					self.positions[1] += dealVol
				else:
					self.positions[1] -= dealVol
					if self.positions[1] < 0:
						self.positions[0] = "buy"
						self.positions[1] = 0 - self.positions[1]
	#记录交易日志
	def saveTradeLog(self, tradeStr):
		if not os.path.isfile(self.logFile):
			tradeStr = "ID识别码,股票代码,时间,操作类型,方向,价位,量,成交量,状态\n" + tradeStr
		logFile = open(self.logFile, "a")
		logFile.write(tradeStr)
		logFile.close()

