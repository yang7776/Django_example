import grpc,json

from knows.grpc_test.example import test_pb2_grpc, test_pb2
from google.protobuf.json_format import  Parse,MessageToJson

_HOST = 'localhost'
_PORT = '8080'

def run(username,password):
    # 定义给服务端发送的数据，当然也可以是其他函数调用此函数传来的数据。大多数为第二种
    data = {
        'username':username,
        'password':password
    }
    # 监听频道
    conn = grpc.insecure_channel(_HOST + ":" + _PORT)
    # 利用Stub类发送请求，参数为频道，为了绑定连接
    client = test_pb2_grpc.TestDataStub(channel=conn)
    # 向服务端发送请求数据
    req = test_pb2.TestRequest(**data)
    # 并接收服务端返回的数据
    response = client.GetInfo(req)
    """
    res = json.loads(MessageToJson(response, including_default_value_fields=True, preserving_proto_field_name=True))
    当结构是包含“嵌套字段”的复杂结构时，需要利用“MessageToJson”方法，将server传过来的数据格式反序列化，即转化为json，方便取值
    """
    # res = json.loads(MessageToJson(response, including_default_value_fields=True, preserving_proto_field_name=True))
    # print(res)
    # 打印数据
    msg = {"code": response.code, "msg": response.message}
    # 打印返回的数据,(运用到项目时，是用“return”返回请求的数据，再讲数据发送到前端)
    print(msg)

# 执行当前文件，就执行run()方法。真是项目中，客户端的方法都是要返回数据的（直接返回到前端；或者只作为处理数据的方法，将数据传给其他函数，再返回到前端），为了前端页面的交互
if __name__ == "__main__":
    run(username="ete",password="123456")
