import grpc,time,json
from concurrent import futures
from knows.grpc_test.example import test_pb2_grpc, test_pb2
from google.protobuf.json_format import  Parse,MessageToJson
# 定义相关参数（推迟服务执行时间，服务器ip，服务器端口）
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
        res = test_pb2.TestResponse()
        # 可将复杂“嵌套”的数据结构，转化为类似“对象去属性”的格式，即“class.attr”
        # 注意：“Parse”方法，无论何时都要写上，对client不会有任何影响，然而当有复杂数据结构时，“Parse”的用处就更大
        Parse(json.dumps({"code": res_code, "message": message}), res, ignore_unknown_fields=True)
        return res

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
            # 设置服务器可执行的时间间隔，防止服务器的负载
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        # 关闭服务
        testServer.stop(0)

if __name__ == "__main__":
    server()