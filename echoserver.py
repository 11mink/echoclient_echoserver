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

	serverSocket = socket(AF_INET, SOCK_STREAM)
	serverSocket.bind(addr)
	serverSocket.listen(5)
	socketList = [serverSocket]
	size = 1024

	while True:
		readable, writable, exceptional = select.select(socketList, [], [], 10)

		for sock in readable:
			if sock == serverSocket:
				clientSocket, addr = serverSocket.accept()
				socketList.append(clientSocket)
				print("client connected", addr)

			else:
				data = sock.recv(size)
				if not data:
					sock.close()
					socketList.remove(sock)
				elif broadcast:
					for client in socketList:
						if client == serverSocket:
							continue
						else:
							client.send(data)
				else:
					clientSocket.send(data)

if __name__ == "__main__":
	main()

