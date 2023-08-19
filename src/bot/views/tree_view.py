from __future__ import annotations
from abc import ABC, abstractmethod
from bot.models.tree_node import TreeNode
from typing import Callable, Iterator

class ITreeView(ABC):
	"""
	Provides access to tree nodes in a family tree model.
	"""
	@abstractmethod
	def __iter__(self) -> Iterator[TreeNode]:
		"""
		Gets an iterator for the tree view.
		"""
		raise NotImplementedError()


	@abstractmethod
	def __len__(self) -> int:
		"""
		Gets the number of nodes in the view.
		"""
		raise NotImplementedError()


	@abstractmethod
	def filter_to_child_nodes(self, parent_node: TreeNode) -> ITreeView:
		"""
		Filters the tree view to only the child nodes of the given parent node.
		@param parent_node The parent node to filter by.
		@returns A new tree view containing only the child nodes of the given
		  parent node.
		"""
		raise NotImplementedError()


	@abstractmethod
	def filter_by(self, predicate: Callable[[TreeNode], bool]) -> ITreeView:
		"""
		Filters the tree view by the given predicate.
		@param predicate The predicate to filter by.
		@returns A new tree view containing only the nodes that match the
		  predicate.
		"""
		raise NotImplementedError()
