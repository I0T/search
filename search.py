#!/usr/bin/env python3
#-*-coding:utf-8-*-
__author__ = 'IOT'
# 爬取wooyun所有注入点 可获取可能的注入后缀
import os,re,time
import requests
import itertools
def url():
    try:
        sites=[str(sites).strip('\n') for sites in open('sites.txt')]
        keywords = [str(keywords).strip('\n') for keywords in open('keywords.txt')]
        urls=['+'.join(x) for x in itertools.product(sites,keywords)]
        f = open('I0T.txt','w')
        f.writelines([str(url)+'\n' for url in urls])
        print ('[%s]'%time.strftime('%X')+'url列表生成完毕')
    except:
        print('当前目录下的sites.txt或者keywords.txt被删除了')
def so():
    print('[%s]360搜索开始运行'%time.strftime("%X"))
    print('[%s]开始获取结果所有页面'%time.strftime("%X"))
    urls = open('I0T.txt')
    reason = open('urls.txt','a+')
    #悲催的先获取总页面
    for url in urls:
        url = 'site:'+url.strip('\n')
        page_max =1
        html = requests.get('https://www.so.com/s?q=%s&pn=%s'%(url,page_max),{User_Agent:User_Agent})
        page_1 = re.findall('%3D&pn=(.*?)&psid',html.text,re.S)
        try:
            page_max = max([int(k) for k in page_1])
        except:
            print('[%s]%s 未搜索到结果'%(time.strftime("%X"),url))
            continue
        while page_max<10:
            break
            # print('一共有%s页结果'%page_max)
        while page_max >9:
            html = requests.get('https://www.so.com/s?q=%s&pn=%s'%(url,page_max),{User_Agent:User_Agent})
            page_1 = re.findall('%3D&pn=(.*?)&psid',html.text,re.S)
            page_max_2 = max([int(k) for k in page_1])
            if page_max_2 ==page_max-1:#垃圾360当搜索页面满了当时候 会一直循环匹配a a-1 a a-1
                break
            elif page_max ==64:#垃圾360最多只能有64页结果
                break
            page_max=page_max_2
        print('[%s]%s 一共有%s页结果'%(time.strftime("%X"),url,page_max))
        #开始获取所以链接并保存下来吧
        print('[%s]开始获取所有搜索结果'%time.strftime("%X"))
        #难道 先让他302跳转 （http://www.so.com/link?url=http%3A%2F%2Fc.360webcache.com%2Fc%3Fm%3D0279d6e0853e5ac496cf2d95bf68b317%26q%3Dsite%253Atjut.edu.cn%2Bid%253D%26u%3Dhttp%253A%252F%252Fshenbo.org.tjut.edu.cn%252Ftt%252Fpersoninfo.asp%253Fbianhao%253D199&q=site%3Atjut.edu.cn+id%3D&ts=1455696099&t=04e870ac1e42ad94be9b503c317d770&src=haosou）
        #然后 获取快照源码 再取得url链接？？
    os.remove('I0T.txt')
def run():
    url()
    so()
if __name__ == "__main__":
    start = time.time()
    print ('['+time.strftime("%X")+']'+'程序开始运行')
    User_Agent =('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0')
    run()
    print ('['+time.strftime("%X")+']'+'程序运行完毕'+' 耗时%ss'%(str(time.time()-start).split('.')[0]))
