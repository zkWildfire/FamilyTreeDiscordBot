from typing import Callable, Generic, TypeVarTuple

Ts = TypeVarTuple("Ts")

class IEvent(Generic[*Ts]):
	"""
	Helper class used for type hinting events.
	This class is never instantiated. Instead, it is used as a type hint for
	  `@property` methods that provide access to `events` module event instances.
	"""
	def __iadd__(self, callback: Callable[[*Ts], None]) -> None:
		"""
		Adds a new event listener to the event.
		@param callback The event listener to add.
		"""
		raise NotImplementedError()


	def __isub__(self, callback: Callable[[*Ts], None]) -> None:
		"""
		Removes an event listener from the event.
		@param callback The event listener to remove.
		"""
		raise NotImplementedError()
