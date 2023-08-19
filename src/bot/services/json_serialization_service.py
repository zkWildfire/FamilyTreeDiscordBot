from bot.models.dict_family_tree import DictFamilyTree
from bot.models.family_tree import IFamilyTree
from bot.models.tree_node import TreeNode
from bot.services.serialization_service import ISerializationService
import json
from pathlib import Path
from typing import Dict, List

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
		with self._save_path.open("w") as f:
			json.dump({
				str(server_id): self._tree_to_list(tree)
				for server_id, tree in trees.items()
			}, f)


	def remove_tree(self, server_id: int) -> None:
		"""
		Removes a previously saved family tree from disk.
		@param server_id The ID of the discord server that the tree belongs to.
		"""
		trees = self.load_trees()
		del trees[server_id]
		with self._save_path.open("w") as f:
			json.dump({
				str(server_id): self._tree_to_list(tree)
				for server_id, tree in trees.items()
			}, f)


	@staticmethod
	def _tree_to_list(tree: IFamilyTree) -> List[TreeNode]:
		"""
		Converts the given tree to a list.
		@param tree The tree to convert.
		@returns A list that contains all nodes in the tree. The first node in
		  the list will always be the root node.
		"""
		return list(tree.get_view())


	@staticmethod
	def _list_to_tree(nodes: List[TreeNode]) -> IFamilyTree:
		"""
		Converts the given list to a tree.
		@param nodes The list of nodes to convert.
		@returns A tree that contains all nodes in the list.
		"""
		if not nodes:
			raise ValueError("Cannot convert an empty list to a tree.")

		root_node = nodes[0]
		tree = DictFamilyTree(root_node)
		for node in nodes[1:]:
			tree.add_node(node)
		return tree
