import requests
from fake_useragent import UserAgent
from lxml import etree
import random
ips=[]
auth_ip=[]
url=r"http://www.xiladaili.com/https/"
url2=r"https://www.baidu.com"
headers={"User-Agent":UserAgent().Chrome}

def verify_ip(f):
    def inner(arg):
        f(arg)
        while(len(ips)!=0):
            try:
                proxyip=random.choice(ips)
                proxies={
                    "https":"https://"+proxyip
                    }
                ips.remove(proxyip)
                res=requests.get(url2,headers=headers,proxies=proxies,timeout=1,stream=True)
                if res.status_code==200:
                    print("正在爬取可用https代理ip:%s"%proxyip)
                    auth_ip.append(proxyip)
            except:
                pass   
                #print(res.raw._connection.sock.getpeername()[0])#返回客户端IP,get请求要加参数stream=True
        if len(auth_ip)==0:
            print("没有可用代理ip")
        else:
            return auth_ip
    return inner

@verify_ip
def get_ip(n=1):
    global ips
    i=1
    while(i<=n):
        url3=url+str(i)
        try:
            response=requests.get(url3,headers=headers,timeout=3)
            #print(response.status_code)
            html=etree.HTML(response.text,etree.HTMLParser())
            ip=html.xpath('//tbody//td[1]/text()')
        except Exception as e:
            print(e)
        else:
            ips=ips+ip
        i=i+1

if __name__=="__main__":
    print(get_ip(3))
