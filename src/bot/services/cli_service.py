import argparse
from bot.services.discord.cli_discord_events_service import CliDiscordEventsService
from typing import Callable, Dict, List

class CliArgs(argparse.Namespace):
	"""
	Defines the command line arguments for the bot.
	"""
	# The type of command to process.
	# This may be one of the following:
	#   - event
	#   - command (to be implemented)
	cmd_type: str

	# The arguments to pass to the command.
	args: List[str]


class CliService:
	"""
	Service used for testing the bot using the command line.
	"""
	# Command issued to break out of the REPL.
	EXIT_CMD = "exit"

	def __init__(self,
		discord_service: CliDiscordEventsService):
		"""
		Initializes the service.
		@param discord_service The service to pass discord event commands to
			for processing.
		"""
		self._discord_service = discord_service
		self._cmd_handlers: Dict[str, Callable[[CliArgs], None]] = {
			"event": self._process_discord_event,
			CliService.EXIT_CMD: self._process_exit_command
		}
		self._parser = self._make_parser(list(self._cmd_handlers.keys()))


	def run(self) -> None:
		"""
		Runs the REPL for the service.
		"""
		cmd = ""
		while cmd != CliService.EXIT_CMD:
			# Wait for the user to enter a command
			cli_args = input(">> ").split(" ")

			try:
				args = self._parser.parse_args(cli_args, namespace=CliArgs())
				self._cmd_handlers[args.cmd_type](args)
				cmd = args.cmd_type
			except argparse.ArgumentError as e:
				# If the user entered an invalid command, print an error message
				#   but otherwise ignore it
				print(e)


	def _process_discord_event(self, args: CliArgs) -> None:
		"""
		Processes a Discord event.
		@param args The command line arguments to process.
		"""
		self._discord_service.process_cmd(args.args)


	def _process_exit_command(self, args: CliArgs) -> None:
		"""
		Processes the exit command.
		@param args The command line arguments to process.
		"""
		print("Exiting...")


	def _make_parser(self, cmds: List[str]) -> argparse.ArgumentParser:
		"""
		Creates the argument parser for the service.
		@returns The argument parser for the service.
		"""
		parser = argparse.ArgumentParser(
			description="CLI command parser for local testing.",
			exit_on_error=False
		)
		parser.add_argument(
			"cmd_type",
			choices=cmds,
			help="The type of command to process."
		)

		# Capture any additional arguments
		parser.add_argument(
			"args",
			nargs=argparse.REMAINDER,
			help="The arguments to pass to the command."
		)

		return parser
