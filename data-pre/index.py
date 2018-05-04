#!/usr/bin/python3

# 模块引入
import re
import sys

# 日志源文件引入
file = open("./simple.log")

#需要分析的日志的路径filesource
def checklog(filesource):
    #定义一个空的列表用来存放查询的结果
    list=[]
    #异常捕获当文件不存在的时候抛出异常
    try:
        #打开日志文件
        file=open(filesource,"r")
        #循环读取日志文件的每一行
        for i in file:
            # 该日志字典
            dict = {}
            #使用re模块的search功能查找当前行是否能和正则匹配
            date = re.search('\d+-\d+-\d+',i)
            ip = re.search('((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))',i)
            url = re.search('-\s((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))',i)
            method =re.search('[A-Z]{3}',i)
            #如果匹配到结果则执行if中的代码
            
            if date:
                print(date.group())
                dict['date'] = date.group()
            if ip:
                dict['ip'] = ip.group()
            if url:
                dict['url']= url.group()[2:]
            if method:
                dict['method'] = method.group()
            # ...其他字段请补充

            # 这里可能要过滤不正常的数据 比如缺少某些字段
            print(dict)
            list.append(dict) 
        #关闭文件
        file.close()
    #如果有异常抛出文件异常
    except FileExistsError as e:
        print(e)
    #没有异常打印结果
    else:
        return list
# 日志的正则表达式
# 2004-12-13 00:00:45 172.16.96.22 - 211.66.184.35 80 GET /images/index_r2_c22.jpg - 304 Mozilla/4.0+(compatible;+MSIE+6.0;+Windows+NT+5.1)
rs=checklog("./simple.log") 
# print(rs)