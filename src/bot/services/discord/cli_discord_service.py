import argparse
from bot.events.discord_events import DiscordEvents
from bot.services.discord.discord_service import IDiscordService
from typing import Callable, Dict, List, Optional

class CliDiscordServiceArgs(argparse.Namespace):
	"""
	Defines the command line arguments for the CLI Discord service.
	"""
	# The type of command to process.
	# This may be one of the following:
	#   - server_added
	#   - server_removed
	#   - invite_created
	#   - user_joined
	#   - user_left
	#   - user_nickname_changed
	type: str

	# The ID of the server the command is for.
	server_id: int

	# The ID of the user who created the invite.
	# Only applicable for invite_created commands.
	inviter_id: Optional[int]

	# The code of the invite.
	# Only applicable for invite_created commands.
	invite_code: Optional[str]

	# The time the invite was created.
	# Only applicable for invite_created commands.
	create_time: Optional[str]

	# The time the invite expires.
	# Only applicable for invite_created commands.
	expire_time: Optional[str]

	# The ID of the user the command is for.
	# Only applicable for user_joined, user_left, and user_nickname_changed
	#   commands.
	user_id: Optional[int]

	# The username of the user the command is for.
	# Only applicable for user_joined commands.
	username: Optional[str]

	# The discriminator of the user the command is for.
	# Only applicable for user_joined commands.
	discriminator: Optional[int]

	# The new nickname of the user the command is for.
	# Only applicable for user_nickname_changed commands.
	new_nickname: Optional[str]


class CliDiscordService(IDiscordService):
	"""
	Service that emits events in response to commands typed into the terminal.
	"""
	def __init__(self):
		"""
		Initializes the service.
		"""
		self._events = DiscordEvents()

		# Maps command types to the functions that process them
		self._cmd_handlers: Dict[str, Callable[[CliDiscordServiceArgs], None]] = {
			"server_added": self._emit_on_server_added,
			"server_removed": self._emit_on_server_removed,
			"invite_created": self._emit_on_invite_created,
			"user_joined": self._emit_on_user_joined,
			"user_left": self._emit_on_user_left,
			"user_nickname_changed": self._emit_on_user_nickname_changed
		}

		# Parser used to process commands typed into the terminal
		self._parser = argparse.ArgumentParser(
			description="Processes event commands originating from the CLI "
				"for testing purposes.",
			exit_on_error=False
		)
		self._parser.add_argument(
			"--type",
			choices=self._cmd_handlers.keys(),
			type=str,
			required=True,
			help="The type of command to process."
		)
		self._parser.add_argument(
			"--server-id",
			type=int,
			required=True,
			help="The ID of the server the command is for."
		)
		self._parser.add_argument(
			"--inviter-id",
			type=int,
			required=False,
			help="The ID of the user who created the invite. Only applicable "
				"for invite_created commands."
		)
		self._parser.add_argument(
			"--invite-code",
			type=str,
			required=False,
			help="The code of the invite. Only applicable for invite_created "
				"commands."
		)
		self._parser.add_argument(
			"--create-time",
			type=str,
			required=False,
			help="The time the invite was created. Only applicable for "
				"invite_created commands."
		)
		self._parser.add_argument(
			"--expire-time",
			type=str,
			required=False,
			help="The time the invite expires. Only applicable for "
				"invite_created commands."
		)
		self._parser.add_argument(
			"--user-id",
			type=int,
			required=False,
			help="The ID of the user the command is for. Only applicable for "
				"user_joined, user_left, and user_nickname_changed commands."
		)
		self._parser.add_argument(
			"--username",
			type=str,
			required=False,
			help="The username of the user the command is for. Only applicable "
				"for user_joined commands."
		)
		self._parser.add_argument(
			"--discriminator",
			type=int,
			required=False,
			help="The discriminator of the user the command is for. Only "
				"applicable for user_joined commands."
		)
		self._parser.add_argument(
			"--new-nickname",
			type=str,
			required=False,
			help="The new nickname of the user the command is for. Only "
				"applicable for user_nickname_changed commands."
		)


	@property
	def events(self) -> DiscordEvents:
		"""
		Events that can be triggered by Discord's API.
		"""
		return self._events


	def process_cmd(self, cli_args: List[str]) -> None:
		"""
		Processes the command and emits the appropriate event.
		@param cli_args The command line arguments to process.
		"""
		args = self._parser.parse_args(
			cli_args,
			namespace=CliDiscordServiceArgs()
		)

		try:
			self._cmd_handlers[args.type](args)
		except Exception as e:
			print(e)


	def _emit_on_server_added(self, args: CliDiscordServiceArgs) -> None:
		"""
		Emits the on_server_added event.
		@param args The command line arguments to process.
		"""
		self._events.on_server_added(args.server_id)


	def _emit_on_server_removed(self, args: CliDiscordServiceArgs) -> None:
		"""
		Emits the on_server_removed event.
		@param args The command line arguments to process.
		"""
		self._events.on_server_removed(args.server_id)


	def _emit_on_invite_created(self, args: CliDiscordServiceArgs) -> None:
		"""
		Emits the on_invite_created event.
		@param args The command line arguments to process.
		"""
		# Make sure the arguments for this event were provided
		if args.inviter_id is None:
			raise ValueError("Missing --inviter-id argument")
		if args.invite_code is None:
			raise ValueError("Missing --invite-code argument")
		if args.create_time is None:
			raise ValueError("Missing --create-time argument")
		if args.expire_time is None:
			raise ValueError("Missing --expire-time argument")

		self._events.on_invite_created(
			args.server_id,
			args.inviter_id,
			args.invite_code,
			args.create_time,
			args.expire_time
		)


	def _emit_on_user_joined(self, args: CliDiscordServiceArgs) -> None:
		"""
		Emits the on_user_joined event.
		@param args The command line arguments to process.
		"""
		# Make sure the arguments for this event were provided
		if args.user_id is None:
			raise ValueError("Missing --user-id argument")
		if args.username is None:
			raise ValueError("Missing --username argument")
		if args.discriminator is None:
			raise ValueError("Missing --discriminator argument")

		self._events.on_user_joined(
			args.server_id,
			args.user_id,
			args.username,
			args.discriminator
		)


	def _emit_on_user_left(self, args: CliDiscordServiceArgs) -> None:
		"""
		Emits the on_user_left event.
		@param args The command line arguments to process.
		"""
		# Make sure the arguments for this event were provided
		if args.user_id is None:
			raise ValueError("Missing --user-id argument")

		self._events.on_user_left(args.server_id, args.user_id)


	def _emit_on_user_nickname_changed(self, args: CliDiscordServiceArgs) -> None:
		"""
		Emits the on_user_nickname_changed event.
		@param args The command line arguments to process.
		"""
		# Make sure the arguments for this event were provided
		if args.user_id is None:
			raise ValueError("Missing --user-id argument")
		if args.new_nickname is None:
			raise ValueError("Missing --new-nickname argument")

		self._events.on_user_nickname_changed(
			args.server_id,
			args.user_id,
			args.new_nickname
		)
