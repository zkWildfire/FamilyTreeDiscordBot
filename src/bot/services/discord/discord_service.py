from abc import ABC, abstractmethod
from bot.events.discord_events import DiscordEvents

class IDiscordService(ABC):
	"""
	Service responsible for emitting events in response to Discord API events.
	"""
	@property
	@abstractmethod
	def events(self) -> DiscordEvents:
		"""
		Events that can be triggered by Discord's API.
		"""
		raise NotImplementedError()
