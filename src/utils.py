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

from typing import Iterable

from elements.exceptions import LoggerOperationFailed, LoggerRegistrationFailed


if __name__ == "__main__":
	from elements.exceptions import IsolatedExecNotAllowed

	raise IsolatedExecNotAllowed

else:
	from logging import (
		basicConfig,
		info,
		critical,
		error,
		warning,
		INFO,
		DEBUG,
		WARNING,
		ERROR,
	)
	from typing import Any, Callable, List, Literal, Optional, Union
	from argparse import ArgumentParser
	from elements.constants import (
		ARG_CONSTANTS,
		ARG_PLAIN_CONTAINER_NAME,
		ARG_PLAIN_DOC_INFO
	)
	from asyncio import create_task, sleep as asyncio_sleep, Task
	from elements.constants import (
		LOGGER_DATETIME_FORMAT,
		LOGGER_FILENAME,
		LOGGER_LOG_LOCATION,
		LOGGER_OUTPUT_FORMAT,
		LoggerCodeRet,
		LOGGER_CHILD_PROPERTIES
  	)

	from elements.exceptions import LoggerRegistrationFailed

	from enum import Enum

	class LoggerComponent:
		"""
		A utility that can instantiate logging for both modules.

		Providing flexibility by wrapping a string to a special function of something. WIP.

		todo: ???
		"""

		async def __init__(self, **kwargs: dict[Any, Any]) -> None:
			"""
			Instantiates [...]

			Credits: https://stackoverflow.com/a/17558764/5353223 | For LoggerAdapter, I just knew it when I looked at the main page, not in HOW TO.
					 https://stackoverflow.com/a/17558757/5353223 | Shortcut
			"""

			basicConfig(
				filename=LOGGER_LOG_LOCATION + LOGGER_FILENAME,
				format=LOGGER_OUTPUT_FORMAT,
				level=INFO,
				datefmt=LOGGER_DATETIME_FORMAT,
				filemode="w+",
			) # todo: Change the level in accordance to cover all levels and handle it through the custom function log().

			self.__children: dict[str[dict[..., ...]]] = {}
			self.__last_ret_code: LoggerCodeRet = LoggerCodeRet.NO_RECORDED_RET_CODE

			self.ENV_PARAMS : dict[str, str] = {} # todo: Evaluate if possible.

			self.__to_console : bool = False # To be evaluated later.

			print(f"This was printed under the {LoggerComponent.__name__} Class.")

		# # Helper Functions
		async def __validate_children(self) -> Union[bool, None]:
			pass

		async def __evaluate_code_ret(self) -> str:
			return "str"

		async def __check_if_child(self) -> bool:
			return False

		async def __setup_child_props(self, ordered_values: List[Union[bool, int]]) -> dict[str, Union[bool, int]]:
			"""Setups the registered child props along with value to be pushed as one later.

			Args:
				ordered_values (List[Union[bool, int]]): A values that contains can_log, can_print and level_coveragein order.

			Returns:
				dict[str, Union[bool, int]]: Returns the context to be pushed later into the child.
			"""

			__default_props__ : dict[str, Union[bool, int]] = {}

			for idx, each_props in enumerate(LOGGER_CHILD_PROPERTIES):
				if each_props == "is_verified":
					__default_props__[each_props] = True
					continue

				__default_props__[each_props] = ordered_values[idx]

			return __default_props__


		async def __verify_and_push(self, cls_name: str, props_value: List[Union[bool, int]]) -> None:
			for each_cls in self.__class__.__mro__[:-1]: # Excludes "this" object.
				if cls_name in each_cls.__name__ and not cls_name in self.__children:

					__props_ctx__ = await self.__setup_child_props(props_value)

					self.__children[cls_name] = __props_ctx__

					await asyncio_sleep(0.2)
					break

				continue

			if not cls_name in self.__children: # I'm confused with the bases of this one. I'm just dumb this 12:58am.
				raise LoggerRegistrationFailed(LoggerCodeRet.INVALID_REGISTERED_CLS)

			return

		# # Main Functions
		async def register(
			self, cls: Union[str, Iterable[tuple[str]]], can_log: bool = False, can_print: bool = False, level_coverage: int = INFO
		) -> None: # todo: Create a custom type of this one.
			"""
			An async function that provides more control of whose class is candidated to log their output.
			This is redundant because I could've just fetched the self.__class__.__bases__ of this class.

			But because of the nature of potential use of this logger component in my future projects,
			I let the arguments "Optional", and if there's no arguments given, you know the rules and so do I.
			"""

			# First, let's check whether the parent inherits this class. If not reject it.

			__props_value__ : List[Union[bool, int]] = [can_log, can_print, level_coverage]

			if type(cls) == str: # Expects singleton.
				await create_task(self.__verify_and_push(cls, __props_value__))
				await asyncio_sleep(0.3)
				return

			elif type(cls) == tuple:
				if len(cls):
					for each_str in cls:
						if not each_str == LoggerComponent:
							await create_task(self.__verify_and_push(each_str.__name__, __props_value__))
							await asyncio_sleep(0.1)
					return

				raise LoggerRegistrationFailed(LoggerCodeRet.DOES_NOT_CONTAIN_VALUE)

			raise LoggerRegistrationFailed(LoggerCodeRet.SUPPLIED_INVALID_ELEMENT)

		async def unregister(
			self, child_cls_name: str
		) -> Union[
			Literal[LoggerCodeRet.UNREGISTER_SUCCESS],
			Literal[LoggerCodeRet.UNREGISTER_FAILED],
		]:
			raise NotImplementedError

		async def set_level_coverage(
			self,
			child_cls_name: str,
			level=Callable[..., None],
			temporary: bool = False,
		) -> Union[
			Literal[LoggerCodeRet.SET_LEVEL_FAILED],
			Literal[LoggerCodeRet.SET_LEVEL_SUCCESS],
			Literal[LoggerCodeRet.REFERRED_CHILD_DOES_NOT_EXIST],
			Literal[LoggerCodeRet.INVALID_REFERRED_LEVEL_FUNC],
		]:
			"""
   			An async function that set multiple levels per registered classes.

			If the logging library can do it for all modules, we can do it per class with magic ^^.
	  		"""
			raise NotImplementedError

		async def log(self, level: Callable, msg : str) -> None:
			""" Unknown for now.

			Args:
				level (Callable): ???
				msg (str): The message to display from the logger.

			Returns:
				Any: [description]

			todo: the following

			This should be the following way on how this code will gonna output in the end.
			(1) Verify the called class if they are the one in the listed self.__children.
			(2) Verify the level given, we expect that this is int, so strict the values based from the logging.
			(3) Check if we should do the print to console. If yes, then called that function.
			(4) Log it ! todo: Check for cls_name keyword in the format.
			(5) Done. We are expected to return None.


			"""
			return None

		async def set_child_props(self, target_cls: str, prop: str, value: Any) -> Any
			"""A function to set child's properties to a certain.

			Returns:
				[type]: [description]
			"""
			return None # lol. todo.

		# # Property Functions

		@property
		async def last_code_ret(self) -> dict[str, Union[int, str]]: # todo: Create resolver function about this one.
			""" """
			return {self.__last_ret_code.name: self.__last_ret_code.value, "msg": "None"}

		@property
		async def registered_cls(self) -> Union[str, List[str]]:
			"""
			A property function that returns either a string representing a single class, or a list if multiple.
			"""

			print(self.__children)
			return list(self.__children) if not len(self.__children) == 1 else str(list(self.__children)[0])

		@property
		def who_is_parent(self) -> str:
			return self.__class__.__name__

	class ArgumentResolver:
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
			self.__task_container_create: Task = create_task(self.__preload_container())
			self.__task_parser_loader: Task = create_task(self.__load_args())

			await asyncio_sleep(1) # This is defined but undefined.


			await self.__task_container_create
			await self.__task_parser_loader     # This is temporary.

			print(f"Loaded. This was printed under {self.__class__.__base__.__name__}")


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

		async def __load_args(self) -> None:
			"""
			Loads the arguments given by the user or the machine upon running this script, if instructed.
			"""

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

			# We wait for the container to finish (from another task) and push those data to the container.
			await self.__task_container_create

			# I would rather catch this than subclassing ArgumentParser to override exit methods
			# to compensate with the use of asyncio for all use case.
			try:
				self.__parser.parse_args(namespace=self.__task_container)
				await asyncio_sleep(0.25)

			except SystemExit:
				exit(0) # todo: Add enum, I know its too overkill, just want to classify magic numbers kek.

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
