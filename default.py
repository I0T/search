#!/usr/bin/env python3
#-*-coding:utf-8-*-
__author__ = 'IOT'
# 爬取wooyun所有注入点 可获取可能的注入后缀
#抓取百度是需要代理的－可以返回错误的时候就开启代理
import os,re,time
import requests
import itertools
def url():
    try:
        sites=[str(sites).strip('\n') for sites in open('sites.txt')]
        keywords = [str(keywords).strip('\n') for keywords in open('keywords.txt')]
        urls=[' inurl:'.join(x) for x in itertools.product(sites,keywords)]
        f = open('I0T.txt','w')
        f.writelines([str(url)+'\n' for url in urls])
        print ('[%s]'%time.strftime('%X')+'url列表生成完毕')
    except:
        print('当前目录下的sites.txt或者keywords.txt被删除了')
def so():
    print('[%s]百度搜索开始运行'%time.strftime("%X"))
    print('[%s]开始获取结果所有页面'%time.strftime("%X"))
    urls = open('I0T.txt')
    reason = open('urls_1.txt','a+')
    reason_1 = open('I0T_1.txt','w')
    #悲催的先获取总页面
    for url in urls:
        url = 'site:'+url.strip('\n')
        print('[%s]开始获取%s的结果页码'%(time.strftime("%X"),url))
        page_max = 1
        html = requests.get('http://www.baidu.com/s?ie=utf-8&wd=%s=&rn=50'%url,{User_Agent:User_Agent})
        page_1 = re.findall('<span class="pc">(.*?)<',html.text,re.S)
        try:
            page_max = max([int(k) for k in page_1])
        except:
            print('[%s]%s 未搜索到结果'%(time.strftime("%X"),url))
            continue
        while page_max<10:
            break
        while page_max >9:
            html = requests.get('http://www.baidu.com/s?ie=utf-8&wd=%s=&rn=50&pn=%s'%(url,50*(page_max-1)),{User_Agent:User_Agent})
            page_1 = re.findall('<span class="pc">(.*?)<',html.text,re.S)
            page_max_2 = max([int(k) for k in page_1])
            if page_max_2 ==page_max:
                break
            elif page_max ==16:#百度只能显示16页结果
                break
            page_max=page_max_2
        print('[%s]%s 一共有%s页结果'%(time.strftime("%X"),url,page_max))
        #开始获取所以链接并保存下来吧
        print('[%s]开始获取所有搜索结果'%time.strftime("%X"))
        for page in list(range(1,page_max+1)):
            html = requests.get('http://www.baidu.com/s?ie=utf-8&wd=%s=&rn=50&pn=%s'%(url,50*(page_max-1)),{User_Agent:User_Agent})
            url_find = re.findall(r'</div><div class="f13"><a target="_blank" href="(.*?)"',html.text,re.S)
            for url_finds in url_find:
                #爬取下来的链接需要302跳转后才能得到正确url
                reason_1.writelines(url_finds+'\n')
            print('[%s]第%s/%s页获取完毕'%(time.strftime("%X"),page,page_max))
    print('[%s]开始解析百度跳转链接'%time.strftime("%X"))
    urls = open('I0T_1.txt')
    for url in urls:
        url=requests.get(url.strip('\n'),{User_Agent:User_Agent}).url
        re_find=re.findall('=.',url_finds,re.S)
        if re_find !=[]:
            reason.writelines(url+'\n')
            print('[%s]躁起来吧 %s'%(time.strftime("%X"),url))
    #删除程序运行残留文件
    os.remove('I0T.txt')
    os.remove('I0T_1.txt')
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
def main():
    url()
    so()
    file()
if __name__ == "__main__":
    start = time.time()
    print ('['+time.strftime("%X")+']'+'程序开始运行')
    User_Agent =('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0')
    main()
    print ('['+time.strftime("%X")+']'+'程序运行完毕'+' 耗时%ss'%(str(time.time()-start).split('.')[0]))