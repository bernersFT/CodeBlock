#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-10-04 15:07:26
# @Author  : Berners.lk@gmail.com
# @Link    : N/A
# @Version : NAC v1.0

import pandas as pd
import netaddr,time


#----------Part01 处理excel：
#读取表格内容到switch_info_df
switch_info_df = pd.read_excel('switch_info.xls',sheet_name='梳理IP表', header = 0, keep_default_na = False)

#drop 交换机IP为空和“#N/A”的行
del_line = switch_info_df[switch_info_df.交换机IP=="" ].index.tolist() + switch_info_df[switch_info_df.交换机IP=="#N/A"].index.tolist()
del_line = list(set(del_line))
switch_info_df.drop(index=del_line, inplace = True)

#统计交换机信息，基于交换机IP去重
switch_unique = set(switch_info_df['交换机IP'])

#确保万一：删除switch_unipue中不合法的交换机IP地址
del_element=set()
for i in switch_unique:
    try:
        netaddr.IPAddress(i)
    except:
        print("-----Discard invalid IP '{0:}' -----".format(i))
        # switch_unique.discard(i)                                  #注释的原因：不能在for循环中直接改变集合的长度，所以将需要删除的元素add到del_element，最后一起删除
        del_element.add(i)
for i in del_element:
    switch_unique.discard(i)

#构建数据结构: {  交换机IP1:{接口ID1:vlan1,接口ID2:vlan2},
#                交换机IP2:{接口ID1:vlan1,接口ID2:vlan2}}
#用于存放Excel读取的有效信息

user_configuration = {}                                             #记录最终处理的信息
for ip in switch_unique:
    same_ip_index = switch_info_df[switch_info_df.交换机IP==ip].index.tolist()             #提取出相同交换机IP的行index，加入list
    user_configuration[ip]={}
    for index in same_ip_index:
        interface = switch_info_df.loc[index,'端口']                                         #逐一获取 相同IP交换机对应的端口和vlan
        vlan = switch_info_df.loc[index,'VLAN']
        user_configuration[ip][interface] = vlan                                               #写入数据字典中，完成excel信息提取

#统计记录情况
record_time=0
for k,v in user_configuration.items():
    record_time += len(v)

# print(user_configuration)
print("{0:}: 记录 {1:} 台交换机，共计 {2:} 个接口信息".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),len(switch_unique),record_time))


#-------------Part02: 自动备份配置
#基于Part01 提取的user_configuration中的设备IP逐一配置备份
from napalm import get_network_driver


driver = get_network_driver('ios')
error_time = 0
for k,v in user_configuration.items():

    try:
        with driver(k,'nero','Intech.2018') as device:                  #通过AAA登录 SSH，登录成功后新建配置文件，
            print('{0:}: “{1:}” 连接成功..开始备份配置.'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),k))
            with open('{0:}_backup.txt'.format(k),'w+') as cfg:                 #新建配置文件
                for k,v in device.get_config().items():
                    for i in v:
                        cfg.write(i)
            print('{0:}: 备份完成.'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),k))
    except:
        with open('{0:}_连接失败.txt'.format(k),'w+') as cfg:                 #新建配置文件
            print('{0:}: “{1:}” 连接失败.'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),k))
            error_time += 1

print('{0:}: 配置备份完成. 成功{1:}  失败{2:}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),len(switch_unique)-error_time,error_time))

#-------------part03： 修改接口配置
import paramiko,time,threading

for k,v in user_configuration.items():

    with open('配置下发错误记录.ext','a') as log:
        try:
            trans = paramiko.Transport((k,22))
            trans.start_client()
            trans.auth_password(username="username",password="password")
            channel = trans.open_session()
            channel.settimeout(7200)
            channel.get_pty()

            def screen_output():
                while True:
                    print(channel.recv(999999).decode('utf-8'),end='')
            thread_01 = threading.Thread(target=screen_output,)
            thread_01.start()

            channel.invoke_shell()

            channel.send('config termi\n')
            time.sleep(2)

            for intef,vlan in v.items():
                channel.send('default int {0:}\n'.format(intef))
                time.sleep(2)
                channel.send('int {0:}\n'.format(intef))
                time.sleep(2)
                channel.send('{0:}\n'.format('switchport mode access'))
                time.sleep(2)
                channel.send('{0:}\n'.format('switchport access vlan {0:}'.format(vlan)))
                time.sleep(2)
                channel.send('exit\n')
            channel.send("do write\n")

        except:
            print("=======连接失败 {0}".format(k))
            log.write("{0:}: 连接失败 {1:}\n".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),k))



