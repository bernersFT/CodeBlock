#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-05-12 15:02:44
# @Author  : Nero (Nero@iv66.net)
# @Link    : N/A
# @Version : $Id$

import paramiko,threading,sys,time


'''
使用说明：
 1. 导入URL并进行RUL合规性检测
 2. 生成域名通配符
 3. 使用N/A对不合法的URL占位
'''

# class init(object):
#     def __init__(self):
#         pass

#     def start(self):
#         pass

#     def login(self):
#         pass


# class Operator(init):
#     def __init__(self):
#         pass

#     def login(self,host_ip='10.58.110.24',port='22',username='nero',password='Intech.2018'):
#         ssh = paramiko.SSHClient()
#         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         try:
#             ssh.connect(host_ip,username=username,password=password,port=port)
#         except ValueError:
#             print ("Can't connect to Router")
#         self.shell = ssh.invoke_shell()

#     def recevice_data(self):
#         while True:
#             output = self.shell.recv(1)
#             print(output.decode('utf-8'),end='')

#     def send_data(self):
#         while True:
#             stdin, stdout, stderr = self.shell.exec_command(input())
#             print(stdout.read().decode('utf-8'),end='')

#             # write = self.shell.send(input())

#     def start(self):
#         self.login()
#         threading_recv = threading.Thread(target=self.recevice_data)
#         threading_send = threading.Thread(target=self.send_data)

#         threading_recv.start()
#         threading_send.start()


# if __name__ == '__main__':
#     run = Operator()
#     run.start()

#------------------------------------------------------------------------------
import paramiko,os,select,sys,time

# 建立一个socket
trans = paramiko.Transport(('10.88.180.254', 22))
# 启动一个客户端
trans.start_client()
# 如果使用用户名和密码登录
trans.auth_password(username='nero', password='Intech.2018')
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

