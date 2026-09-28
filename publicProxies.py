from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
response = requests.get("https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text")
proxies = list()
try:
    proxies = response.text.split()
except requests.RequestException as e:
    print(e)
def check_proxy(url):
    httpxx = {"http":url,"https":url}
    try:
        res = requests.get("https://httpbin.org/",url,timeout=5)
        if res.status_code == 200:
            return url,True,res.status_code
    except requests.RequestException as e:
        print(e)
    return url,False,None

with ThreadPoolExecutor(max_workers=10) as excu:
    results = excu.map(check_proxy,proxies)
    with open("validProxies.txt","w",encoding="utf-8") as file:
        for url,valid,code in results:
            if valid:
                file.writelines(f"{url}\n")
    
