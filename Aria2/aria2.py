import json
from urllib.request import urlopen

server = "example.com"
port = "6800"
token = "token"

def AddURL(List):
	global server,port,token
	jsonreq = json.dumps({'jsonrpc': '2.0', 'id': 'qwer',
							  'method': 'aria2.addUri',
							  'params': ['token:'+token,List],
							  }).encode()
	c = urlopen('http://'+server+':'+port+'/jsonrpc', jsonreq)
