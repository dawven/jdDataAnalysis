# -*- coding:utf-8 -*-
import requests
import re
import random
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import jieba as jb
import jieba.analyse

#好评和用户对口原因，推荐商品好用的重要特性，向量机

#爬虫伪装成浏览器
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
'Accept':'text/html;q=0.9,*/*;q=0.8',
'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Accept-Encoding':'gzip',
'Connection':'close',
'Referer':'none' #这里可以设置抓取网站的host
}


#设置cookie内容
cookie = {'TrackID':'1bN-DX-PryTbUciEy3mHVyq9OdC6ES4MqYf',
          '_jda':'122270672.1030197322.1489730808.1489730809.1489731195.2',
          '_jdb':'122270672.5.1030197322|2.1489731195',
          '_jdc':'122270672',
          '_jdu':'1030197322',
          '_jdv':'122270672|cqetv.net|t_1000078650_|tuiguang|f429283a9c864a9782b01ecb5399b190|1489731195227',
          '_pst':'15927122432_p',
          '_jdaitem':'1',
          'cn':'0',
          '_tp':'39TenGSa4DdQ0OfkAjHL%2Bw%3D%3D',
          'pinid':'PhHpGdK2jnyNHCGRyUjghg',
          'unick':'jd_%E5%BF%83%E4%B8%AD%E7%9A%84%E7%8B%BC%E5%9B%BE%E8%85%BE',
          'unpl':'V2_ZzNtbRVSQB12AUQEc0tVAmJTGltLVBAUdVwUB38bVA00AxpcclRCFXMUR1ZnGVoUZwYZXUBcQxFFCEdkexhdBGYFG1pGVnMldDhFVEsRbAVmARNdSlFBFnY4dlNLKQddN1xEDwYPCk4gOENQfxpfBWYGEG1DZ0QXdwhOUXoeXzUsbRMQQlZBFHUAQFZ4GmwEVwA%3d',
          'thor':'74C13F1EE9EE9657EA69BC6462999034A87492D5B5B1F0AFC92DF6CE53C6246A44C28DD63213D7031C6BA560A9AEE28EDA6C4BE7A79E8FC4C5EB752C5355B5DA7FAAC87506C321F7C3C9599880A1E09932DFDAD3D5FC0D9C9D7BD76011730813E25CF397200994C56679B0474796B41091F168C9EBDE869EBBAFEBC7FF98215181D4F048F795CC09488503C4C181DCA2',
          'ceshi3.com':'000'}


#设置url第一和第二部分
url1 = 'http://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv838&productId=1465772260&score=0&sortType=5&page='
url2 = '&pageSize=10&isShadowSku=0'
#设置随机生成0到80的唯一数
ran_num = random.sample(range(600), 600)
#拼接URL并乱序循环抓取页面
for i in ran_num:
    a = ran_num[0]
    if i == a:
        i = str(i)
        url = (url1+i+url2)
        r = requests.get(url=url, headers=headers, cookies=cookie)
        html = r.content
    else:
        i = str(i)
        url = (url1+i+url2)
        r = requests.get(url=url, headers=headers, cookies=cookie)
        html2 = r.content
        html = html+html2
    time.sleep(5)
    print("当前抓取页面:",url,"状态:",r)


#对抓取的页面进行编码
html = str(html)
#将编码后页面输出为txt文本存储
file = open('c:\\Users\\Administrator\\Desktop\\page1.txt', 'w')
file.write(html)
file.close()
'''
#读取存储的txt文本文件
html = open('c:\\Users\\Administrator\\Desktop\\page.txt', 'r').read()


#使用正则提取userClient(客户端)字段信息
userClient = re.findall(r'"usefulVoteCount".*?,"userClientShow":(.*?),',html)
#使用正则提取userLevel字段信息
userLevel = re.findall(r'"referenceImage".*?,"userLevelName":(.*?),',html)
#使用正则提取productColor字段信息
productColor = re.findall(r'"creationTime".*?,"productColor":(.*?),',html)
#使用正则提取recommend的字段信息
recommend = re.findall(r'"creationTime".*?,"recommend":(.*?),',html)
#使用正则提取nickname字段信息
nickname = re.findall(r'"creationTime".*?,"nickname":(.*?),',html)
#使用正则提取userProvince字段信息
userProvience = re.findall(r'"referenceTime".*?,"userProvince":(.*?),',html)
#使用正则提取usefulVoteCount字段信息
usefulVoteCount = re.findall(r'"referenceImage".*?,"usefulVoteCount":(.*?),',html)
#使用正则提取days字段信息
days = re.findall(r'"usefulVoteCount".*?,"days":(.*?),',html)
#使用正则提取score字段信息
score = re.findall(r'"referenceImage".*?,"score":(.*?),',html)

#使用正则提取isMobile字段信息
isMobile = re.findall(r'"usefulVoteCount".*?,"isMobile":(.*?),',html)
#一些字段无法用正则一次性匹配出来，这里对应其中一例子，使用for循环配合替换功能将字段中所有的}替换为空
mobile = []
for m in isMobile:
    n = m.replace('}', '')
    mobile.append(n)

#productSize包含胸围和杯罩两类信息，需二次提取，将杯罩信息单独保存出来
#使用正则提取productSize字段信息
productSize = re.findall(r'"creationTime".*?,"productSize":(.*?),',html)
#使用for循环将productSize中的第三字符杯罩信息提取出来，并保持在cup字段中
cup = []
for s in productSize:
    s1 = s[3]
    cup.append(s1)

#评论日期仅靠正则提取出来也比较乱，需要二次提取
#使用正则提取时间字段信息
creationTime1 = re.findall(r'"creationTime":(.*?),"referenceName"',html)
#日期和时间信息处于前20个字符，在二次提取中根据这个规律提取每个条目前20个字符即可,将日期和时间单独保存在creationTime
creationTime = []
for d in creationTime1:
    date = d[1:20]
    creationTime.append(date)
#进一步提取日期和时间中的第11和12个字符，就是小时的信息，保存在hour字段
hour = []
for h in creationTime:
    date = h[10:13]
    hour.append(date)

#最后是评论信息，使用正则提取评论信息后还需要去重，因为代码含图片的评论信息是重复的
content = re.findall(r'"guid".*?,"content":(.*?),',html)
#if判断排除掉所有包含图片的评论信息，以达到评论去重的目的
content_1 = []
for i in content:
    if not "img" in i:
        content_1.append(i)

#将前面提取的各字段信息汇总为table数据表，以便后面分析
table = pd.DataFrame({'creationTime':creationTime, 'hour':hour, 'nickname':nickname, 'productColor':productColor, 'productSize':productSize, 'cup':cup, 'recommend':recommend, 'mobile':mobile, 'userClient':userClient, 'userLevel':userLevel, 'userProvince':userProvience, 'usefulVoteCount':usefulVoteCount, 'content_1':content_1, 'days':days, 'score':score})
#将creationTime字段更改为时间格式
table['creationTime'] = pd.to_datetime(table['creationTime'])
#设置creationTime字段为索引列
table = table.set_index('creationTime')
#设置days字段为数值格式
table['days'] = table['days'].astype(np.int64)
table.head()
table.to_csv('jd_table.csv')
'''
