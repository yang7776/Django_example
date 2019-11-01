from django.shortcuts import render, HttpResponse

from dwebsocket.decorators import accept_websocket, require_websocket
from collections import defaultdict

"""
dwebsocket有两种装饰器：require_websocket和accept_websocekt，使用require_websocket装饰器会导致视图函数无法接收导致正常的http请求，一般情况使用accept_websocket方式就可以了，

dwebsocket的一些内置方法：

request.is_websocket（）：判断请求是否是websocket方式，是返回true，否则返回false
request.websocket： 当请求为websocket的时候，会在request中增加一个websocket属性，
WebSocket.wait（） 返回客户端发送的一条消息，没有收到消息则会导致阻塞
WebSocket.read（） 和wait一样可以接受返回的消息，只是这种是非阻塞的，没有消息返回None
WebSocket.count_messages（）返回消息的数量
WebSocket.has_messages（）返回是否有新的消息过来
WebSocket.send（message）像客户端发送消息，message为byte类型
"""
# 保存所有接入的用户地址(真正使用时，存入数据库，针对用户是否登录，判断临时存储还是持续性存储)
allconn = defaultdict(list)
@accept_websocket
def ws_chat(request, userid):
	# 获取用户信息
	allresult = {
		"user_id":userid,
		"user_name":"杨先生"
	}
	# 声明全局变量
	global allconn
	if not request.is_websocket():  # 判断是不是websocket连接
		try:  # 如果是普通的http方法
			message = request.GET['message']
			return HttpResponse(message)
		except:
			return render(request, 'chat.html', allresult)
	else:
		# 将链接(请求？)存入全局字典中
		allconn[str(userid)] = request.websocket
		# 遍历请求地址中的消息
		for message in request.websocket:
			if message:
				# 将信息发至自己的聊天框（即在聊天室看到自己发送的消息）
				request.websocket.send(message)
				# 将信息发至其他所有用户的聊天框（将自己的消息发送给其他所有用户，当然也可以在此指定用户）
				for i in allconn:
					if i != str(userid):  # 遍历userid，但不包括自己的userid
						allconn[i].send(message)