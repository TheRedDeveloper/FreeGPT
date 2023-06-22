from requests import get
import json
from multiprocessing import Pool
import urllib.parse

def TryProxy(url):
    try:
        res = get('https://chatforai.site/api/rate',proxies={"https":url})
        loc = str(res.json()["country"])+"-"+str(urllib.parse.unquote(str(res.json()["city"])))
        if res.json()["rate"] != None and res.json()["rate"] >= 10: raise Exception("RATE EXCEEDED: "+res.json()["expire"])
        print(url+","+loc)
    except BaseException as e:
        print(url+",FAIL")
def TryProxyDict(proxy):
    return TryProxy("http://"+proxy["IP"]+":"+proxy["PORT"])
    # return TryProxy("http://"+proxy)
if __name__ == '__main__':
    print("fetching proxies...")
    # proxies = get("https://api.proxyscrape.com/v2/?request=displayproxies").text.splitlines()
    proxies = json.loads(open('Proxy List.json').read())
    print("proxies fetched!")
    pool = Pool(61)
    pool.map(TryProxyDict, proxies)
