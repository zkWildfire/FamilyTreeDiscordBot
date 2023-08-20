from bot.models.dict_family_tree import DictFamilyTree
from bot.models.family_tree import IFamilyTree
from bot.models.tree_node import TreeNode
from bot.services.serialization.serialization_service import ISerializationService
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

class JsonSerializationService(ISerializationService):
	"""
	Serialization service that writes to a JSON file on disk.
	"""
	def __init__(self, save_path: Path):
		"""
		Initializes a new instance of the class.
		@param save_path The path to the JSON file to save to.
		"""
		self._save_path = save_path


	def load_trees(self) -> Dict[int, IFamilyTree]:
		"""
		Loads all family trees from disk.
		@returns A dictionary of all family trees saved on disk, indexed by
		  Discord server ID.
		"""
		if not self._save_path.exists():
			return {}
		with self._save_path.open("r") as f:
			return {
				int(server_id): self._list_to_tree(nodes_list)
				for server_id, nodes_list in json.load(f).items()
			}


	def save_tree(self, server_id: int, tree: IFamilyTree) -> None:
		"""
		Saves the given family tree to disk.
		@param server_id The ID of the discord server that the tree belongs to.
		@param tree The family tree to save.
		"""
		trees = self.load_trees()
		trees[server_id] = tree
		JsonSerializationService._write(
			self._save_path,
			{
				server_id: JsonSerializationService._tree_to_list(tree)
				for server_id, tree in trees.items()
			}
		)


	def remove_tree(self, server_id: int) -> None:
		"""
		Removes a previously saved family tree from disk.
		@param server_id The ID of the discord server that the tree belongs to.
		"""
		trees = self.load_trees()
		del trees[server_id]
		JsonSerializationService._write(self._save_path, trees)


	@staticmethod
	def _tree_to_list(tree: IFamilyTree) -> List[Dict[str, Any]]:
		"""
		Converts the given tree to a list.
		@param tree The tree to convert.
		@returns A list that contains all nodes in the tree. The first node in
		  the list will always be the root node.
		"""
		return [
			JsonSerializationService._node_to_dict(n) for n in tree.get_view()
		]


	@staticmethod
	def _list_to_tree(nodes: List[Dict[str, Any]]) -> IFamilyTree:
		"""
		Converts the given list to a tree.
		@param nodes The list of dictionaries representing tree nodes.
		@returns A tree that contains all nodes in the list.
		"""
		if not nodes:
			raise ValueError("Cannot convert an empty list to a tree.")

		# Create each node and store it in a dictionary indexed by each node's
		#   discord ID.
		# This is necessary because the deserialization process will not restore
		#   the `inviter` property. Instead, that property will be set after
		#   all nodes have been created.
		nodes_dict: Dict[int, TreeNode] = {
			int(node_dict["discord_id"]): \
				JsonSerializationService._dict_to_node(node_dict)
			for node_dict in nodes
		}

		# Iterate over each node and set its inviter property
		for node_dict in nodes:
			# Find the node corresponding to the current node dictionary
			node = nodes_dict[int(node_dict["discord_id"])]

			# If the node has an inviter, find the corresponding node and set
			#   the inviter property
			if node_dict["inviter"]:
				node.inviter = nodes_dict[int(node_dict["inviter"])]

		# Find the root node
		root_node = next(iter(
			[n for n in nodes_dict.values() if n.inviter == None]
		))

		tree = DictFamilyTree(root_node)
		for node in nodes_dict.values():
			if node != root_node:
				tree.add_node(node)
		return tree


	@staticmethod
	def _node_to_dict(node: TreeNode) -> Dict[str, Optional[str]]:
		"""
		Converts the given node to a dictionary.
		@param node The node to convert.
		@returns A dictionary that contains all node data.
		"""
		return {
			"discord_id": str(node.discord_id),
			"username": node.discord_username,
			"discriminator": str(node.discord_discriminator),
			"nickname": node.user_nickname,
			"background_color": node.background_color,
			"inviter": str(node.inviter.discord_id) if node.inviter else None
		}


	@staticmethod
	def _dict_to_node(node_dict: Dict[str, Optional[str]]) -> TreeNode:
		"""
		Converts the given dictionary to a node.
		@warning This method will create a new tree node object but will not set
		  its inviter property. The inviter property must be set by the caller
		  after all nodes have been created.
		@param node_dict The dictionary to convert.
		@returns A node that contains all data in the dictionary.
		"""
		assert node_dict["discord_id"] is not None
		assert node_dict["username"] is not None
		assert node_dict["discriminator"] is not None
		assert node_dict["nickname"] is not None
		assert node_dict["background_color"] is not None

		return TreeNode(
			int(node_dict["discord_id"]),
			node_dict["username"],
			int(node_dict["discriminator"]),
			node_dict["nickname"],
			node_dict["background_color"],
			None
		)


	@staticmethod
	def _write(file: Path, data: Dict[Any, Any]) -> None:
		"""
		Writes the given data to the given file.
		@param file The file to write to.
		@param data The data to write to the file.
		"""
		with file.open("w") as f:
			json.dump(data, f, indent=2)
