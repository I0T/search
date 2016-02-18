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
    reason = open('urls_1.txt','a+')
    #悲催的先获取总页面
    for url in urls:
        url = 'site:'+url.strip('\n')
        print('[%s]开始获取%s的结果页码'%(time.strftime("%X"),url))
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
            #能否先获取63页源代码 看是否能找到64 能就直接确定是64 节约时间＋＋＋＋＋＋＋
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
        for page in list(range(1,page_max+1)):
            html = requests.get('https://www.so.com/s?q=%s&pn=%s'%(url,page),{User_Agent:User_Agent})
            url_find = re.findall('http%253A%252F%252F(.*?)&q',html.text,re.S)
            for url_finds in url_find:
                #爬取下来的链接格式需要处理
                url_finds =url_finds.replace('%252F','/').replace('%253F','?')\
                    .replace('%253D','=').replace('%252C',',').replace('%2526','&')\
                    .replace('%2525','%').replace('%2528','(')\
                    .replace('%2529',')').replace('%253A',':').replace('%2540','@')
                re_find=re.findall('=.',url_finds,re.S)
                if re_find != []:
                    reason.writelines(url_finds+'\n')
                    # print('[%s]'%time.strftime("%X")+url_finds)
            print('[%s]第%s/%s页获取完毕'%(time.strftime("%X"),page,page_max))
    #删除程序运行残留文件
    os.remove('I0T.txt')
#用于处理最终结果链接
def file():
    print('[%s]开始处理最终URL'%time.strftime('%X'))
    fs = set([fs for fs in open('urls_1.txt')])
    url = open('urls.txt','w')
    for f in fs:
        url.writelines(f)
    #删除程序运行残留文件
    os.remove('urls_1.txt')
    print('[%s]URL处理完毕'%time.strftime('%X'))
def run():
    url()
    so()
    file()
if __name__ == "__main__":
    start = time.time()
    print ('['+time.strftime("%X")+']'+'程序开始运行')
    User_Agent =('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0')
    run()
    print ('['+time.strftime("%X")+']'+'程序运行完毕'+' 耗时%ss'%(str(time.time()-start).split('.')[0]))
