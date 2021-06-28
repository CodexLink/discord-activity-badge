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
    )  # todo: Finalize this later.
    from typing import Any, List, Literal, Union
    from argparse import ArgumentParser
    from elements.constants import (
        ARG_CONSTANTS,
        ARG_PLAIN_CONTAINER_NAME,
        ARG_PLAIN_DOC_INFO,
    )
    from asyncio import create_task, sleep as asyncio_sleep, Task
    from elements.constants import (
        LOGGER_DATETIME_FORMAT,
        LOGGER_FILENAME,
        LOGGER_LOG_LOCATION,
        LOGGER_OUTPUT_FORMAT,
    )

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
            )

            self.__children: dict[str, object] = {}

        async def register(
            self, cls: object
        ) -> Literal[True]:  # todo: Create an enumeration here.

            return True  # for now.

        @property
        def who_is_parent(self) -> str:  # todo: Refer to Line 50.
            return (
                self.__class__.__name__
            )  # Please evaluate if this really returns, who inherite this in the first case.

        @property
        def show_child(self) -> Union[str, dict[str, str], List[str]]:
            """
            A property function that returns the state of classes that was registered in this case.
            """
            return "str"

        def is_state_status(
            self, attr_name: str
        ) -> Literal[True]:  # todo: Refer to Line 50.
            """
            This function returns the certain state of this class.

            todo: Create possible attributes here.
            """

            return True

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
                await asyncio_sleep(0.1)

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
