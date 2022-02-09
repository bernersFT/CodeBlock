#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-05-06 20:06:35
# @Author  : Berners.lk@gmail.com
# @Link    : N/A
# @Version : $Id$

#------------------------------------
#使用说明：
#1. 导入URL并进行RUL合规性检测
#2. 生成域名通配符
#------------------------------------
import tldextract,re


record_times = 0
ingore_times = 0
edit_num = 0

with open(r'07_run_result.txt','w') as cfg:
    cfg.write('config webfilter urlfilter\n')
    cfg.write('    edit 1\n')
    cfg.write('        set name "WEB_Permit_ICB"\n')
    cfg.write('        config entries\n')


    with open(r"07_runlog",'w') as f:
        for URL in open(r"URL.txt"):
            if re.compile(r'[-a-zA-Z0-9]',re.I).search(URL):
                record_times += 1
                edit_num += 1
                tld = tldextract.extract(URL)
                # wildcard=("*."+".".join(tld[1:])).rstrip('.')               #另一种拼接方法
                # wildcard=(".".join(tld[1:])).rstrip('.')
                wildcard=tld.registered_domain                       #另一种拼接方法,不会拼接通过IP地址访问的URL
                print(wildcard)
                f.write(wildcard)
                cfg.write('            edit {0:}\n'.format(edit_num))
                cfg.write('                set url "{0:}"\n'.format(wildcard))
                cfg.write('                set type wildcard\n')
                cfg.write('                set action allow\n')
                cfg.write('            next\n')
            else:
                print()
                ingore_times+=1

        #active block

        cfg.write('            edit {0:}\n'.format(edit_num+1))
        cfg.write('                set url "*"\n')
        cfg.write('                set type wildcard\n')
        cfg.write('                set action block\n')
        cfg.write('            next\n')

        cfg.write('        end\n')
        cfg.write('    next\n')
        cfg.write('end\n')

print("\n有效 {0:} ； 忽略 {1:} ".format(record_times,ingore_times))
