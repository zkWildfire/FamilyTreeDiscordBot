from events import Events # pyright: ignore[reportMissingTypeStubs]

class DiscordEvents(Events):
	"""
	Defines the events that can be triggered by Discord's API.
	The events defined by this class only include those that are autogenerated
	  by Discord. Events that are manually triggered by users (bot commands,
	  reactions, etc) are not included in this class.
	"""
	__events__ = (
		# Event emitted when the bot is added to a new server.
		# Args: (server_id: int)
		"on_server_added",

		# Event emitted when the bot is removed from a server.
		# Args: (server_id: int)
		"on_server_removed",

		# Event emitted when a user creates an invite to a server.
		# Args: (
		#   server_id: int,
		#   inviter_id: int,
		#   invite_code: str,
		#   create_time: datetime,
		#   expire_time: datetime
		# )
		"on_invite_created",

		# Event emitted when a user joins a server.
		# Args: (server_id: int, user_id: int, username: str, discriminator: int)
		"on_user_joined"

		# Event emitted when a user leaves a server.
		# Args: (server_id: int, user_id: int)
		"on_user_left",

		# Event emitted when a user changes their nickname.
		# Args: (server_id: int, user_id: int, new_nickname: str)
		"on_user_nickname_changed"
	)