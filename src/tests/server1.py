import socket

s = socket.socket()
host = socket.gethostname()
port = 12346
s.bind((host, port))

s.listen(5)
while True:
	c, addr = s.accept()
	print "Got connection from", addr
	c.send("5")
	c.close()
