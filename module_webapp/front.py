#!/usr/bin/env python3.10

import waitress
import flask

from config import DFLT_FRONT_PORT, DFLT_HOME_PAGE, DFLT_LSTN_HOST
from server import Server, ST
from log import log, a, p

from pprint import pprint

class FrontServer():
	def __init__(self, port = DFLT_FRONT_PORT, listen_host = DFLT_FRONT_HOST):
		self.server = Server(port, ST.FRONT, DFLT_FRONT_LSTN_HOST)
		self.listen_host = listen_host
		self.home_page = DFLT_HOME_PAGE
		self.app = flask.Flask(__name__)

	def add_route(self, route, file, **args):
		pprint(args)
		@self.app.route(route)
		def index():
			return flask.render_template(file, **args)

	def run(self):
		waitress.serve(self.app.run(host=self.listen_host, port=self.port))
		log.print(f"Server listenning on port {a.GREEN}{self.server.port}{a.RST}")

if __name__ == "__main__":
	front = FrontServer()
	front.add_route("/", "./templates/index.hmtl", name_1="test", name_2="test_2")
	front.run()
