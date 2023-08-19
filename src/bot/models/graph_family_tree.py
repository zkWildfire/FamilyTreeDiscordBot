from bot.models.tree_node import TreeNode
from bot.models.family_tree import IFamilyTree
from bot.util.discord_statics import DiscordStatics
from bot.views.tree_view import ITreeView
from bot.views.list_tree_view import ListTreeView
from typing import Dict

class GraphFamilyTree(IFamilyTree):
	"""
	Graph-based implementation of the family tree data model.
	"""
	def __init__(self, root_node: TreeNode):
		"""
		Initializes a new instance of the FamilyTree class.
		@param root_node The root node of the tree.
		"""
		self._root_node = root_node

		# Dictionary of all nodes in the tree
		# Each node is indexed by the full username of the user.
		self._nodes: Dict[str, TreeNode] = {
			root_node.discord_full_username: root_node
		}


	def __len__(self) -> int:
		"""
		Gets the number of nodes in the tree.
		"""
		return len(self._nodes)


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
		if node.discord_full_username in self._nodes:
			raise ValueError(
				f"Node for user {node.discord_full_username} already exists."
			)

		# Make sure the inviter exists in the tree
		if not node.inviter:
			raise RuntimeError(
				"Cannot add a second root node to the tree."
			)
		if node.inviter.discord_full_username not in self._nodes:
			raise ValueError(
				f"Inviter for user {node.discord_full_username} does not exist."
			)

		# Add the node to the tree
		self._nodes[node.discord_full_username] = node


	def find_node_by_username(self, username: str, user_id: int) -> TreeNode:
		"""
		Finds a node in the tree by the user's discord username.
		@param username The discord username to search for.
		@param user_id The discriminator associated with the user's discord
		  account.
		@throws KeyError If a node for the given username does not exist in
		  the tree.
		@returns The node for the given username.
		"""
		full_username = DiscordStatics.get_full_username(username, user_id)
		return self._nodes[full_username]


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
			node.discord_user_id
		)

		# Make sure the node is not the root node
		if node == self._root_node:
			raise ValueError("Cannot remove the root node.")

		# Update all child nodes to point to the parent node
		child_nodes = self.get_view().filter_to_child_nodes(node)
		for child_node in child_nodes:
			child_node.inviter = node.inviter

		# Remove the node from the tree
		del self._nodes[node.discord_full_username]
