#!/usr/bin/env python3

from http.server import HTTPServer, CGIHTTPRequestHandler

class Handler(CGIHTTPRequestHandler):
    cgi_directories = ["/cgi-bin"]

PORT = 8080 

try:
	httpd = HTTPServer(("", PORT), Handler)
	print("serving at port", PORT)
	httpd.serve_forever()
except KeyboardInterrupt:
	print (" received, shutting down..")
	httpd.socket.close()
