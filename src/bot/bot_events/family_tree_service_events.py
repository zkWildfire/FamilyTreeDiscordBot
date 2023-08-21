from events import Events # pyright: ignore[reportMissingTypeStubs]

class FamilyTreeServiceEvents(Events):
	"""
	Defines the events that can be triggered by family tree service instances.
	"""
	__events__ = (
		# Event emitted when a Discord server is added.
		# Args: (server_id: int, family_tree: IFamilyTree)
		"on_family_tree_created",

		# Event emitted when a family tree is modified.
		# Args: (server_id: int, family_tree: IFamilyTree)
		"on_family_tree_modified",

		# Event emitted when a Discord server is removed.
		# Args: (server_id: int)
		"on_family_tree_removed"
	)
