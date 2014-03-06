#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket, datetime, time
import socketFun

class CDataApi(socket.socket):
	def __init__(self, HOST, PORT, bufferStack):
		super(CDataApi, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
		self.ADDR = (HOST, PORT)
		self.connectState = True
		self.bufferStack = bufferStack	#每个合约一个堆栈
		self.preDataTime = datetime.datetime(1990,1,1,0,0,0)
	#链接服务器
	def connectServer(self):
		self.connect(self.ADDR)
		time.sleep(1)
	#订阅股票
	def subscibeStock(self, isAllMarket, subStocks):
		socketFun.subscibeStock(self, isAllMarket, subStocks)
	#请求数据
	def requestData(self, requestType, flag, startTime, endTime):
		if requestType == 0:		#请求当天数据
			socketFun.requestCurrentDay(self, flag, startTime.time())
		elif requestType == 1:		#请求某一天数据
			socketFun.requestOneDay(self, startTime.date(), startTime.time(), endTime.time())
		elif requestType == 2:		#请求某一段时间数据
			socketFun.requestSomeTimes(self, startTime.date(), endTime.date())
		else:
			print "Request illegal Param"
	#启动执行
	def run(self):
		socketFun.recvSubscibeRespond(self, 1)
	#----------------------------
	#需重载函数
	#----------------------------
	#初始化接口
	def init(self):
		pass
	#数据接收接口
	def onRtnDepthMarketData(self, dataType, data):
		self.bufferStack[data["stockCode"][:6]].put((dataType,data))
		if self.bufferStack.has_key("Multiple"):
			if dataType == 3 or dataType == 4 or dataType == 5:
				self.bufferStack["Multiple"].put((dataType,data))
		if data["dateTime"].date() != self.preDataTime.date():
			self.onRtnDayEnd()
		self.preDataTime = data["dateTime"]
	#日期切换
	def onRtnDayEnd(self):
		self.bufferStack["__SystemMessage__"].put("DayEnd")
		print "DayEnd", self.preDataTime
	#数据传输结束
	def onRtnDataEnd(self):
		self.bufferStack["__SystemMessage__"].put("DataEnd")
		print "DataEnd"