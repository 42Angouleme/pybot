#!/usr/bin/env python3.10

from .server import Server, ServerType
from . import DFLT_DB_PORT

class DBServer(Server):
	def __init__(self, port = DFLT_DB_PORT):
		super(FrontServer, self).__init__(port, ServerType.DB)

if __name__ == "__main__":
	pass
