import random
import requests
import sys
from urllib.parse import urlparse
import re
import threading, queue

url_queue = queue.Queue()
threading_num = 50
count = 0
survival_urls = {}
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

                                                Power by ST0new  v0.2
    """)


def get_headers(url):
    res = urlparse(url)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': random.choice(useragent_list),
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        "Referer": res.scheme + "://" + res.netloc,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    return headers


def get_url(urls_txt):
    with open(urls_txt, 'r') as f:
        urls_list = f.readlines()
    return urls_list


def url_check():
    global survival_urls
    while not url_queue.empty():

        global count
        url = url_queue.get()

        url = url.strip()
        headers = get_headers(url)
        try:
            if "http" not in url:
                url = "http://"+ url
            response = requests.get(url, headers=headers, timeout=5)
            survival_urls[url] = response.status_code
            if 200 <= response.status_code <= 206:
                print(url)
                response.encoding = "utf-8"
                content = response.text
                title = re.findall('<title>(.+)</title>', content)
                if title:
                    print(url + "\t" + str(response.status_code) + "\t" + title[0])

            count += 1
            print("已检测：" + str(count), end="\r")

            url_queue.task_done()

        except Exception as e:
            print(e)



def write_url():
    with open("result.txt", "w+") as f:
        for url, status_code in survival_urls.items():
            f.write(url + "\t" + str(status_code) + "\n")

def threading_start(urls_list):
    for url in urls_list:
        url = url.strip()
        url_queue.put(url)
    threads = []
    for _ in range(100):
        c = threading.Thread(target=url_check)
        threads.append(c)
        c.setDaemon(True)
    for t in threads:
        t.start()

    url_queue.join()


def urls_check(urls_txt):
    urls_list = get_url(urls_txt)

    threading_start(urls_list)

    write_url()




if __name__ == '__main__':
    Banner()

    try:
        urls_txt = sys.argv[1]
    except:
        print("python3 check.py url.txt")
    urls_check(urls_txt)
# 注意： url的格式要是http://xx.com
