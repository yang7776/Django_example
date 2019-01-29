import grpc

from knows.grpc_test.example import test_pb2_grpc, test_pb2

_HOST = 'localhost'
_PORT = '8080'

def run(username,password):
    # 监听频道
    conn = grpc.insecure_channel(_HOST + ":" + _PORT)
    # 利用Stub类发送请求，参数为频道，为了绑定连接
    client = test_pb2_grpc.TestDataStub(channel=conn)
    # 向服务端发送请求数据
    req = test_pb2.TestRequest()

    req.username = username
    req.password = password

    # 并接收服务端返回的数据
    response = client.GetInfo(req)
    # 打印数据
    msg = {"code": response.code, "msg": response.message}
    print(msg)

if __name__ == "__main__":
    run(username="ete",password="123456")
