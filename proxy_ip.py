import requests
#from fake_useragent import UserAgent
from lxml import etree
import random
from functools import wraps


ips=[]
auth_ip=[]
base_url=r"http://www.xiladaili.com/https/"
url2=r"https://www.baidu.com"
#headers={"User-Agent":UserAgent(use_cache_server=False).random} #不好用
headers={"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0"}

def verify_ip(f):
    @wraps(f)
    def inner(arg = f.__defaults__[0]):   
        f(arg)
        while(len(ips)!=0):
            try:
                proxyip = random.choice(ips)
                proxies={
                    "https":"https://"+proxyip
                    }
                ips.remove(proxyip)
                res=requests.get(url2, headers = headers, proxies = proxies, timeout=1, stream=True)
                if res.status_code == 200:
                    if __name__ == "__main__": #直接运行get_ip()生成一个代理ip池
                        print("正在爬取可用https代理ip:%s"%proxyip)
                        auth_ip.append(proxyip)
                    else:
                        return proxies         #作为模块被引用时，返回一个可用的proxies
            except:
                pass   
                #print(res.raw._connection.sock.getpeername()[0])#返回客户端IP,get请求要加参数stream=True
        if len(auth_ip) == 0:
            return 0
        else:
            return auth_ip
    return inner

@verify_ip
def get_ip(n = 3):
    global ips
    for i in range(n):
        url3 = base_url+str(i+1)
        try:
            response = requests.get(url3,headers = headers,timeout = 3)
            #print(response.status_code)
            html = etree.HTML(response.text,etree.HTMLParser())
            ip = html.xpath('//tbody//td[1]/text()')
        except Exception as e:
            print(e)
        else:
            ips = ips+ip


if __name__=="__main__":
    n_page = int(input("please input crawl number of pages:"))
    print(get_ip(n_page))
   
