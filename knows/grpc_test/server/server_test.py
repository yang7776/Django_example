import grpc,time

from concurrent import futures
from knows.grpc_test.example import test_pb2_grpc, test_pb2

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_HOST = "localhost"
_PORT = "8080"

class TestData(test_pb2_grpc.TestDataServicer):
    def GetInfo(self, request, context):
        username = request.username
        password = request.password
        if username != "ete":
            res_code = 400
            message = "用户名错误"
        else:
            if password != "123456":
                res_code = 400
                message = "密码错误"
            else:
                res_code = 200
                message = "登录成功"

        return test_pb2.TestResponse(
            code=res_code,
            message = message,
        )

def server():
    # 创建一个服务器，设置最大连接数
    testServer = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    # 给派生类添加一个接口服务
    test_pb2_grpc.add_TestDataServicer_to_server(TestData(), testServer)
    # 添加监听端口
    testServer.add_insecure_port(_HOST + ":" + _PORT)
    # 开启服务
    testServer.start()
    try:
        while True:
            print("服务器已开启")
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        # 关闭服务
        testServer.stop(0)

if __name__ == "__main__":
    server()