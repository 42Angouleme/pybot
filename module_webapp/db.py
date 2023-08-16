from module_webapp import Server

class DBServer(Server):
	def __init__(self, port = 5432):
		super(FrontServer, self).__init__(port, ServerType.DB)

if __name__ == "__main__":
	pass
