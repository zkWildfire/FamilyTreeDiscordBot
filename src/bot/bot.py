#!/usr/bin/env python3
# Entry point for the Family Tree Discord bot.
import argparse
from bot.services.family_tree.dict_family_tree_service import DictFamilyTreeService
from bot.services.serialization.json_serialization_service import JsonSerializationService
from bot.services.service_collection import IServiceCollection
from bot.services.struct_service_collection import StructServiceCollection
from pathlib import Path
import sys

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
	return parser


def make_services(args: CliArgs) -> IServiceCollection:
	"""
	Creates the service collection for the bot.
	@param args The command line arguments for the bot.
	@returns The service collection for the bot.
	"""
	family_tree_service = DictFamilyTreeService()
	serialization_service = JsonSerializationService(Path(args.save_path))

	# Bind to events
	family_tree_service.events.on_family_tree_created += serialization_service.save_tree # type: ignore
	family_tree_service.events.on_family_tree_modified += serialization_service.save_tree # type: ignore
	family_tree_service.events.on_family_tree_removed += serialization_service.remove_tree # type: ignore

	return StructServiceCollection(
		family_tree_service,
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

	# Create the service collection
	services = make_services(args)

	return 0


if __name__ == "__main__":
	sys.exit(main(*sys.argv[1:]))
