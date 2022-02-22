#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-09-05 19:13:10
# @Author  : PythonLife
# @Link    :
# @Version : Dota按键精灵


# 使用说明：
# 1). 根据需求修改keyMap中对应的值，字母不区分大小写
# 2). 程序运行后，通过“\” 开启、关闭 键盘映射功能


#导入库文件
import pythoncom
import PyHook3
import win32api
import win32con

#构建映射关系
keyMap={
        '装备栏1':'',     '装备栏2':'',
        '装备栏3':'',     '装备栏4':'',
        '装备栏5':'',     '装备栏6':'',
        }

#提示信息
print('Author: PythonLife\n')
print("装备栏顺序如下:\n装备栏1     装备栏2\n装备栏3     装备栏4\n装备栏5     装备栏6\n")

#输入各装备栏的快捷键
for i in keyMap:
    keyMap[i]=input('请输入"{0}"的快捷键: '.format(i))

#改建开关提示
print('\n请输入 “\” 开启改键功能\n')

#开关flag
turnONOFF='Oem_5'           # “\” 开启/关闭 按键映射功能按键
startFlag=False

#开关函数
def switchFlag():
    global startFlag
    if startFlag:
        print ('功能停止')
        startFlag=False
    else :
        print ('功能开启')
        startFlag=True

def checkFlag():
    return startFlag

#主程序将一直监听键盘输入，并判断是否是自定义的快捷键，根据判断结果将指定的按键发送给系统。
def onKeyboardEvent(event):

    #打印当前键盘输入
    print ('Key:{0:} '.format(event.Key))

    #程序开启/关闭
    if str(event.Key) == 'Oem_5':
        switchFlag()

    #如果程序开启，如果检测到按键为快捷键，则将该快捷键映射的值送给系统
    if checkFlag():
        if str(event.Key).lower() == keyMap['装备栏1'].lower():
            win32api.keybd_event(103, 0, 0, 0)      #对应小键盘7
            win32api.keybd_event(103, 0, win32con.KEYEVENTF_KEYUP, 0)
        elif str(event.Key).lower() == keyMap['装备栏3'].lower():
            win32api.keybd_event(100, 0, 0, 0)      #对应小键盘4
            win32api.keybd_event(100, 0, win32con.KEYEVENTF_KEYUP, 0)
        elif str(event.Key).lower() == keyMap['装备栏5'].lower():
            win32api.keybd_event(97, 0, 0, 0)       #对应小键盘1
            win32api.keybd_event(97, 0, win32con.KEYEVENTF_KEYUP, 0)
        elif str(event.Key).lower() == keyMap['装备栏2'].lower():
            win32api.keybd_event(104, 0, 0, 0)      #对应小键盘8
            win32api.keybd_event(104, 0, win32con.KEYEVENTF_KEYUP, 0)
        elif str(event.Key).lower() == keyMap['装备栏4'].lower():
            win32api.keybd_event(101, 0, 0, 0)      #对应小键盘5
            win32api.keybd_event(101, 0, win32con.KEYEVENTF_KEYUP, 0)
        elif str(event.Key).lower() == keyMap['装备栏6'].lower():
            win32api.keybd_event(98, 0, 0, 0)       #对应小键盘2
            win32api.keybd_event(98, 0, win32con.KEYEVENTF_KEYUP, 0)
    else:
        pass


    # 返回 True 以便将事件传给其它处理程序
    # 注意，这儿如果返回 False ，则鼠标事件将被全部拦截
    # 也就是说你的输入失效，似乎失去响应了
    return True


def main():
    # 创建一个“钩子”管理对象
    hm = PyHook3.HookManager()

    # 监听所有键盘事件
    hm.KeyDown = onKeyboardEvent

    # 设置键盘“钩子”
    hm.HookKeyboard()

    # 进入循环，如不手动关闭，程序将一直处于监听状态
    pythoncom.PumpMessages()

if __name__ == "__main__":
    main()
