from abc import ABC, abstractmethod
from datetime import datetime

class IInviteService(ABC):
	"""
	Service used to determine who invited a user to a server.
	"""
	@abstractmethod
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
		raise NotImplementedError()


	@abstractmethod
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
		raise NotImplementedError()
