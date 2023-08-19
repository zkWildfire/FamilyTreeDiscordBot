from abc import ABC, abstractmethod
from bot.services.family_tree.family_tree_service import IFamilyTreeService
from bot.services.serialization.serialization_service import ISerializationService

class IServiceCollection(ABC):
	"""
	Provides access to all services used by the bot.
	"""
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
