from bot.bot_events.discord_events import DiscordEvents
from bot.services.discord.discord_events_service import IDiscordEventsService

class ApiDiscordEventsService(IDiscordEventsService):
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
