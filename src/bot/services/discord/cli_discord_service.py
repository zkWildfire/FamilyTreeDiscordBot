import argparse
from bot.bot_events.discord_events import DiscordEvents
from bot.services.discord.discord_service import IDiscordService
import logging
from typing import Callable, Dict, List, Optional

logger = logging.getLogger(__name__)

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
	# Only applicable for server_added, user_joined, user_left, and
	#   user_nickname_changed commands.
	user_id: Optional[int]

	# The username of the user the command is for.
	# Only applicable for server_added and user_joined commands.
	username: Optional[str]

	# The discriminator of the user the command is for.
	# Only applicable for server_added and user_joined commands.
	discriminator: Optional[int]

	# The (maybe new) nickname of the user the command is for.
	# Only applicable for server_added and user_nickname_changed commands.
	nickname: Optional[str]


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
		self._parser = self._make_parser(list(self._cmd_handlers.keys()))


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
		try:
			args = self._parser.parse_args(
				cli_args,
				namespace=CliDiscordServiceArgs()
			)
			self._cmd_handlers[args.type](args)
		# For some reason, even though the parser is configured with
		#   `exit_on_error=False`, it's still throwing a SystemExit exception
		#   when it fails to parse the arguments. As a workaround, catch the
		#   exception and ignore it instead of exiting. Note that nothing needs
		#   to be printed here as the parser will have already printed an error
		#   message.
		except SystemExit as e:
			pass
		except argparse.ArgumentError as e:
			# If the user entered an invalid command, print an error message
			#   but otherwise ignore it
			# This is the code path that *should* be taken but isn't being
			#   taken since the parser is throwing a SystemExit exception.
			print(e)
		except ValueError as e:
			print(e)


	def _emit_on_server_added(self, args: CliDiscordServiceArgs) -> None:
		"""
		Emits the on_server_added event.
		@param args The command line arguments to process.
		"""
		if args.user_id is None:
			raise ValueError("Missing --user-id argument")
		if args.username is None:
			raise ValueError("Missing --username argument")
		if args.discriminator is None:
			raise ValueError("Missing --discriminator argument")
		if args.nickname is None:
			raise ValueError("Missing --nickname argument")

		logger.info(
			"Emitting on_server_added event:\n"
			f"  server id: {args.server_id}\n"
			f"  owner user id: {args.user_id}\n"
			f"  owner username: {args.username}\n"
			f"  owner discriminator: {args.discriminator}\n"
			f"  owner nickname: {args.nickname}"
		)
		self._events.on_server_added(
			args.server_id,
			args.user_id,
			args.username,
			args.discriminator,
			args.nickname
		)


	def _emit_on_server_removed(self, args: CliDiscordServiceArgs) -> None:
		"""
		Emits the on_server_removed event.
		@param args The command line arguments to process.
		"""
		logger.info(
			"Emitting on_server_removed event:\n"
			f"  server id: {args.server_id}"
		)
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

		logger.info(
			"Emitting on_invite_created event:\n"
			f"  server id: {args.server_id}\n"
			f"  inviter id: {args.inviter_id}\n"
			f"  invite code: {args.invite_code}\n"
			f"  create time: {args.create_time}\n"
			f"  expire time: {args.expire_time}"
		)
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

		logger.info(
			"Emitting on_user_joined event:\n"
			f"  server id: {args.server_id}\n"
			f"  user id: {args.user_id}\n"
			f"  username: {args.username}\n"
			f"  discriminator: {args.discriminator}"
		)
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

		logger.info(
			"Emitting on_user_left event:\n"
			f"  server id: {args.server_id}\n"
			f"  user id: {args.user_id}"
		)
		self._events.on_user_left(args.server_id, args.user_id)


	def _emit_on_user_nickname_changed(self, args: CliDiscordServiceArgs) -> None:
		"""
		Emits the on_user_nickname_changed event.
		@param args The command line arguments to process.
		"""
		# Make sure the arguments for this event were provided
		if args.user_id is None:
			raise ValueError("Missing --user-id argument")
		if args.nickname is None:
			raise ValueError("Missing --nickname argument")

		logger.info(
			"Emitting on_user_nickname_changed event:\n"
			f"  server id: {args.server_id}\n"
			f"  user id: {args.user_id}\n"
			f"  new nickname: {args.nickname}"
		)
		self._events.on_user_nickname_changed(
			args.server_id,
			args.user_id,
			args.nickname
		)


	def _make_parser(self, cmds: List[str]) -> argparse.ArgumentParser:
		"""
		Creates the argument parser for the service.
		@param cmds The commands that can be processed by the service.
		@returns The argument parser for the service.
		"""
		parser = argparse.ArgumentParser(
			# This is the string that must be typed into the terminal to select
			#   this class as the handler for the CLI command
			prog="event",
			description="Processes event commands originating from the CLI "
				"for testing purposes.",
			exit_on_error=False
		)
		parser.add_argument(
			"type",
			choices=cmds,
			type=str,
			help="The type of command to process."
		)
		parser.add_argument(
			"--server-id",
			"--sid",
			dest="server_id",
			type=int,
			required=True,
			help="The ID of the server the command is for."
		)
		parser.add_argument(
			"--inviter-id",
			"--iid",
			dest="inviter_id",
			type=int,
			required=False,
			help="The ID of the user who created the invite. Only applicable "
				"for invite_created commands."
		)
		parser.add_argument(
			"--invite-code",
			"--ic",
			dest="invite_code",
			type=str,
			required=False,
			help="The code of the invite. Only applicable for invite_created "
				"commands."
		)
		parser.add_argument(
			"--create-time",
			"--ct",
			dest="create_time",
			type=str,
			required=False,
			help="The time the invite was created. Only applicable for "
				"invite_created commands."
		)
		parser.add_argument(
			"--expire-time",
			"--et",
			dest="expire_time",
			type=str,
			required=False,
			help="The time the invite expires. Only applicable for "
				"invite_created commands."
		)
		parser.add_argument(
			"--user-id",
			"--uid",
			dest="user_id",
			type=int,
			required=False,
			help="The ID of the user the command is for. Only applicable for "
				"server_added, user_joined, user_left, and "
				"user_nickname_changed commands."
		)
		parser.add_argument(
			"--username",
			"--name",
			"-u",
			dest="username",
			type=str,
			required=False,
			help="The username of the user the command is for. Only applicable "
				"for server_added and user_joined commands."
		)
		parser.add_argument(
			"--discriminator",
			"--dc",
			"-d",
			dest="discriminator",
			type=int,
			required=False,
			help="The discriminator of the user the command is for. Only "
				"applicable for server_added and user_joined commands."
		)
		parser.add_argument(
			"--nickname",
			"--nick",
			"-n",
			dest="nickname",
			type=str,
			required=False,
			help="The nickname of the user the command is for. Only "
				"applicable for server_added and user_nickname_changed commands."
		)

		return parser
