from bot.events.event import IEvent
from bot.events.family_tree_events import FamilyTreeEvents
from bot.models.dict_family_tree import DictFamilyTree
from bot.models.family_tree import IFamilyTree
from bot.models.tree_node import TreeNode
from bot.services.family_tree_service import IFamilyTreeService
from typing import Dict

class DictFamilyTreeService(IFamilyTreeService):
	"""
	Family tree service that stores family trees in a dictionary.
	"""
	def __init__(self):
		"""
		Initializes a new instance of the service.
		"""
		# Dictionary of all family trees, indexed by discord server ID.
		self._family_trees: Dict[int, IFamilyTree] = {}

		# Events object used to broadcast to event listeners
		self._events = FamilyTreeEvents()


	@property
	def on_family_tree_created(self) -> IEvent[int, IFamilyTree]:
		"""
		An event that is emitted when a new family tree is created.
		The arguments will be the ID of the discord server and the new family
		  tree instance that was created for the Discord server. The family
		  tree instance will contain at least one node.
		"""
		return self._events.on_family_tree_created # type: ignore


	@property
	def on_family_tree_deleted(self) -> IEvent[int]:
		"""
		An event that is emitted when a new family tree is created.
		The argument will be the ID of the discord server that was removed.
		"""
		return self._events.on_family_tree_deleted # type: ignore


	def register_discord_server(self,
		server_id: int,
		root_node: TreeNode) -> None:
		"""
		Registers a discord server and creates a new family tree for the server.
		@param server_id The unique ID of the discord server.
		@param root_node The root node for the server's family tree instance.
		@throws ValueError If a tree for the given server already exists.
		"""
		if server_id in self._family_trees:
			raise ValueError(
				f"Family tree for server {server_id} already exists."
			)

		tree = DictFamilyTree(root_node)
		self._family_trees[server_id] = tree
		self._events.on_family_tree_created(server_id, tree)


	def remove_discord_server(self, server_id: int) -> None:
		"""
		Removes a previously added discord server and its associated family tree.
		@param server_id The unique ID of the discord server.
		@throws KeyError If a tree for the given server does not exist.
		"""
		if server_id not in self._family_trees:
			raise KeyError(
				f"Family tree for server {server_id} does not exist."
			)

		del self._family_trees[server_id]
		self._events.on_family_tree_deleted(server_id)


	def get_family_tree(self, server_id: int) -> IFamilyTree:
		"""
		Returns the family tree object for a server the bot has been added to.
		@param server_id The unique ID of the discord server.
		@throws KeyError If a tree for the given server does not exist.
		@returns The family tree instance for the given server.
		"""
		if server_id not in self._family_trees:
			raise KeyError(
				f"Family tree for server {server_id} does not exist."
			)

		return self._family_trees[server_id]
