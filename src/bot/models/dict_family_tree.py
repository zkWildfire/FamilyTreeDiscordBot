from bot.bot_events.family_tree_events import FamilyTreeEvents
from bot.models.tree_node import TreeNode
from bot.models.family_tree import IFamilyTree
from bot.util.discord_statics import DiscordStatics
from bot.views.tree_view import ITreeView
from bot.views.list_tree_view import ListTreeView
from typing import Dict

class DictFamilyTree(IFamilyTree):
	"""
	Family tree implementation that keeps track of nodes in a dictionary.
	"""
	def __init__(self, root_node: TreeNode):
		"""
		Initializes a new instance of the FamilyTree class.
		@param root_node The root node of the tree.
		"""
		self._root_node = root_node
		self._events = FamilyTreeEvents()

		# Dictionary of all nodes in the tree
		# Each node is indexed by the user's discord account ID
		self._nodes: Dict[int, TreeNode] = {
			root_node.discord_id: root_node
		}


	def __len__(self) -> int:
		"""
		Gets the number of nodes in the tree.
		"""
		return len(self._nodes)


	@property
	def events(self) -> FamilyTreeEvents:
		"""
		Event emitter for all family tree events.
		"""
		return self._events


	def add_node(self, node: TreeNode) -> None:
		"""
		Adds a new node to the tree.
		@param node The node to add.
		@throws ValueError If a node for the given user already exists in the
		  tree.
		@throws ValueError If the inviter for the given node does not exist in
		  the tree.
		@throws ValueError If the inviter for the given node is None.
		"""
		# Make sure the node does not already exist in the tree
		if node.discord_id in self._nodes:
			raise ValueError(
				f"Node for user {node.discord_full_username} already exists."
			)

		# Make sure the inviter exists in the tree
		if not node.inviter:
			raise RuntimeError(
				"Cannot add a second root node to the tree."
			)
		if node.inviter.discord_id not in self._nodes:
			raise ValueError(
				f"Inviter for user {node.discord_full_username} does not exist."
			)

		# Add the node to the tree
		self._nodes[node.discord_id] = node


	def find_node_by_user_id(self, user_id: int) -> TreeNode:
		"""
		Finds a node in the tree by the user's discord ID.
		@param user_id The unique ID associated with the user's discord account.
		@throws KeyError If a node for the given user does not exist in the tree.
		@returns The node for the given username.
		"""
		view = self.get_view().filter_by_user_id(user_id)
		if len(view) == 0:
			raise KeyError(
				f"Node for user {user_id} does not exist."
			)

		assert len(view) == 1
		return next(iter(view))


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
		full_username = DiscordStatics.get_full_username(username, discriminator)
		view = self.get_view().filter_by_username(full_username)\
			.filter_by_discriminator(discriminator)
		if len(view) == 0:
			raise KeyError(
				f"Node for user {full_username} does not exist."
			)

		assert len(view) == 1
		return next(iter(view))


	def get_view(self) -> ITreeView:
		"""
		Gets a view of the entire tree.
		"""
		return ListTreeView(self._nodes.values())


	def remove_node(self, node: TreeNode) -> None:
		"""
		Removes a node from the tree.
		All child nodes of the given node will be re-assigned to the parent
		  node of the given node.
		@param node The node to remove.
		@throws ValueError If the given node does not exist in the tree.
		@throws ValueError Thrown if the node is the root node.
		"""
		# Get the node to remove
		node = self.find_node_by_username(
			node.discord_username,
			node.discord_discriminator
		)

		# Make sure the node is not the root node
		if node == self._root_node:
			raise ValueError("Cannot remove the root node.")

		# Update all child nodes to point to the parent node
		child_nodes = self.get_view().filter_to_child_nodes(node)
		for child_node in child_nodes:
			child_node.inviter = node.inviter

		# Remove the node from the tree
		del self._nodes[node.discord_id]
