from bot.bot_events.family_tree_service_events import FamilyTreeServiceEvents
from bot.models.dict_family_tree import DictFamilyTree
from bot.models.family_tree import IFamilyTree
from bot.models.tree_node import TreeNode
from bot.services.family_tree.family_tree_service import IFamilyTreeService
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
		self._events = FamilyTreeServiceEvents()


	@property
	def events(self) -> FamilyTreeServiceEvents:
		"""
		Event emitter for all family tree events.
		"""
		return self._events


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
		tree.events.on_modified += lambda t: self._events.on_family_tree_modified(server_id, t) # type: ignore

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

		tree = self._family_trees[server_id]
		del self._family_trees[server_id]
		self._events.on_family_tree_deleted(server_id, tree)


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
