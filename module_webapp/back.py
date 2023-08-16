from module_webapp import Server

class BackServer(Server):
	def __init__(self, port = 3000):
		super(FrontServer, self).__init__(port, ServerType.BACK)

if __name__ == "__main__":
	pass
