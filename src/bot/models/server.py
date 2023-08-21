from abc import ABC, abstractmethod
from bot.models.family_tree import IFamilyTree
from bot.models.user import IUser
from typing import Sequence

class IServer(ABC):
	"""
	Tracks internal bot state for a server.
	"""
	@property
	@abstractmethod
	def family_tree(self) -> IFamilyTree:
		"""
		The family tree for the server.
		"""
		raise NotImplementedError()


	@property
	@abstractmethod
	def server_id(self) -> int:
		"""
		The Discord-assigned unique ID of the server.
		"""
		raise NotImplementedError()


	@abstractmethod
	def get_users(self) -> Sequence[IUser]:
		"""
		Gets a list of all users in the server.
		@returns A list of all users in the server.
		"""
		raise NotImplementedError()
