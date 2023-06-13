from requests import get
import json
from multiprocessing import Pool
import urllib.parse
def TryProxy(url):
    try:
        res = get('https://chatforai.site/api/rate',proxies={"https":url})
        loc = str(res.json()["country"])+"-"+str(urllib.parse.unquote(str(res.json()["city"])))
        print(url+","+loc)
    except:
        print(url+",FAIL")
def TryProxyDict(proxy):
    return TryProxy("http://"+proxy["IP"]+":"+proxy["PORT"])
if __name__ == '__main__':
    proxies = json.loads(open('Proxy List.json').read())
    pool = Pool(61)
    zip(*pool.map(TryProxyDict, proxies))