from __future__ import annotations
from bot.util.discord_statics import DiscordStatics
from typing import Optional

class TreeNode:
	"""
	Represents all data for a node in the generated family tree diagram.
	"""
	def __init__(self,
		discord_username: str,
		discord_user_id: int,
		user_nickname: str,
		background_color: str,
		inviter: Optional[TreeNode]):
		"""
		Initializes a new instance of the TreeNode class.
		@param discord_username The username of the user's discord account.
		@param discord_user_id The discriminator associated with the user's
		  discord account. Most accounts will have a discriminator of 0 since
		  discord migrated all user accounts to unique names. However, since
		  discriminators are still visible to bots, the value is still included
		  in the data model.
		@param user_nickname The nickname of the user in the server. This will
		  be what is displayed in the generated diagram for the user and may
		  change over time.
		@param background_color The background color to use for the user's node
		  in the generated diagram.
		"""
		self._discord_username = discord_username
		self._discord_user_id = discord_user_id
		self._user_nickname = user_nickname
		self._background_color = background_color
		self._inviter = inviter


	@property
	def discord_full_username(self) -> str:
		"""
		Gets the full username of the user's discord account.
		This is the username and discriminator combined.
		"""
		return DiscordStatics.get_full_username(
			self._discord_username,
			self._discord_user_id
		)


	@property
	def discord_username(self) -> str:
		"""
		Gets the username of the user's discord account.
		"""
		return self._discord_username


	@property
	def discord_user_id(self) -> int:
		"""
		Gets the discriminator associated with the user's discord account.
		Most accounts will have a discriminator of 0 since discord migrated all
		  user accounts to unique names. However, since discriminators are still
		  visible to bots, the value is still included in the data model.
		"""
		return self._discord_user_id


	@property
	def user_nickname(self) -> str:
		"""
		Gets the nickname of the user in the server.
		This will be what is displayed in the generated diagram for the user and
		  may change over time.
		"""
		return self._user_nickname


	@user_nickname.setter
	def user_nickname(self, value: str):
		"""
		Sets the nickname of the user in the server.
		@throws ValueError if the value is empty.
		"""
		if not value:
			raise ValueError("Cannot set a user's nickname to the empty string.")

		self._user_nickname = value


	@property
	def background_color(self) -> str:
		"""
		Gets the background color to use for the user's node in the generated
		diagram.
		"""
		return self._background_color


	@background_color.setter
	def background_color(self, value: str):
		"""
		Sets the background color to use for the user's node in the generated
		diagram.
		@throws ValueError if the value is empty.
		"""
		if not value:
			raise ValueError("Cannot set a user's background color to the empty string.")

		self._background_color = value


	@property
	def inviter(self) -> Optional[TreeNode]:
		"""
		Gets the node of the user that invited the user to the server.
		"""
		return self._inviter


	@inviter.setter
	def inviter(self, value: Optional[TreeNode]):
		"""
		Sets the node of the user that invited the user to the server.
		"""
		self._inviter = value
