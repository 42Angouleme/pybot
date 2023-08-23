#!/usr/bin/env python3.10

import enum
import flask
import waitress

class ST(enum.Enum):
	FRONT = enum.auto(),
	BACK = enum.auto(),
	DB = enum.auto(),

	@classmethod
	def has_value(cls, value):
		return any(x == value for x in cls.__members__.values())

class Server():
	def __init__(self, port, server_type, host):
		if not ST.has_value(server_type):
			exit(123)
		self.server_type = server_type
		self.port = port
		self.listen_host = host

if __name__ == "__main__":
	front = Server(80, ST.FRONT)
	back = Server(3000, ST.BACK)
	db = Server(5432, ST.DB)
