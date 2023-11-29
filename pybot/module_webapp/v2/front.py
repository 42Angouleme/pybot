#!/usr/bin/env python3.10

from .config import WEB_FRONT_PORT, WEB_HOME_PAGE, WEB_FRONT_LSTN_HOST
from .server import Server, ST
from .log import log, a, p

import waitress
import flask

class FrontServer():
	def __init__(self, port = WEB_FRONT_PORT, listen_host = WEB_FRONT_LSTN_HOST):
		self.server = Server(port, ST.FRONT, listen_host)
		self.home_page = WEB_HOME_PAGE
		self.app = flask.Flask(__name__)

	def add_route(self, route, file, **args):
		@self.app.route(route)
		def index():
			return flask.render_template(file, **args)

	def run(self):
		waitress.serve(
			self.app.run(host=self.server.listen_host, port=self.server.port)
		)
		log.print(f"Server listenning on port {a.GREEN}{self.server.port}{a.RST}")

if __name__ == "__main__":
	front = FrontServer()
	front.add_route("/", "./templates/index.hmtl", name_1="test", name_2="test_2")
	front.run()
