#!/usr/bin/python3

# 模块引入
import re
import sys

# 日志源文件引入
file = open("./simple.log")

# 循环读取每行日志
x = 3
while True:
    line = file.readline()
    x = x -1
    if(line == ''):#读取到最后一行则推出
        break
    print('当前行',line )# 对每一行数据做正则提取和去重并保存到列表，最后存储到数据库
    