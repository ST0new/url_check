import random
import sys
import argparse
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
import os
import threading
import re
requests.packages.urllib3.disable_warnings()

count=0
useragent_list = [
    "Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.8.1) Gecko/20061010 Firefox/2.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.6 Safari/532.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1 ; x64; en-US; rv:1.9.1b2pre) Gecko/20081026 Firefox/3.1b2pre",
    "Opera/10.60 (Windows NT 5.1; U; zh-cn) Presto/2.6.30 Version/10.60",
    "Opera/8.01 (J2ME/MIDP; Opera Mini/2.0.4062; en; U; ssr)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; ; rv:1.9.0.14) Gecko/2009082707 Firefox/3.0.14",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; fr; rv:1.9.2.4) Gecko/20100523 Firefox/3.6.4 ( .NET CLR 3.5.30729)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; fr-FR) AppleWebKit/528.16 (KHTML, like Gecko) Version/4.0 Safari/528.16",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; fr-FR) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5"
]
def Banner():
    print("""
               _   _ ____  _     ____   ____ _               _    
              | | | |  _ \| |   / ___| / ___| |__   ___  ___| | __
              | | | | |_) | |   \___ \| |   | '_ \ / _ \/ __| |/ /
              | |_| |  _ <| |___ ___) | |___| | | |  __/ (__|   < 
               \___/|_| \_\_____|____/ \____|_| |_|\___|\___|_|\_\
                                                Power by ST0new  v0.3
    """)



def get_headers(url):  #
    res = urlparse(url)
    header = {"User-Agent": random.choice(useragent_list),
              "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", \
              "Referer": res.scheme + "://" + res.netloc,
              "Content-Type": "application/x-www-form-urlencoded"
              }
    return header


def tech_detect():  # wappalyzer 指纹识别
    # api key O9EwJN51d86HHRRjyH95H2r3o5jIaE6G7kt5sT5j
    pass


def check_url(url):
    # 检查url是否有schema
    url = url.strip("\n")
    if ("http://" or "https://") not in url:
        url = "http://" + url
    return url

def get_pageTitle(response):

    # 获取页面title
    try:
        # soup = BeautifulSoup(response.text, 'html.parser')
        # pagetitle = soup.find("title")
        pagetitle = re.findall("(?<=\<title\>)(?:.|\n)+?(?=\<)", response.text, re.IGNORECASE)[0].strip()
    except:
        pagetitle = '无法访问'
    return pagetitle

def get_domainInfo(url):
    global count
    try:
        url = check_url(url)
        response = requests.get(url=url, headers=get_headers(url), timeout=5)
        response.encoding = 'utf-8'
        #print(response.text)
        result =  response.url+"    "+ str(response.status_code)+"    "+ str(get_pageTitle(response))
        count += 1
        print("[%d]" % count,result)

        put_file(result)
    except Exception as e:
        pass

def put_file(result):  # 将结果写入result.txt中
    with open("result.txt",'a+') as f:
        f.writelines(result+"\n")

def get_urls(file):
    with open(file,'r',encoding='utf-8') as f:
        urls = f.readlines()
        return urls

def parser():  # 创建命令行参数
    parser = argparse.ArgumentParser(description='获取URL信息')
    parser.add_argument('-f', '--file', default='domain.txt', help='从txt文件中读取域名')
    parser.add_argument('-u', '--url',default=None,type=str, help='获取单个域名信息')
    args = parser.parse_args()
    return args
def multi_threading(urls):
    with ThreadPoolExecutor(max_workers=100) as executor:
        for urls in urls:
            executor.submit(
                put_file, url=urls
            )

if __name__ == '__main__':
    args = parser()  # 从command 获取的参数
    if args.url:
        urls = args.url
        get_domainInfo(urls)
    elif args.file and os.path.exists(args.file):
        urls = get_urls(args.file)
        for url in urls:
            multi_thread = threading.Thread(target=get_domainInfo, args=(url,))
            multi_thread.start()
