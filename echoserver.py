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
		for fd in readable:
			if fd == server:
				client, addr = server.accept()
				socketList.append(client)
				print("client connected", addr)
			else:
				data = fd.recv(size)
				if not data:
					fd.close()
					socketList.remove(fd)
				elif broadcast:
					for sock in socketList:
						if sock == server:
							continue
						else:
							sock.send(data)
				else:
					client.send(data)

if __name__ == "__main__":
	main()
