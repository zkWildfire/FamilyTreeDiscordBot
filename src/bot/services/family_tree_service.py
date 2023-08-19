from abc import ABC, abstractmethod
from bot.events.family_tree_service_events import FamilyTreeServiceEvents
from bot.models.family_tree import IFamilyTree
from bot.models.tree_node import TreeNode

class IFamilyTreeService(ABC):
	"""
	Provides access to server-specific family tree instances.
	"""
	@property
	@abstractmethod
	def events(self) -> FamilyTreeServiceEvents:
		"""
		Event emitter for all family tree events.
		"""
		raise NotImplementedError()


	@abstractmethod
	def register_discord_server(self,
		server_id: int,
		root_node: TreeNode) -> None:
		"""
		Registers a discord server and creates a new family tree for the server.
		@param server_id The unique ID of the discord server.
		@param root_node The root node for the server's family tree instance.
		@throws ValueError If a tree for the given server already exists.
		"""
		raise NotImplementedError()


	@abstractmethod
	def remove_discord_server(self, server_id: int) -> None:
		"""
		Removes a previously added discord server and its associated family tree.
		@param server_id The unique ID of the discord server.
		@throws KeyError If a tree for the given server does not exist.
		"""
		raise NotImplementedError()


	@abstractmethod
	def get_family_tree(self, server_id: int) -> IFamilyTree:
		"""
		Returns the family tree object for a server the bot has been added to.
		@param server_id The unique ID of the discord server.
		@throws KeyError If a tree for the given server does not exist.
		@returns The family tree instance for the given server.
		"""
		raise NotImplementedError()
