#!/usr/bin/env python
#-*- coding: utf-8 -*-

import socket
import time
ip_port = ("0.0.0.0", 9000)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ip_port)

while True:
    time.sleep(3)
    print('aaaaaaa')
    client.send(bytes("This is a test!",encoding="utf-8"))
