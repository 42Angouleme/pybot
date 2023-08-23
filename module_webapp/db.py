#!/usr/bin/env python3.10

from .server import Server, ST
from .config import WEB_DB_LSTN_HOST

class DBServer(Server):
	def __init__(self, port = 3000, listen_host = WEB_DB_LSTN_HOST):
		self.server = Server(port, ST.DB, listen_host)

if __name__ == "__main__":
	pass
