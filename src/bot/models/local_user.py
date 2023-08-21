from bot.models.user import IUser

class LocalUser(IUser):
	"""
	User implementation that relies purely on local data.
	This implementation is primarily used for testing.
	"""
	def __init__(self,
		user_id: int,
		username: str,
		discriminator: int,
		nickname: str):
		"""
		Initializes the user.
		@param user_id The Discord-assigned unique ID of the user.
		@param username The username of the user.
		@param discriminator The discriminator of the user.
		@param nickname The nickname of the user.
		"""
		self._user_id = user_id
		self._username = username
		self._discriminator = discriminator
		self._nickname = nickname


	@property
	def user_id(self) -> int:
		"""
		The Discord-assigned unique ID of the user.
		"""
		return self._user_id


	@property
	def username(self) -> str:
		"""
		The username of the user.
		"""
		return self._username


	@property
	def discriminator(self) -> int:
		"""
		The discriminator of the user.
		"""
		return self._discriminator


	@property
	def nickname(self) -> str:
		"""
		The nickname of the user.
		"""
		return self._nickname
