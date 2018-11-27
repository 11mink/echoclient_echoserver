import sys
import select
from socket import *

def usage():
	print("syntax : echoserver <port> [-b]")
	print("sample : echoserver 1234 -b")

def main():
	broadcast = False
	if len(sys.argv) == 3 and sys.argv[2] == "-b":
		broadcast = True
	elif len(sys.argv) != 2:
		usage()
		sys.exit()

	ip = "127.0.0.1"
	port = sys.argv[1]
	addr = (ip, int(port))

	server = socket(AF_INET, SOCK_STREAM)
	server.bind(addr)
	server.listen(5)
	socketList = [server]
	size = 1024

	while True:
		readable, writable, exceptional = select.select(socketList, [], [], 10)
		for sock in readable:
			if sock == server:
				client, addr = server.accept()
				socketList.append(client)
				print("client connected", addr)
			else:
				data = sock.recv(size)
				if not data:
					sock.close()
					socketList.remove(sock)
				elif broadcast:
					for socket in socketList:
						if socket == server:
							continue
						else:
							socket.send(data)
				else:
					client.send(data)

if __name__ == "__main__":
	main()

