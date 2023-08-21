from abc import ABC, abstractmethod
from bot.bot_events.discord_events import DiscordEvents

class IDiscordEventsService(ABC):
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
