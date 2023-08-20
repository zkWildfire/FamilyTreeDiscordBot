from bot.events.discord_events import DiscordEvents
from bot.services.discord.discord_service import IDiscordService

class ApiDiscordService(IDiscordService):
	"""
	Service that emits events in response to Discord API events.
	"""
	def __init__(self):
		"""
		Initializes the service.
		"""
		self._events = DiscordEvents()


	@property
	def events(self) -> DiscordEvents:
		"""
		Events that can be triggered by Discord's API.
		"""
		return self._events
