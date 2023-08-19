from events import Events # pyright: ignore[reportMissingTypeStubs]

class FamilyTreeEvents(Events):
	"""
	Defines the events that can be triggered by family tree service instances.
	"""
	__events__ = (
		# Event emitted when a Discord server is added.
		# Args: (discord_server_id: int, family_tree: IFamilyTree)
		"on_family_tree_created",
		# Event emitted when a Discord server is removed.
		# Args: (discord_server_id: int)
		"on_family_tree_deleted"
	)
