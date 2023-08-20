#!/usr/bin/env python3
# Entry point for the Family Tree Discord bot.
import argparse
from bot.models.tree_node import TreeNode
from bot.services.cli_service import CliService
from bot.services.discord.api_discord_service import ApiDiscordService
from bot.services.discord.cli_discord_service import CliDiscordService
from bot.services.family_tree.dict_family_tree_service import DictFamilyTreeService
from bot.services.invite.most_recent_invite_service import MostRecentInviteService
from bot.services.serialization.json_serialization_service import JsonSerializationService
from bot.services.service_collection import IServiceCollection
from bot.services.struct_service_collection import StructServiceCollection
import logging
from pathlib import Path
from typing import Dict
import sys

# Log levels that may be specified on the command line
LOG_LEVELS: Dict[str, int] = {
	"critical": logging.CRITICAL,
	"error": logging.ERROR,
	"warning": logging.WARNING,
	"info": logging.INFO,
	"debug": logging.DEBUG
}

# Background color used by default for nodes in generated diagrams
DEFAULT_NODE_BACKGROUND_COLOR = "#FFFFFF"

class BotFormatter(logging.Formatter):
	"""
	Formatter used for logging bot messages.
	"""
	# Mapping of log levels to the single character used to represent them.
	LOG_LEVEL_MAPPING = {
		'DEBUG': 'D',
		'INFO': 'I',
		'WARNING': 'W',
		'ERROR': 'E',
		'CRITICAL': 'C'
	}

	def format(self, record: logging.LogRecord) -> str:
		"""
		Re-maps the log level name to a single character.
		@param record The log record to format.
		@returns The formatted log record.
		"""
		record.levelname = BotFormatter.LOG_LEVEL_MAPPING.get(
			record.levelname,
			record.levelname[0]
		)
		return super().format(record)

class CliArgs(argparse.Namespace):
	"""
	Defines the command line arguments for the bot.
	"""
	# Path to the config file for the bot.
	# This may be a relative or absolute path to the config file. Relative paths
	#   will be interpreted relative to the current working directory.
	config: str

	# Path to the file to save family trees to.
	# This may be a relative or absolute path to the file. Relative paths will
	#   be interpreted relative to the current working directory.
	save_path: str

	# If enabled, provides a CLI to simulate Discord events instead of
	#   connecting to Discord's API.
	local: bool

	# The level of logging to use.
	log_level: str


def make_parser() -> argparse.ArgumentParser:
	"""
	Creates the argument parser for the bot.
	@returns The argument parser for the bot.
	"""
	parser = argparse.ArgumentParser(
		description="Family Tree Discord bot."
	)
	parser.add_argument(
		"--config",
		default="config.yml",
		type=str,
		help="The path to the config file for the bot."
	)
	parser.add_argument(
		"--save-path",
		default="trees.json",
		type=str,
		help="The path to the file to save family trees to."
	)
	parser.add_argument(
		"--local",
		action="store_true",
		help="If enables, uses a CLI to simulate Discord events instead of "
			"connecting to Discord's API."
	)
	parser.add_argument(
		"--log-level",
		default="info",
		choices=list(LOG_LEVELS.keys()),
		type=str,
		help="The level of logging to use."
	)
	return parser


def make_services(args: CliArgs) -> IServiceCollection:
	"""
	Creates the service collection for the bot.
	@param args The command line arguments for the bot.
	@returns The service collection for the bot.
	"""
	if args.local:
		discord_service = CliDiscordService()
		cli_service = CliService(discord_service)
	else:
		discord_service = ApiDiscordService()
		cli_service = None

	family_tree_service = DictFamilyTreeService()
	invite_service = MostRecentInviteService()
	serialization_service = JsonSerializationService(Path(args.save_path))

	# Bind to events
	def on_server_added(
		server_id: int,
		owner_id: int,
		owner_username: str,
		owner_discriminator: int,
		owner_nickname: str) -> None:
		"""
		Helper method for converting the event data to a tree node.
		"""
		root_node = TreeNode(
			owner_id,
			owner_username,
			owner_discriminator,
			owner_nickname,
			DEFAULT_NODE_BACKGROUND_COLOR,
			None
		)
		family_tree_service.register_discord_server(server_id, root_node)

	discord_service.events.on_server_added += on_server_added # type: ignore
	discord_service.events.on_server_removed += family_tree_service.remove_discord_server # type: ignore

	family_tree_service.events.on_family_tree_created += serialization_service.save_tree # type: ignore
	family_tree_service.events.on_family_tree_modified += serialization_service.save_tree # type: ignore
	family_tree_service.events.on_family_tree_removed += serialization_service.remove_tree # type: ignore

	return StructServiceCollection(
		cli_service,
		discord_service,
		family_tree_service,
		invite_service,
		serialization_service
	)


def main(*cli_args: str) -> int:
	"""
	Entry point for the Family Tree Discord bot.
	@param cli_args The command line arguments to parse. Should not include the
	  script name.
	"""
	# Process command line arguments
	parser = make_parser()
	args = parser.parse_args(cli_args, namespace=CliArgs())

	# Configure logging
	logger = logging.getLogger()
	logger.setLevel(LOG_LEVELS[args.log_level])

	# Configure the format used for logging
	handler = logging.StreamHandler()
	handler.setLevel(logging.DEBUG)
	formatter = BotFormatter(
		"(%(levelname)s)[%(asctime)s.%(msecs)03d] %(filename)s:%(lineno)d: %(message)s",
		datefmt = "%Y-%m-%d %H:%M:%S"
	)
	handler.setFormatter(formatter)
	logger.addHandler(handler)

	# Create the service collection
	services = make_services(args)

	# Run the bot
	if args.local:
		assert services.cli_service is not None
		services.cli_service.run()

	return 0


if __name__ == "__main__":
	sys.exit(main(*sys.argv[1:]))
