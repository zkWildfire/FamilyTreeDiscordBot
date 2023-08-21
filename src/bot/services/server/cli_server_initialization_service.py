from bot.models.server import IServer
from bot.services.cli_service import CliService
from bot.services.server.server_initialization_service import IServerInitializationService

class CliServerInitializationService(IServerInitializationService):
	"""
	Server initialization service that allows user input via a CLI.
	"""
	def __init__(self,
		cli_service: CliService):
		"""
		Initializes the service.
		@param cli_service The service to use for user input.
		"""
		self._cli_service = cli_service


	def initialize_server(self, server_id: int) -> IServer:
		"""
		Initializes the given server.
		@param server_id The ID of the server to initialize.
		@returns The initialized server.
		"""
		raise NotImplementedError()
