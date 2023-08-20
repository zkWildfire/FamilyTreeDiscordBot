from bot.services.cli_service import CliService
from bot.services.discord.discord_service import IDiscordService
from bot.services.family_tree.family_tree_service import IFamilyTreeService
from bot.services.invite.invite_service import IInviteService
from bot.services.serialization.serialization_service import ISerializationService
from bot.services.service_collection import IServiceCollection
from typing import Optional

class StructServiceCollection(IServiceCollection):
	"""
	Struct-like implementation of the IServiceCollection interface.
	"""
	def __init__(self,
		cli_service: Optional[CliService],
		discord_service: IDiscordService,
		family_tree_service: IFamilyTreeService,
		invite_service: IInviteService,
		serialization_service: ISerializationService):
		"""
		Initializes a new instance of the class.
		@param cli_service The service used to test the bot using the command
		  line.
		@param discord_service The service used to emit events in response to
		  Discord API events.
		@param family_tree_service The service used to manage family trees.
		@param invite_service The service used to determine who invited a user
		  to a server.
		@param serialization_service The service used to save and load data from
		  disk.
		"""
		self._cli_service = cli_service
		self._discord_service = discord_service
		self._family_tree_service = family_tree_service
		self._invite_service = invite_service
		self._serialization_service = serialization_service


	@property
	def cli_service(self) -> Optional[CliService]:
		"""
		The service used to test the bot using the command line.
		This service is only available when the bot is running in local testing
		  mode.
		"""
		return self._cli_service


	@property
	def discord_service(self) -> IDiscordService:
		"""
		The service used to emit events in response to Discord API events.
		"""
		return self._discord_service


	@property
	def family_tree_service(self) -> IFamilyTreeService:
		"""
		The service used to manage family trees.
		"""
		return self._family_tree_service


	@property
	def invite_service(self) -> IInviteService:
		"""
		The service used to determine who invited a user to a server.
		"""
		return self._invite_service


	@property
	def serialization_service(self) -> ISerializationService:
		"""
		The service used to save and load data from disk.
		"""
		return self._serialization_service
