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


	def filter_by(self, predicate: Callable[[TreeNode], bool]) -> ITreeView:
		"""
		Filters the tree view by the given predicate.
		@param predicate The predicate to filter by.
		@returns A new tree view containing only the nodes that match the
		  predicate.
		"""
		return ListTreeView(filter(predicate, self._nodes))
