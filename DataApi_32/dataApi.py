#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import socketFun
import time
import thread

class CDataApi(socket.socket):
	def __init__(self, HOST, PORT):
		super(CDataApi, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
		self.ADDR = (HOST, PORT)
		self.connectState = True
	#链接服务器
	def connectServer(self):
		self.connect(self.ADDR)
		time.sleep(2)
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
			return
		thread.start_new_thread(socketFun.recvSubscibeRespond, (self,1)) 
		#socketFun.recvSubscibeRespond(self)
	#----------------------------
	#需重载函数
	#----------------------------
	#初始化接口
	def init(self):
		pass
	#数据接收接口
	def onRtnDepthMarketData(self, dataType, data):
		pass
	#数据传输结束
	def onRtnDataEnd(self):
		print "DataEnd"