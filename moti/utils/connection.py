class Connection:
	def __init__(self, sock):
		self.sock = sock

	def __repr__(self):
		my_sock = ':'.join([str(i) for i in self.sock.getsockname()])
		con_sock = ':'.join([str(i) for i in self.sock.getpeername()])
		return f'<Connection from {my_sock} to {con_sock}>'

	def send(self, data):
		self.sock.sendall(data)

	def receive(self, size):
		message = b''
		while len(message)<size:
			try:
				t = self.sock.recv(size-len(message))
				if t:
					message += t
				else:
					raise Excption('connection lost')
			except:
				raise Exception('connection lost')
		return message

	def close(self):
		self.sock.close()

	def __enter__(self):
		return self

	def connect(host, port):
		import socket
		sock = socket.socket()
		sock.connect((host,port))
		return Connection(sock)

	def __exit__(self, exception, error, traceback):
		self.close()
