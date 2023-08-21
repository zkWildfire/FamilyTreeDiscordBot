from abc import ABC, abstractmethod

class IUser(ABC):
	"""
	Represents a Discord user on a server.
	"""
	@property
	@abstractmethod
	def user_id(self) -> int:
		"""
		The Discord-assigned unique ID of the user.
		"""
		raise NotImplementedError()


	@property
	@abstractmethod
	def username(self) -> str:
		"""
		The username of the user.
		"""
		raise NotImplementedError()


	@property
	@abstractmethod
	def discriminator(self) -> int:
		"""
		The discriminator of the user.
		"""
		raise NotImplementedError()


	@property
	@abstractmethod
	def nickname(self) -> str:
		"""
		The nickname of the user.
		"""
		raise NotImplementedError()
