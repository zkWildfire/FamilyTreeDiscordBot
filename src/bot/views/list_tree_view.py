from bot.models.tree_node import TreeNode
from bot.views.tree_view import ITreeView
from typing import Callable, Iterable, Iterator

class ListTreeView(ITreeView):
	"""
	Provides access to tree nodes in a family tree model.
	This view will return nodes in the order they were provided to the
	  constructor.
	"""
	def __init__(self, nodes: Iterable[TreeNode]):
		"""
		Initializes a new instance of the ListTreeView class.
		@param root_node The root node of the tree.
		"""
		self._nodes = list(nodes)


	def __iter__(self) -> Iterator[TreeNode]:
		"""
		Gets an iterator for the tree view.
		"""
		return iter(self._nodes)


	def __len__(self) -> int:
		"""
		Gets the number of nodes in the view.
		"""
		return len(self._nodes)


	def filter_by(self, predicate: Callable[[TreeNode], bool]) -> ITreeView:
		"""
		Filters the tree view by the given predicate.
		@param predicate The predicate to filter by.
		@returns A new tree view containing only the nodes that match the
		  predicate.
		"""
		return ListTreeView(filter(predicate, self._nodes))


	def filter_by_discriminator(self,
		discriminator: int) -> ITreeView:
		"""
		Filters nodes in the tree by the discriminator.
		@param discriminator The discriminator to filter by.
		@returns The nodes with the given discriminator.
		"""
		return self.filter_by(
			lambda node: node.discord_discriminator == discriminator
		)


	def filter_by_nickname(self,
		nickname: str) -> ITreeView:
		"""
		Filters nodes in the tree by the nickname.
		@param nickname The nickname to filter by.
		@returns The nodes with the given nickname.
		"""
		return self.filter_by(
			lambda node: node.user_nickname == nickname
		)


	def filter_by_user_id(self, user_id: int) -> ITreeView:
		"""
		Filters nodes in the tree by the discord ID.
		@param user_id The unique ID associated with the user's discord account.
		@returns A view filtered to only the nodes with the given discord ID.
		  The returned view should only ever have a length of 0 or 1.
		"""
		return self.filter_by(
			lambda node: node.discord_id == user_id
		)


	def filter_by_username(self,
		username: str) -> ITreeView:
		"""
		Filters nodes in the tree by the discord username.
		@param username The discord username to filter by.
		@returns The nodes with the given discord username.
		"""
		return self.filter_by(
			lambda node: node.discord_username == username
		)


	def filter_to_child_nodes(self, parent_node: TreeNode) -> ITreeView:
		"""
		Filters the tree view to only the child nodes of the given parent node.
		@param parent_node The parent node to filter by.
		@returns A new tree view containing only the child nodes of the given
		  parent node.
		"""
		return ListTreeView(
			filter(
				lambda node: node.inviter == parent_node,
				self._nodes
			)
		)
