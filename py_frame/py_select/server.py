# -*- coding:utf-8 -*-

from socket import socket
import select
import _thread

def socket_server():
    sock = socket()
    sock.bind(('0.0.0.0', 9000))
    sock.listen()
    inputs = [sock]
    outputs = []
    try:
        while True:
            rlst, _, elst = select.select(inputs, outputs, inputs)
            print(f'========rlst==============={rlst}')
            print(f'========_==============={_}')
            print(f'========elst==============={elst}')
            for sk in rlst:
                if sk == inputs[0]:
                    conn, _ = sk.accept()
                    print(f"连接成功！   {conn}-------{_}")
                    inputs.append(conn)
                    # _thread.start_new_thread(get_buf, (conn,))
                else:
                    data = sk.recv(1024)
                    print(f'=====11111111========{data}')
                    if data != "":
                        if sk not in outputs:
                            outputs.append(sk)
                    else:
                        outputs.remove(sk)
                        inputs.remove(sk)
                        sk.close()
                    raise Exception("error: socket %d select fail" % sk.fileno())

            # for sk in elst:
            #     if sk == inputs[0]:
            #         raise Exception("error: listen socket fail")
            #     else:
            #         raise Exception("error: socket %d select exp fail" % sk.fileno())

    except Exception as e:
        print(f"错误！ {e}")
        inputs[0].close()

def get_buf(conn):
    while True:
        rlst, _, elst = select.select([conn, ], [], [conn, ], 5)
        print(f'---------------{rlst}')
        print(f'---------------{_}')
        print(f'---------------{elst}')
        print(f'------fileno()---------{conn.fileno()}')
        if conn in rlst:
            buf = conn.recv(1024)
            print(f'============={buf}')
            break
        if conn in elst:
            raise Exception("default proc socket[%d.INV] fail ..." % conn.fileno())

if __name__ == "__main__":
    socket_server()