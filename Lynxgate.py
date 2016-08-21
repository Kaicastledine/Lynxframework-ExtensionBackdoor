#!usr/bin/env	python3

import os,sys
import time
import BaseHTTPServer
import urlparse


config_file = open('gate.ini').read()
HOST_NAME = config_file.split('SERVER_IP=')[1].split('#')[0]
PORT_NUMBER = int(config_file.split('SERVER_PORT=')[1].split('#')[0])

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_POST(s):
    	length = int(s.headers['Content-Length'])
    	s.send_response(200)
        post_data = urlparse.parse_qs(s.rfile.read(length).decode('utf-8'))
        for key, value in post_data.iteritems():
        	if "url" in key:
        		print "[+] url : " + value[0]
        	if "info" in key:
        		print "[+] Log : " + value[0]

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print "LynxGate Started ..."
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()