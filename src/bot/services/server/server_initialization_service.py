from abc import ABC, abstractmethod
from bot.models.server import IServer

class IServerInitializationService(ABC):
	"""
	Service used to handle server initialization.
	"""
	@abstractmethod
	def initialize_server(self, server_id: int) -> IServer:
		"""
		Initializes the given server.
		@param server_id The ID of the server to initialize.
		@returns The initialized server.
		"""
		raise NotImplementedError()
