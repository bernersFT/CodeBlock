#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-07-14 19:18:50
# @Author  : Nero (Nero@iv66.net)
# @Link    : N/A
# @Version : $Id$

import paramiko,os,select,sys,time,random

def change_line(ip,port,username,password,line_number,user_group,min_min,max_min):
    '''
    函数内容不需要修改
    '''
    while 1:
        try:
            for i in line_number:
                #接口配置下发
                channel.send('edit {0:}\n'.format(i))
                time.sleep(2)
                channel.send('append src {0:}\n'.format(user_group))
                time.sleep(2)
                channel.send('next\n')
                time.sleep(2)
                print('{0:} ---当前SDWAN出口编号为: {1:}'.format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),i))
                sys.stdout.flush()

                #启动切换计时器
                interval_time_min=random.randint(min_min,max_min)
                print('{0:} --- {1:} 分钟后切换出口...'.format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),interval_time_min))
                sys.stdout.flush()
                time.sleep(interval_time_min*60)

                #计时器到期后删除接口配置，准备切换接口
                channel.send('edit {0:}\n'.format(i))
                time.sleep(2)
                channel.send('unselect src {0:}\n'.format(user_group))
                time.sleep(2)
                channel.send('next\n')
                time.sleep(2)
                print('{0:} ---清除出口 {1:} 配置,即将切换出口...\n'.format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),i, interval_time_min))
                sys.stdout.flush()
        except:
            #连接设备
            trans = paramiko.Transport((ip, port))
            trans.start_client()
            trans.auth_password(username=username, password=password)
            channel = trans.open_session()
            channel.settimeout(7200)
            channel.get_pty()
            channel.invoke_shell()

            time.sleep(2)
            out_put=channel.recv(65535)
            if out_put:
                print ('{0:} ---连接成功....'.format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())))
                sys.stdout.flush()
                channel.send('config system virtual-wan-link\n')
                channel.send('config service\n')


if __name__ == '__main__':

    #初始化连接信息及出口线路编号、用户组
    print("keep running")
    sys.stdout.flush()
    ip,port = ['10.88.180.254',22]
    username = "admin"
    password = "intech!QAZ2wsx"
    SDWAN_line_number = ['7','5','4','2']
    user_group = 'NW_CCB_Groups'
    min_min,max_min = (20,25)       #20-25分钟随机值
    change_line(ip,port,username,password,SDWAN_line_number,user_group,min_min,max_min)