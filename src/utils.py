"""
Copyright 2021 Janrey "CodexLink" Licas

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

	http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from email.mime import base


if __name__ == "__main__":
	from elements.exceptions import IsolatedExecNotAllowed

	raise IsolatedExecNotAllowed

else:
	import logging
	from typing import Any, Generator, Union
	from argparse import ArgumentParser
	from elements.constants import (
		ARG_CONSTANTS,
		ARG_PLAIN_CONTAINER_NAME,
		ARG_PLAIN_DOC_INFO,
	)
	from asyncio import create_task, sleep as asyncio_sleep, Task

	class LoggerComponent:  # For this scenario, we might assume that
		"""A utility that can instantiate logging for both modules."""

		# Class Attributes (Non-Shared)

		# For everytime that the logger is instantiated. Get the superclass name.
		async def __init__(self, **kwargs: dict[Any, Any]) -> None:
			print(self.__class__.__name__, self.__class__.__base__)
			print(f"This was called in {self.__class__.__base__} | Should be LoggerComponent")

		def set_logging_state_child(self) -> None:
			pass

		@property
		def who_is_parent(self):
			pass

		@property
		def show_child(self):
			pass

		def output_to(self):
			pass

		# todo: Handle this later.
		# logger = logging.getLogger('discord')
		# logger.setLevel(logging.DEBUG)
		# handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
		# handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
		# logger.addHandler(handler)

		@property
		# todo: This can return an enum later.
		def get_current_level(self: object) -> str:
			pass

	class ArgumentResolver:
		async def __init__(self, **kwargs: dict[Any, Any]) -> None:
			# * Value Containers
			print(f"This was called in {self.__class__.__base__} | Should be Argument Resolvers")
			self.__is_args_loaded: bool = False
			self.__task_container: object = None

			# * Task Containers
			self.__task_container_create: Task = create_task(self.__preload_container())
			self.__task_parser_loader: Task = create_task(self.__load_args())

		# todo: Style this one.
		# Properly Update the string based on the received string.
		def __repr__(self) -> str:
			return f"<Argument Handler, Received: Argument/s, Loaded: {self.is_loaded} | Subclassed by {self.__class__.__name__}>"

		async def __preload_container(self) -> None:
			self.__task_container = type(
				ARG_PLAIN_CONTAINER_NAME, (object,), {"__info__": ARG_PLAIN_DOC_INFO}
			)

		async def __load_args(self) -> None:
			self.__parser = ArgumentParser(
				description=str(ARG_CONSTANTS["ENTRY_PARSER_DESC"]),
				epilog=str(ARG_CONSTANTS["ENTRY_PARSER_EPILOG"]),
			)

			self.__parser.add_argument(
				"-dn",
				"--do-not-alert-user",
				action="store_true",
				help=ARG_CONSTANTS["HELP_DESC_NO_ALERT_USR"],
				required=False,
			)

			self.__parser.add_argument(
				"-dr",
				"--dry-run",
				action="store_true",
				help=ARG_CONSTANTS["HELP_DESC_DRY_RUN"],
			)

			self.__parser.add_argument(
				"-nl",
				"--no-logging",
				action="store_true",
				help=ARG_CONSTANTS["HELP_DESC_NO_LOGGING"],
				required=False,
			)

			self.__parser.add_argument(
				"-lc",
				"--log-to-console",
				action="store_true",
				help=ARG_CONSTANTS["HELP_DESC_LOG_TO_CONSOLE"],
				required=False,
			)

			await self.__task_container_create  # We wait for the container to finish (from another task) and push those data to the container.

			# I would rather catch this than subclassing ArgumentParser to override exit methods to compensate with the use of asyncio for all use case.
			try:
				self.__parser.parse_args(namespace=self.__task_container)
				await asyncio_sleep(0.25)

			except SystemExit:
				await asyncio_sleep(0.1)

			self.__is_args_loaded: bool = True

		async def get_parameter_value(
			self, arg_key: str
		) -> Union[bool, dict[str, bool], None]:
			await self.__task_parser_loader  # If we start too early, then await.

			__valid_properties: Union[dict[str, bool], None] = None

			if arg_key == "*":
				__valid_properties = {}
				for key, data in vars(self.__task_container).items():

					if not key.startswith("__"):
						__valid_properties[key] = data
						await asyncio_sleep(0.05)
			else:
				__valid_properties = vars(self.__task_container).get(arg_key, None)

			return __valid_properties

		# These properties are for debugging purposes only. Might subject to remove if still not used in unit-testing.
		@property  # self-check
		def is_loaded(self) -> bool:
			return self.__is_args_loaded

		@property
		def loaded_by_who(self) -> str:
			return self.__class__.__name__
