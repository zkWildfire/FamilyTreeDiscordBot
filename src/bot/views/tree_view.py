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
	def filter_by(self, predicate: Callable[[TreeNode], bool]) -> ITreeView:
		"""
		Filters the tree view by the given predicate.
		@param predicate The predicate to filter by.
		@returns A new tree view containing only the nodes that match the
		  predicate.
		"""
		raise NotImplementedError()


	@abstractmethod
	def filter_by_discriminator(self,
		discriminator: int) -> ITreeView:
		"""
		Filters nodes in the tree by the discriminator.
		@param discriminator The discriminator to filter by.
		@returns The nodes with the given discriminator.
		"""
		raise NotImplementedError()


	@abstractmethod
	def filter_by_nickname(self,
		nickname: str) -> ITreeView:
		"""
		Filters nodes in the tree by the nickname.
		@param nickname The nickname to filter by.
		@returns The nodes with the given nickname.
		"""
		raise NotImplementedError()


	@abstractmethod
	def filter_by_user_id(self, user_id: int) -> ITreeView:
		"""
		Filters nodes in the tree by the discord ID.
		@param user_id The unique ID associated with the user's discord account.
		@returns A view filtered to only the nodes with the given discord ID.
		  The returned view should only ever have a length of 0 or 1.
		"""
		raise NotImplementedError()


	@abstractmethod
	def filter_by_username(self,
		username: str) -> ITreeView:
		"""
		Filters nodes in the tree by the discord username.
		@param username The discord username to filter by.
		@returns The nodes with the given discord username.
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
