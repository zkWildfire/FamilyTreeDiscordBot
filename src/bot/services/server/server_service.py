from abc import ABC, abstractmethod
from bot.bot_events.server_service_events import ServerServiceEvents
from bot.models.server import IServer

class IServerService(ABC):
	"""
	Service used to query information about servers.
	"""
	@property
	@abstractmethod
	def events(self) -> ServerServiceEvents:
		"""
		Event emitter for all server service events.
		"""
		raise NotImplementedError()


	@abstractmethod
	def add_server(self, server: IServer) -> None:
		"""
		Adds a server to the service.
		@param server The server to add.
		"""
		raise NotImplementedError()


	@abstractmethod
	def get_server(self, server_id: int) -> IServer:
		"""
		Gets the server with the given ID.
		@param server_id The unique ID of the server.
		@throws KeyError Thrown if the bot has not been added to the server.
		@returns The server with the given ID.
		"""
		raise NotImplementedError()


	@abstractmethod
	def remove_server(self, server_id: int) -> None:
		"""
		Removes a server from the service.
		@param server_id The unique ID of the server.
		@throws KeyError Thrown if the bot has not been added to the server.
		"""
		raise NotImplementedError()
