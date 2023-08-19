from abc import ABC, abstractmethod
from bot.models.family_tree import IFamilyTree
from typing import Dict

class ISerializationService(ABC):
	"""
	Interface for services that save and load data from disk.
	"""
	@abstractmethod
	def load_trees(self) -> Dict[int, IFamilyTree]:
		"""
		Loads all family trees from disk.
		@returns A dictionary of all family trees saved on disk, indexed by
		  Discord server ID.
		"""
		raise NotImplementedError()


	@abstractmethod
	def save_tree(self, server_id: int, tree: IFamilyTree) -> None:
		"""
		Saves the given family tree to disk.
		@param server_id The ID of the discord server that the tree belongs to.
		@param tree The family tree to save.
		"""
		raise NotImplementedError()


	@abstractmethod
	def remove_tree(self, server_id: int) -> None:
		"""
		Removes a previously saved family tree from disk.
		@param server_id The ID of the discord server that the tree belongs to.
		"""
		raise NotImplementedError()
