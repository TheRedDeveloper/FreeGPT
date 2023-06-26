from requests import get
import json
from multiprocessing import Pool
import urllib.parse
import time

def TryProxy(url):
    try:
        res = get('https://chatforai.site/api/rate',proxies={"https":url})
        loc = str(res.json()["country"])+"-"+str(urllib.parse.unquote(str(res.json()["city"])))
        if res.json()["rate"] != None and res.json()["rate"] >= 10: raise Exception("RATE EXCEEDED: "+res.json()["expire"])
        print(url+","+loc)
        return url, loc
    except BaseException as e:
        print(url+",FAIL")
def TryProxyDict(proxy):
    return TryProxy("http://"+proxy["IP"]+":"+proxy["PORT"])
    # return TryProxy("http://"+proxy)
results = []
def callback(r):
    if r != None:
        results.append(r)
        print(json.dumps(results))
if __name__ == '__main__':
    print("fetching proxies...")
    # proxies = get("https://api.proxyscrape.com/v2/?request=displayproxies").text.splitlines()
    proxies = json.loads(open('Proxy List.json').read())
    print("proxies fetched!")
    pool = Pool(61)
    [pool.apply_async(TryProxyDict, args=(proxy,), callback=callback) for proxy in proxies]
    # pool.map(TryProxyDict, proxies)
    time.sleep(30)
    pool.terminate()
    urls = list(map(lambda x: x[0], results))
    cities = list(map(lambda x: x[1], results))
    json.dump(urls, open("proxies.json", "w"))
    json.dump(cities, open("cities.json", "w"))
    print("DONE")
