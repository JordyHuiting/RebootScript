from __future__ import unicode_literals
#from PyCRC.CRC16 import CRC16

import requests
import re
import hashlib
import base64
import os, sys
from time import gmtime, strftime





def login(baseurl, username, password):
	s = requests.Session()
	r = s.get(baseurl + "html/home.html")
	csrf_tokens = grep_csrf(r.text)
	headers_update(s.headers,csrf_tokens[1])
	data = login_data(username, password, str(csrf_tokens[1]))
	r = s.request('POST', baseurl + "api/user/login", data=data)
	#s.headers.update({'__RequestVerificationToken': r.headers["__RequestVerificationToken"]})
	print( r.text)
	return s

def headers_update(dictbase, token):
	dictbase['Accept-Language'] = 'en-US'
	dictbase['Content-Type'] = 'application/x-www-form-urlencoded'
	dictbase['X-Requested-With'] = 'XMLHttpRequest'
	dictbase['__RequestVerificationToken'] = token
	dictbase['Cache-Control'] = 'no-cache'
	dictbase['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9'
	
def grep_csrf(html):
	pat = re.compile(r".*meta name=\"csrf_token\" content=\"(.*)\"", re.I)
	matches = (pat.match(line) for line in html.splitlines())
	return [m.group(1) for m in matches if m]

def encrypt(text):
		m = hashlib.sha256()
		#print(text)
		m.update(text)
		#print (m.hexdigest())
		return base64.b64encode(m.hexdigest().encode('ascii'))


def login_data(username, password, csrf_token):
	password_hash = encrypt(username.encode('ascii') + encrypt(password.encode('ascii')) + csrf_token.encode('ascii')).decode("utf-8")	
	return '<?xml version "1.0" encoding="UTF-8"?><request><Username>%s</Username><Password>%s</Password><password_type>4</password_type></request>' % (username, password_hash)


def reboot(baseurl, session):
        data = '<request><Control>1</Control></request>'
        r = s.request('POST', baseurl + "api/device/control", data=data)
        print(r.text)
        
pinghost =  "8.8.8.8"
logfile = "c:\\scripts\\rebootlog.txt"
baseurl = "http://192.168.8.1/"
username = "admin"
password = 'XXXX'


if __name__ == "__main__":
        

        response = os.system("ping -n 1 " + pinghost)
        if response == 0:
                print("Host is up!")

        else:
                print("Host is down!")
                print ("Trying to log in...")
                s = login(baseurl, username, password)
                print ("Logged in !!")
                f = open(logfile, 'a')
                f.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " Ping failed, attempt to reboot!\n" ) 
                f.close()
                reboot(baseurl,s)
                
                
                        
       
