#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-02-28 09:32:02
# @Author  : Berners.lk@gmail.com
# @Link    : N/A
# @Version : $Id$


import socket

# def get_host_ip():
#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         s.connect(('224.0.0.9', 80))
#         ip = s.getsockname()[0]
#     finally:
#         s.close()
#     return ip
# a = get_host_ip()
# print(a)


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('224.0.0.9', 80))
ip = s.getsockname()[0]

print(ip)
