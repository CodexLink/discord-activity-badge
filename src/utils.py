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
	import logging
	from typing import Any
	from argparse import ArgumentParser
	from elements.constants import ARG_CONSTANTS, ARG_PLAIN_CONTAINER_NAME, ARG_PLAIN_DOC_INFO

	class InconstantArguments(object):
		def __init__(self, **kwargs: dict[Any, Any]) -> None:
			# Load default values here.
			self.is_args_loaded : bool = False

			# print(self.__class__.__name__)
			# print(dir(self.__class__.__class__))
			# print(self.__class__.mro())
			# print(self.__class__.__base__.__name__)
			# print(self.__class__.__bases__)
			self.load_parser()

		def __repr__(self) -> str:
			# Properly Update the string based on the received string.
			return f"<Argument Handler, Received: Argument/s, Loaded: {self.is_loaded} | Subclassed by {self.__class__.__name__}>"

		def __preload_container(self) -> None:
			self.container : object = type(ARG_PLAIN_CONTAINER_NAME, (object, ), {"__info__": ARG_PLAIN_DOC_INFO})

		def load_parser(self) -> None:
			# Check if we could do it first. We need to check if the class who subclass this is alive and true.
			# Once we done, allow loading dynamic class container and let the parser do it's work.
			self.__preload_container()

			self.parser = ArgumentParser(
				description=str(ARG_CONSTANTS["ENTRY_PARSER_DESC"]),
				epilog=str(ARG_CONSTANTS["ENTRY_PARSER_EPILOG"]),
			)

			self.parser.add_argument(
				"-d",
				"--disable-log",
				action="store_true",
				help=ARG_CONSTANTS["HELP_DESC_DISABLE_LOG"],
				required=False,
			)

			self.parser.add_argument(
				"-n",
				"--no-alert",
				action="store_true",
				help=ARG_CONSTANTS["HELP_DESC_NO_ALERT_USR"],
				required=False,
			)
			self.parser.add_argument(
				"-p",
				"--print-logs",
				action="store_true",
				help=ARG_CONSTANTS["HELP_DESC_PRINT_LOG_REALTIME"],
				required=False,
			)

			self.parser.parse_args(namespace=self.container) # To be divided later.

			# Just in case, we need to know if the arguments are evaluated. Turn is_loaded to True.
			self.is_args_loaded : bool = True

		@property  # self-check
		def is_loaded(self) -> bool:
			return self.is_args_loaded

		@property
		def loaded_by_who(self) -> str:
			return self.__class__.__name__


		def evaluate(self) -> None:
			pass

		@property
		def return_args(self) -> Any: # This is temporary.
			return self.container



	# if len(argv) == 1:
		# entry_parser.print_help()  # Invoke this when there's no arguments or is invalid.
	#
	# print(dir(handler))
	# # print(getattr(entry_parser, "run_only"))
	# print(vars(handler))

	class LoggerComponent:
		""" A utility that can instantiate logging for both modules. """

		# Class Attributes (Non-Shared)
		def __init__(self, **kwargs: dict[Any, Any]) -> None:
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
