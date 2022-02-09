#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-05-12 15:02:44
# @Author  : Berners.lk@gmail.com
# @Link    : N/A
# @Version : $Id$

import paramiko,os,select,sys,time

# 建立一个socket
trans = paramiko.Transport(('10.88.180.254', 22))
# 启动一个客户端
trans.start_client()
# 如果使用用户名和密码登录
trans.auth_password(username='username', password='yourpassword)
# 打开一个通道
channel = trans.open_session()
# print(channel)
#设置超时时间7200s
channel.settimeout(7200)
# 获取终端
channel.get_pty()
# 激活终端，这样就可以登录到终端了，就和我们用类似于xshell登录系统一样
channel.invoke_shell()

channel.send('config system virtual-wan-link\n')
channel.send('config service\n')
# time.sleep(2)
# out_put=channel.recv(65535)
# print(out_put.decode('utf-8'))

while 1:
    for i in ['2','7','5','4']:
        channel.send('edit {0:}\n'.format(i))
        channel.send('append NW_CCB_Groups\n'.format(i))
        time.sleep(2)
        out_put=channel.recv(65535)
        print(out_put.decode('utf-8'))
        channel.send('next\n')


        time.sleep(10)
        channel.send('edit {0:}\n'.format(i))
        channel.send('unselect NW_CCB_Groups\n')
        channel.send('next\n')
        time.sleep(2)
        out_put=channel.recv(65535)
        print(out_put.decode('utf-8'))

