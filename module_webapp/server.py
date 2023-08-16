#!/usr/bin/env python3.10

import enum

class ServerType(enum.Enum):
	FRONT = enum.auto(),
	BACK = enum.auto(),
	DB = enum.auto(),

	@classmethod
	def has_value(cls, value):
		return any(x == value for x in cls.values())

class Server():
	def __init__(self, port, server_type):
		if not ServerType.has_value(server_type):
			exit(123)
		self.server_type = server_type
		self.port = port

if __name__ == "__main__":
	front = Server(80, ServerType.FRONT)
	back = Server(3000, ServerType.BACK)
	db = Server(5432, ServerType.DB)
