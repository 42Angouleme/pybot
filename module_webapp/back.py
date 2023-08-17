#!/usr/bin/env python3.10

from .server import Server, ServerType

class BackServer(Server):
	def __init__(self, port = 3000):
		super(FrontServer, self).__init__(port, ServerType.BACK)

if __name__ == "__main__":
	pass
