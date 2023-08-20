from abc import ABC, abstractmethod
from bot.bot_events.family_tree_events import FamilyTreeEvents
from bot.models.tree_node import TreeNode
from bot.views.tree_view import ITreeView

class IFamilyTree(ABC):
	"""
	Data model for a family tree diagram.
	"""
	@abstractmethod
	def __len__(self) -> int:
		"""
		Gets the number of nodes in the tree.
		"""
		raise NotImplementedError()


	@property
	@abstractmethod
	def events(self) -> FamilyTreeEvents:
		"""
		Event emitter for all family tree events.
		"""
		raise NotImplementedError()


	@abstractmethod
	def add_node(self, node: TreeNode) -> None:
		"""
		Adds a new node to the tree.
		@param node The node to add.
		@throws ValueError If a node for the given user already exists in the
		  tree.
		@throws ValueError If the inviter for the given node does not exist in
		  the tree.
		"""
		raise NotImplementedError()


	@abstractmethod
	def find_node_by_user_id(self, user_id: int) -> TreeNode:
		"""
		Finds a node in the tree by the user's discord ID.
		@param user_id The unique ID associated with the user's discord account.
		@throws KeyError If a node for the given user does not exist in the tree.
		@returns The node for the given username.
		"""
		raise NotImplementedError()


	@abstractmethod
	def find_node_by_username(self,
		username: str,
		discriminator: int) -> TreeNode:
		"""
		Finds a node in the tree by the user's discord username.
		@param username The discord username to search for.
		@param discriminator The discriminator associated with the user's
		  discord account.
		@throws KeyError If a node for the given username does not exist in
		  the tree.
		@returns The node for the given username.
		"""
		raise NotImplementedError()


	@abstractmethod
	def get_view(self) -> ITreeView:
		"""
		Gets a view of the entire tree.
		"""
		raise NotImplementedError()


	@abstractmethod
	def remove_node(self, node: TreeNode) -> None:
		"""
		Removes a node from the tree.
		All child nodes of the given node will be re-assigned to the parent
		  node of the given node.
		@param node The node to remove.
		@throws ValueError If the given node does not exist in the tree.
		@throws ValueError Thrown if the node is the root node.
		"""
		raise NotImplementedError()
