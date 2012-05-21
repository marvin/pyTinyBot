import socket
import sys
import traceback

# some constants
SERVER = 'irc.hackint.eu'
PORT = 6667
NICKNAME = 'MarvinAutoBot'
BUFSIZE = 4096

# bot class
class bot:
	# __init__
	def __init__(self, host, port, nickname, ident="Bot", realname="bot", chans="#testdavid,#testdavid2"):
		self.host = host
		self.port = int(port)
		self.nickname = nickname
		self.ident = ident
		self.realname = realname
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, )
		self.chans = chans
		self.ping_count = 0
	# connect
	def connect(self):
		self.sock.connect((self.host, self.port))
		self.botinit()
		self.loop()
		
	# botinit
	def botinit(self):
		self.sock.send('NICK ' + self.nickname + '\n')
		self.sock.send('USER ' + self.ident + ' 8 * : ' + self.realname + ' \n')

	# connection loop
	def loop(self):
		while 1:
			replytosrv = ""
			data = self.sock.recv(BUFSIZE)
			if not data: break
			replytosrv = self.event(data)
			print replytosrv

	# event handling
	def event(self, data):
		arrdata = []
		for word in data.split(' '):
			arrdata.append(word)
		if arrdata[0] == 'PING':
			self.pong(arrdata[1])

		return data

	# ping back to pinger
	def pong(self, pongstring):
		self.sock.send('PONG ' + pongstring + ' \n')
		if self.ping_count == 0:
			self.join()
		self.ping_count = self.ping_count + 1

	# join listed channels
	def join(self):
		for chan in self.chans.split(','):
			print 'join: ' + chan
			self.sock.send('JOIN ' + chan + ' \n')

# initialize and connect bot
mybot = bot(SERVER, PORT, NICKNAME)
mybot.connect()