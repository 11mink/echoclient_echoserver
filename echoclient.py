import sys
import select
from socket import *

def usage():
		print("syntax : echoclient <host> <port>")
		print("sample : echoclient 127.0.0.1 1234")
		
def main():
	if len(sys.argv) != 3:
		usage()
		sys.exit()

	ip = sys.argv[1]
	port = sys.argv[2]
	addr = (ip, int(port))

	client = socket(AF_INET, SOCK_STREAM)
	client.connect(addr)
	print("connected")

	inputs = [sys.stdin, client]
	size = 1024
	received = True
	timeout = 0.1

	while True:
		readable, writable, exceptional = select.select(inputs,[],[],timeout)
		
		if readable == [] and received == False:
			print("disconnected")
			client.close()
			sys.exit()

		for sock in readable:
			if sock == client:
				data = client.recv(size)
				if not data:
					client.close()
					sys.exit()
				else:
					print("<Server> " + data)
					received = True
			elif sock == sys.stdin:
				client.send(raw_input())
				received = False

if __name__ == "__main__":
	main()