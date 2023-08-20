from events import Events # pyright: ignore[reportMissingTypeStubs]

class FamilyTreeEvents(Events):
	"""
	Defines the events that can be triggered by family tree instances.
	"""
	__events__ = (
		# Event emitted when a family tree is modified.
		# Args: (family_tree: IFamilyTree)
		"on_modified"
	)
