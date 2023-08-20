from abc import ABC, abstractmethod
from bot.services.cli_service import CliService
from bot.services.discord.discord_service import IDiscordService
from bot.services.family_tree.family_tree_service import IFamilyTreeService
from bot.services.serialization.serialization_service import ISerializationService
from typing import Optional

class IServiceCollection(ABC):
	"""
	Provides access to all services used by the bot.
	"""
	@property
	@abstractmethod
	def cli_service(self) -> Optional[CliService]:
		"""
		The service used to test the bot using the command line.
		This service is only available when the bot is running in local testing
		  mode.
		"""
		raise NotImplementedError()


	@property
	@abstractmethod
	def discord_service(self) -> IDiscordService:
		"""
		The service used to emit events in response to Discord API events.
		"""
		raise NotImplementedError()


	@property
	@abstractmethod
	def family_tree_service(self) -> IFamilyTreeService:
		"""
		The service used to manage family trees.
		"""
		raise NotImplementedError()


	@property
	@abstractmethod
	def serialization_service(self) -> ISerializationService:
		"""
		The service used to save and load data from disk.
		"""
		raise NotImplementedError()
