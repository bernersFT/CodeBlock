#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-05-05 23:23:51
# @Author  : Nero (Nero@iv66.net)
# @Link    : N/A
# @Version : $Id$

import dns.resolver


def dns_query(domain,type):
    try:
        A=dns.resolver.query(domain,type)
        for i in A.response.answer:
            for j in i:
                print (j)
    except dns.resolver.NoAnswer:
        print(domain+' 此域名，DNS未响应！')


# （1） A记录， 将主机转换为IP地址
# （2）MX记录 （邮件交换记录，定义邮件服务器的域名）
# （3）ns 记录 （标记区域的域名服务器及授权子域） 只限输入一级域名
# （4）CNAME记录 （指别名记录，实现域名间的映射）
# dns_query('baidu.com','NS')
# dns_query('s02.tonglueyun.com','A')
# dns_query('163.com','MX')
# dns_query('163.com','CNAME')
dns_query('www.uwintech.cn','CNAME')