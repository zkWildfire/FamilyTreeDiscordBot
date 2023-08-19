from bot.services.family_tree_service import IFamilyTreeService
from bot.services.serialization_service import ISerializationService
from bot.services.service_collection import IServiceCollection

class StructServiceCollection(IServiceCollection):
	"""
	Struct-like implementation of the IServiceCollection interface.
	"""
	def __init__(self,
		family_tree_service: IFamilyTreeService,
		serialization_service: ISerializationService):
		"""
		Initializes a new instance of the class.
		@param family_tree_service The service used to manage family trees.
		@param serialization_service The service used to save and load data from
		  disk.
		"""
		self._family_tree_service = family_tree_service
		self._serialization_service = serialization_service


	@property
	def family_tree_service(self) -> IFamilyTreeService:
		"""
		The service used to manage family trees.
		"""
		return self._family_tree_service


	@property
	def serialization_service(self) -> ISerializationService:
		"""
		The service used to save and load data from disk.
		"""
		return self._serialization_service
