import socket
import SocketServer
import SimpleHTTPServer
import urllib2
import urlparse
import fff
OUR_PORT = 12345

THR_HOST = '10.25.147.129'
THR_PORT = 54321

class Proxy(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):
		"""
		1 character of E
		50 characters of Domain
		10 characters of port
		1 character of N
		GET/POST
		1 character of space
		URL
		1 char of space
		HTTP/1.1
		0d0a
		"""
		uri = urlparse.urlparse(self.path)
		print "PROXY",uri
		print uri.scheme
		parts = uri.netloc.split(':')
		
		if len(parts) > 1:
			port = parts[1]
		else:
			port = '80'
		if len(uri.query):
			query = "?" + uri.query
		else:
			query = uri.query
		
		frame = "E%-50s%-10s N%s %s%s HTTP/1.1\n" % 
		( parts[0],port,'GET',uri.path,query)
		frame += "%s" % self.headers
		print frame
		
		output = fff.ncode(frame)
		
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect((THR_HOST,THR_PORT))
		s.sendall(output)
		data = ''
		while 1:
			t = s.recv(4096)
			if not len(t): break
			data += t
		self.wfile.write(data)
		s.close()
http = SocketServer.ForkingTCPServer(('',OUR_PORT),Proxy)
print "serving at %d port" % OUR_PORT
http.serve_forever()
