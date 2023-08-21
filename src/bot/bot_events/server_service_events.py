from events import Events # pyright: ignore[reportMissingTypeStubs]

class ServerServiceEvents(Events):
	"""
	Defines the events that can be triggered by server service instances.
	"""
	__events__ = (
		# Event emitted when a Discord server is added.
		# Args: (server_id: int, family_tree: IFamilyTree)
		"on_server_added",

		# Event emitted when a Discord server is removed.
		# Args: (server_id: int)
		"on_server_removed"
	)
