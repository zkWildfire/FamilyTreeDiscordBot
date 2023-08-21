from bot.models.family_tree import IFamilyTree
from bot.models.server import IServer
from bot.models.user import IUser
from typing import Sequence

class LocalServer(IServer):
	"""
	Server implementation that relies entirely on local data.
	This implementation is primarily used for testing.
	"""
	def __init__(self,
		server_id: int,
		users: Sequence[IUser],
		family_tree: IFamilyTree):
		"""
		Initializes the server.
		@param server_id The Discord-assigned unique ID of the server.
		@param users The users on the server.
		@param family_tree The family tree for the server. This tree must
		  contain a node for the current owner of the server but should not
		  contain any other nodes as the nodes for the other users will be added
		  as part of the initialization process.
		"""
		self._server_id = server_id
		self._users = list(users)
		self._family_tree = family_tree


	@property
	def family_tree(self) -> IFamilyTree:
		"""
		The family tree for the server.
		"""
		return self._family_tree


	@property
	def server_id(self) -> int:
		"""
		The Discord-assigned unique ID of the server.
		"""
		return self._server_id


	def get_users(self) -> Sequence[IUser]:
		"""
		Gets a list of all users in the server.
		@pre `is_initialized` must be `True`.
		@returns A list of all users in the server.
		"""
		return self._users
