from json import dumps, loads
from time import time
from flask import request
from hashlib import sha256
from requests import post
import os

from flask import Flask

app = Flask(__name__)
headers = {
  'authority': 'chatforai.site',
  'origin': 'https://chatforai.site',
  'referer': 'https://chatforai.site/',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
}
proxy = 0
proxies = list(loads(open('proxies.json').read()))
cities = list(loads(open('cities.json').read()))

def _conversation():
  if request.args.get("body") == None: return app.response_class('BODY EMPTY')
  print("# PROCESSING NEW REQUEST")
  global proxy
  global proxies
  global cities
  try:
    conversation = loads(request.args.get("body"))
    timestamp = int(time() * 1000)
    gpt_resp = post(
      'https://chatforai.site/api/generate',
      headers=headers,
      proxies={"https":proxies[proxy]},
      stream=True,
      data=dumps(
        separators=(',', ':'),
        obj={
          'messages':
          conversation,
          'time':
          timestamp,
          'pass':
          None,
          'sign':
          sha256(f'{timestamp}:{conversation[-1]["content"]}:k6zeE77ge7XF'.
                 encode()).hexdigest(),
          'key':
          ''
        }))
    print(gpt_resp.text)
    if "quota" in gpt_resp.text: raise Exception("Request requires new proxy")
    return app.response_class(gpt_resp.text, mimetype='text/markdown')

  except Exception as e:
    print(e)
    proxy += 1
    if proxy >= len(cities):
        os.system('python proxytest.py')
        proxy = 0
        proxies = list(loads(open('proxies.json').read()))
        cities = list(loads(open('cities.json').read()))
    print("--- CHANGING TO PROXY: "+cities[proxy]+" ---")
    return _conversation()

app.add_url_rule('/', view_func=_conversation, methods=['POST','GET'])
