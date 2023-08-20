from bot.services.invite.invite_service import IInviteService
from datetime import datetime
from typing import Dict

class MostRecentInviteService(IInviteService):
	"""
	Service that uses the most recently created invite to resolve inviters.
	This class exists because Discord only provides information about the user
	  who joined a server and does not provide information about how the user
	  joined the server (as of 2023-08-20). This means that the only way to
	  determine who invited is to guesstimate it based on the most recently
	  created invite.
	@warning This implementation is a basic implementation that does not take
	  into account expiry times for invites.
	"""
	def __init__(self) -> None:
		"""
		Initializes a new instance of the class.
		"""
		# Maps server IDs to the ID of the user that created the most recently
		#   created invite.
		self._invites: Dict[int, int] = {}


	def on_invite_created(self,
		server_id: int,
		inviter_id: int,
		invite_code: str,
		create_time: datetime,
		expire_time: datetime) -> None:
		"""
		Called when a user creates an invite to a server.
		@param inviter_id The unique ID of the user that created the invite.
		@param invite_code The unique code of the invite.
		@param create_time The time the invite was created.
		@param expire_time The time the invite will expire.
		"""
		self._invites[server_id] = inviter_id


	def get_inviter(self,
		server_id: int,
		user_id: int) -> int:
		"""
		Figures out which user invited the new user to the server.
		@param server_id The unique ID of the discord server that the new user
		  joined.
		@param user_id The unique ID of the user that joined the server.
		@throws RuntimeError Thrown if the service was unable to determine who
		  invited the given user to the server.
		@returns The ID of the user that invited the new user to the server.
		"""
		if server_id not in self._invites:
			raise RuntimeError(
				f"Unable to determine who invited user {user_id} to server {server_id}."
			)

		return self._invites[server_id]
