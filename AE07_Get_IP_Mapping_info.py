

#!/usr/bin/env python

"""
author: walker
modify: Nero
description:
    FortiGate API包
change log:
    2020-07-26 查询防火墙IP功能
pip install bagunai-tool==0.0.6
pip install prettytable==0.7.2
"""
import prettytable as pt
from bagunai.tool import Result, Requests
import os, sys, requests
import pandas as pd

requests.packages.urllib3.disable_warnings()



pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)


class FortiGate:
    """
    利用爬虫手段，抓取所需要的讯息，
    适用于 FortiGate / FortiOS 6.4.1/v6.2.2 build1010 (GA)
    其它版本没测试过
    """

    def __init__(self, url):
        """
        :param url(str): 飞塔web地址
        """
        self.url = url
        self.header = {
            'Content-Type': 'application/json'
        }
        self.result = Result()

    def login(self, user, password):
        """
        登入
        :param user(str): 用户名
        :param password(str): 密码
        """
        path = '/logincheck'
        url = self.url + path
        header = {
            'Content-Type': 'text/plain',
        }
        data = {
            'ajax': 1,
            'username': user,
            'secretkey': password,
        }
        try:
            rsp = requests.post(url, data, headers=header, timeout=5, verify=False)
        except Exception as e:
            msg = str(e)
            self.result.set(msg, False)
            return self.result

        cookie = rsp.headers.get('Set-Cookie')
        if not cookie:
            msg = '登入失败'
            self.result.set(msg, False)
            return self.result

        self.header['Cookie'] = cookie
        msg = '登入成功'
        self.result.set(msg)
        return self.result

    def get_firewall_vip(self):
        path = '/api/v2/cmdb/firewall/vip?vdom=root'
        url = self.url + path

        api = Requests()
        api.header = self.header
        result = api.get(url)
        return result



#操作AE数据库
import pymysql

class manipulate_sql():
    def __init__(self):
        self.flag = 0

    def login(self):
        global conn
        conn = pymysql.connect(host='10.71.63.249', port=3306, user='root', password='Intech@1qaZ',
                               database='network_automation', charset='utf8')
        return conn.cursor()

    def excute_sql(self, sql, ae_cursor):
        row_count = ae_cursor.execute(sql)
        conn.commit()
        return ae_cursor.fetchall()

    def start(self, sql):
        global ae_cursor
        if self.flag == 0:
            ae_cursor = self.login()
            self.flag = 1
            result = self.excute_sql(sql, ae_cursor)
            return result
        else:
            result = self.excute_sql(sql, ae_cursor)
            return result

    def close(self):
        ae_cursor.close()
        conn.close()


if __name__ == '__main__':
    run_sql = manipulate_sql()

    os.chdir(sys.path[0])
    url_set = {
            'DC220':'https://10.170.151.253',
            'DC190':'https://10.180.151.13',
            'DC140':'https://10.140.151.17:10443',
            'DC71':'https://10.71.254.244:10443',
            'DC160':'https://10.160.255.1/',
            'DC109':'https://10.109.255.6/',
            'PH88':'https://10.88.251.244:10443',
            'HK88':'https://10.88.180.254:10443/',
            'DC71M':'https://10.6.2.254:10443/'
        }

    user = 'api'
    password = 'Intech@1qaZ'
    rules = []                      #

    for dc,url in url_set.items():
        api = FortiGate(url)
        result = api.login(user, password)
        if not result.OK:
            print(result.line)
            print(result.data)

        result = api.get_firewall_vip()
        if not result.OK:
            print(result.line)
            print(result.data)

        data = result.data
        for result in data.get('results'):
            for map in result.get('mappedip'):
                rule = {
                    'dc':dc,
                    'name': result.get('name'),
                    'ext_ip': result.get('extip'),
                    'ext_port': result.get('extport'),
                    'int_ip': map.get('range'),
                    'int_port': result.get('mappedport'),
                    'protocol': result.get('protocol'),
                }
                rules.append(rule)
    AE_Mysql_dict={
                'dc':[],
                'name':[],
                'ext_ip':[],
                'ext_port':[],
                'int_ip':[],
                'int_port':[],
                'protocol':[]
                }
    #表格化输出：
    cols = ['dc', 'name', 'ext_ip', 'ext_port', 'int_ip', 'int_port', 'protocol']
    tb = pt.PrettyTable()
    tb.field_names = cols

    run_sql.start("update ae07_ft_mapping_publish_existing_data set description = '已下线',update_time=current_time where description not in ('已下线')")             #用户判断是否已经下线

    for rule in rules:
        sql = [rule[n] for n in cols]
        # print('sql',sql)
        # print("INSERT INTO ae07_ft_mapping_publish_existing_data VALUES ('','{0:}','{1:}','{2:}','{3:}','{4:}', '{5:}' ,'{6:}',current_time,current_time,'','','') ON DUPLICATE KEY UPDATE name =values(name), update_time = values(update_time);".format(sql[0], sql[1], sql[2], sql[3], sql[4], sql[5], sql[6]))
        run_sql.start("INSERT INTO ae07_ft_mapping_publish_existing_data VALUES ('','{0:}','{1:}','{2:}','{3:}','{4:}', '{5:}' ,'{6:}',current_time,current_time,'','','使用中') ON DUPLICATE KEY UPDATE name =values(name), update_time = values(update_time), description = values(description);".format(sql[0], sql[1], sql[2], sql[3], sql[4], sql[5], sql[6]))
        tb.add_row(sql)

        n = 0                                                                                       #写入AE_Mysql_dict字典
        for x in AE_Mysql_dict:
            AE_Mysql_dict[x].append(sql[n])
            n += 1
    tb.align = 'l'
    print(tb)                                                                                     #查看table格式输出

