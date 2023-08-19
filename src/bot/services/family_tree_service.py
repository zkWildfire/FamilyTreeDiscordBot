from abc import ABC, abstractmethod
from bot.events.event import IEvent
from bot.models.family_tree import IFamilyTree
from bot.models.tree_node import TreeNode

class IFamilyTreeService(ABC):
	"""
	Provides access to server-specific family tree instances.
	"""
	@property
	@abstractmethod
	def on_family_tree_created(self) -> IEvent[int, IFamilyTree]:
		"""
		An event that is emitted when a new family tree is created.
		The arguments will be the ID of the discord server and the new family
		  tree instance that was created for the Discord server. The family
		  tree instance will contain at least one node.
		"""
		raise NotImplementedError()


	@property
	@abstractmethod
	def on_family_tree_deleted(self) -> IEvent[int]:
		"""
		An event that is emitted when a new family tree is created.
		The argument will be the ID of the discord server that was removed.
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
