from module_webapp import Server, ServerType

class FrontServer(Server):
	def __init__(self, port = 80):
		super(FrontServer, self).__init__(port, ServerType.FRONT)

	def start(self):
		pass

if __name__ == "__main__":
	front_server = FrontServer()
	front_server.start()
