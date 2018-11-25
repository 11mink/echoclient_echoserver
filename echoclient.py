import sys
import select
from socket import *

def usage():
	if len(sys.argv) != 3:
		print("syntax : echoclient <host> <port>")
		print("sample : echoclient 127.0.0.1 1234")
		sys.exit()

def main():
	usage()

	ip = sys.argv[1]
	port = sys.argv[2]
	addr = (ip, int(port))

	client = socket(AF_INET, SOCK_STREAM)
	client.connect(addr)
	print("connected")

	inputs = [sys.stdin, client]
	size = 1024
	received = True
	timeout = 0.5

	while True:
		readable, writable, exceptional = select.select(inputs,[],[],timeout)

		if readable == [] and received == False:
			print("disconnected")
			client.close()
			sys.exit()

		for sock in readable:
			if sock == client:
				print("<Server> " + client.recv(size))
				received = True

			elif sock == sys.stdin:
				client.send(raw_input())
				received = False

if __name__ == "__main__":
	main()

