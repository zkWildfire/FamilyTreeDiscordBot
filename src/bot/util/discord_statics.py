class DiscordStatics:
	"""
	Defines various static helper methods for Discord-related functionality.
	"""
	@staticmethod
	def get_full_username(username: str, user_id: int) -> str:
		"""
		Gets the full username of the user's discord account.
		@param username The username of the user's discord account.
		@param user_id The discriminator associated with the user's discord
		  account.
		@returns The full username of the user's discord account.
		"""
		return f"{username}#{user_id}"
