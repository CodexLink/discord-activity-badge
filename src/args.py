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

if __name__ == "__main__":
	from elements.exceptions import IsolatedExecNotAllowed

	raise IsolatedExecNotAllowed

else:
	from typing import Any, Callable, List, Literal, Optional, Union
	from argparse import ArgumentParser
	from elements.constants import (
		ARG_CONSTANTS,
		ARG_PLAIN_CONTAINER_NAME,
		ARG_PLAIN_DOC_INFO
	)
	from asyncio import create_task, sleep as asyncio_sleep, Task, ensure_future

	class ArgumentResolver(object):
		"""
		An over-detailed async class that helps entrypoint class to manage arguments and deliver them at any subclasses, either specific or all of it.
		"""

		async def __init__(self, **kwargs: dict[Any, Any]) -> None:
			"""
			Contains State and Task Containers. Initialized when called via await from fellow async (super)class.

			Enumerations:
							Class State Containers
									- self.__is_args_evaluated
									- self.__task_container

			Task Containers
									- self.__task_container_create 	|  A task that creates a hidden class container for the evaluated args to reside after operation.
									- self.__task_parser_loader		| A task that initializes loading and evaluation of arguments. Created for future use. (ie. do not load until env is good)
			"""

			self.__is_args_evaluated: bool = False
			self.__task_container: object = None

			# * Task Containers
			self.__task_container_create: Task = ensure_future(self.__preload_container())
			self.__task_parser_loader: Task = ensure_future(self.__load_args())

			await asyncio_sleep(1) # This is defined but undefined.


			await self.__task_container_create
			self.logger.debug(f"Awaited Task (1): {self.__task_container_create=}")

			await self.__task_parser_loader     # This is temporary.
			self.logger.debug(f"Awaited Task: {self.__task_parser_loader=}")
			self.logger.info(f"Instance of {ArgumentResolver.__name__} was done doing tasks asynchronously.")

			super().__init__() # todo: Annotate this one.

		def __repr__(self) -> str:
			"""
			Represents the Class State when called or referred.

			Returns:
					str: Containing Class Container, combined in str.
			"""
			return f"<Argument Handler, Parent: {self.__class__.__name__}, Evaluated? {self.__is_args_evaluated}>"

		async def __preload_container(self) -> None:
			"""
			Creates a container for the class to forward evaluated args. Accessible under variable named "self.__task_container"
			"""

			self.__task_container = type(
				ARG_PLAIN_CONTAINER_NAME, (object,), {"__info__": ARG_PLAIN_DOC_INFO}
			)

			self.logger.info(f"The container {self.__task_container} was instantiated on runtime successfully.")

		async def __load_args(self) -> None:
			"""
			Loads the arguments given by the user or the machine upon running this script, if instructed.
			"""

			self.__parser = ArgumentParser(
				description=str(ARG_CONSTANTS["ENTRY_PARSER_DESC"]),
				epilog=str(ARG_CONSTANTS["ENTRY_PARSER_EPILOG"]),
			)

			self.logger.info("ArgumentParser: Instantiated.")

			self.__parser.add_argument(
				"-dr",
				"--dry-run",
				action="store_true",
				help=ARG_CONSTANTS["HELP_DESC_DRY_RUN"],
			)

			self.logger.debug(f"ArgumentParser: Argument -dr added.")

			self.__parser.add_argument(
				"-lc",
				"--log-to-console",
				action="store_true",
				help=ARG_CONSTANTS["HELP_DESC_LOG_TO_CONSOLE"],
				required=False,
			)

			self.logger.debug(f"ArgumentParser: Argument -lc added.")

			self.__parser.add_argument(
				"-dn",
				"--do-not-alert-user",
				action="store_true",
				help=ARG_CONSTANTS["HELP_DESC_NO_ALERT_USR"],
				required=False,
			)

			self.logger.debug(f"ArgumentParser: Argument -dn added.")

			self.__parser.add_argument(
				"-nl",
				"--no-file",
				action="store_true",
				help=ARG_CONSTANTS["HELP_DESC_NO_LOG_TO_FILE"],
				required=False,
			)

			self.logger.debug(f"ArgumentParser: Argument -nl added.")

			self.__parser.add_argument(
				"-vc",
				"--verbose_client",
				action="store_true",
				help=ARG_CONSTANTS["HELP_DESC_VERBOSE_CLIENT"],
				required=False,
			)

			self.logger.debug(f"ArgumentParser: Argument -vc added.")

			# We wait for the container to finish (from another task) and push those data to the container.
			await self.__task_container_create
			self.logger.debug(f"Awaited Task (2): {self.__task_container_create=}")

			# I would rather catch this than subclassing ArgumentParser to override exit methods
			# to compensate with the use of asyncio for all use case.
			try:
				self.__parser.parse_args(namespace=self.__task_container)
				self.logger.debug(f"ArgumentParser <self.__parser> has arguments parsed.")
				await asyncio_sleep(0.25)

			except SystemExit:
				self.logger.info(f"ArgumentParser raised SystemExit, exiting now...")
				exit(0)

			# Once done, let other function checkers that the args is available for use.
			self.__is_args_evaluated: bool = True

		async def get_parameter_value(
			self, arg_key: str
		) -> Union[bool, dict[str, bool], None]:
			"""
			Allows other class who inherits the superclass to access the arguments by requesting them.

			Args:
				arg_key (str): Invoke "*" if the class wants to receive the whole arguments forwarded, invoked or not (True or False).
					: Invoke "attribute | property" to get a singleton result.

			Returns:
				Union[bool, dict[str, bool], None]: Returns either True or False if property was invoked. Or a dictionary containing `str` as key and `bool` as value if "*" is invoked.

			todos: Maybe implement, exception_on_not_found?
			"""

			await self.__task_parser_loader  # If we start too early, await.

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
			return self.__is_args_evaluated

		@property
		def loaded_by_who(self) -> str:
			return self.__class__.__name__
