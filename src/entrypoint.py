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

# # Entrypoint of the Application Services — entrypoint.py

if __name__ != "__main__":
    from elements.exceptions import EntryImportNotAllowed

    raise EntryImportNotAllowed

from distutils.util import strtobool
import logging
import os
from asyncio import (
    AbstractEventLoop,
    Future,
    Task,
    all_tasks,
    ensure_future,
    gather,
    get_event_loop,
)
from asyncio import sleep as asyncio_sleep
from asyncio import wait
from sys import stdout
from time import time as curr_exec_time
from typing import Any, Generator, Optional, Set, Type, Union

from api import AsyncRequestAPI
from args import ArgumentResolver
from badge import BadgeConstructor
from client import DiscordClientHandler
from elements.constants import (
    ContextOnSubject,
    ENV_FILENAME,
    ENV_STRUCT_CONSTRAINTS,
    LOGGER_FILENAME,
    LOGGER_OUTPUT_FORMAT,
    MAXIMUM_RUNTIME_SECONDS,
    RET_DOTENV_NOT_FOUND,
    ROOT_LOCATION,
    GithubRunnerActions,
)
from elements.exceptions import DotEnvFileNotFound
from enum import Enum
from elements.constants import PreferredActivityDisplay, PreferredTimeDisplay


class ActivityBadgeServices(
    ArgumentResolver, AsyncRequestAPI, DiscordClientHandler, BadgeConstructor
):
    """The start of everything. This is the core from initializing the workflow to generating the badge."""

    # # Special Methods.
    def __await__(self) -> Generator:
        return self.__start__().__await__()

    async def __start__(self, *args: list[Any], **kwargs: dict[Any, Any]) -> Any:
        """
        Step 0.1 | Instantiates all subclasses to prepare the module for the process.
        Step 0.1 | Prepare other modules / classes that may need to record until runtime.

        Notes:
                        (1.a) Let's load the logger first to enable backtracking incase if there's anything happened wrong. [If explicitly stated to run based on arguments.]
                        (1.b) We migh want to shield this async function to avoid corruption. We don't want a malformed output.
                        (2) Await the first super().__ainit__() which instantiates ArgumentResolver, this is required before we do tasking since we need to evaluate the given arguments.
                        (3.a) Instantiate the super().__init__(intents) which belongs to DiscordClientHandler. This is required to load other properties that is required by its methods.
                        (3.b) We cannot await this one because discord.__init__ is not a coroutine. And it shouldn't be, which is right.
                        (4) And once we load the properties, we can now asynchronously load discord in task. Do not await this task!
                        (5) There will be another task that is gathered into one so that it is distinguishly different than other await functions. They are quite important under same context.

        Credits:
                        (1) https://stackoverflow.com/questions/33128325/how-to-set-class-attribute-with-await-in-init.
                        (2) https://stackoverflow.com/questions/9575409/calling-parent-class-init-with-multiple-inheritance-whats-the-right-way/55583282#55583282
        """
        gather(self.prepare(), super().__ainit__())

        await asyncio_sleep(0.001)

        # * We can now insert the arguments at this point.
        self._init_logger(
            level_coverage=logging.DEBUG,
            log_to_file=getattr(self.args_container, "no_file"),
            out_to_console=getattr(self.args_container, "log_to_console"),
            verbose_client=getattr(self.args_container, "verbose_client"),
        )  # * (1) [a,b]

        # todo:ake ArgumentParser be the first one to execute.

        ensure_future(self.process())  # * (4)

        await self.__end__()

    # # User Space Functions
    async def prepare(self) -> None:
        """
        A function that prepares any modules and functions to load before the process.

        Basically, it (1) checks for parameter values, (2) checks for a file that should be existing under script directory (ie. README.md) right after being able to fetch the repository.
        This function has to run without any exceptions before being able to instantiate other functions that may start the proess of whatever this is.

        Note:
                        (n) Validate the arguments given in the secrets. If they aren'
                        (n) Fetch the repository first. Error whenever there's a process that can't be done via Exception.
                        (1) Check if the key from ENV_STRUCT_CONSTRAINTS is valid by checking them in os.environ.
                        (2) If they dont have a value or does not exist, are they optional?
                        (3) If optional, assigned value (with respect to the type) and push those to self.envs.
                        (4) If not optional, then proceed with emitting error, telling to the runner that it should be filled by the user.
                        (5) If they have a value that it isn't None and has a value for any type then try to resolve that value with respect to type().

        Note:
                        This does not resolve the value to the point that it will be valid from other functions that needs it. I just want to make them less of a burden
                        without explicitly convering and calling them during run time. I want it prepared before proceeding anything.

        todo: Annotate better to feel the seperation of two intention code here.
        """

        if not isinstance(ENV_STRUCT_CONSTRAINTS, dict):  # * (1)
            self.logger.critical(
                f"Constraints ({type(ENV_STRUCT_CONSTRAINTS)}) for the evaluation of Env is invalid! (expects to be {type(dict)}) Please contact the developer if you think this is a bug!"
            )
            os._exit(-1)

        await asyncio_sleep(0.001)

        if getattr(self.args_container, "local"):
            self._check_dotenv()  # ! This cannot be awaited.

        else:
            self.logger.info(
                "Argument -l / --local is not invoked. Skipping '.env' checking... (at self.__check_dotenv)"
            )

        self._resolve_envs()
        await asyncio_sleep(0.001)

        self.logger.info("Waiting for the API Connection Tester to finish...")  # ! (2)
        await wait([self._test_api_task])

        await self.github_api_connect()  # Authenticate first before we do something.

    # Wrapper of other steps.
    async def process(self) -> None:
        """
        Step 3 | Discord Accessing and Caching of Data.
        Step 4 | Badge Generation.
        Step 5 | Submit changes.

        Let these tasks have a referrable variable first, just for DRY implementation.

        ! The _raw_readme_data has been able to asynchronously run along with github_api_connect()
        ! I know there will be no problem so far in terms of rate getting limited. But if you think I should really wait
        ! for github_api_connect(), please make an issue about this.

        """

        _raw_readme_data: Future = ensure_future(
            self.exec_api_actions(GithubRunnerActions.FETCH_README)
        )  # todo: Create error when it was unable to connect or the README does not exist.

        await asyncio_sleep(0.001)

        self.logger.info("Instantiating Discord Client's WebSocket and Connection...")

        _discord_client_task: Future = ensure_future(
            self.start(self.envs["DISCORD_BOT_TOKEN"])
        )  # * (4)

        await wait([_raw_readme_data])  # Checkpoint.
        ensure_future(self.check_badge_identifier(_raw_readme_data.result()))

        await wait([_discord_client_task])  # Checkpoint.
        ensure_future(self.construct_badge())

        self.logger.info("Entrypoint: Done loading all tasks.")

    async def __end__(self) -> None:
        """
        An end-part of the entrypoint functionality. This contains handler for when to end the script and display logs when it can't.
        It should wait 0.5 sec for every changes. Anything below 0.5 will cause the log to be unreadable.
        """

        __timeout_start = curr_exec_time()

        while True:
            __this_time = curr_exec_time() - __timeout_start
            __tasks: Set[Task] = all_tasks()

            if (__this_time >= MAXIMUM_RUNTIME_SECONDS) and not getattr(
                self.args_container, "local"
            ):
                self.logger.critical(
                    "The script took longer to finish than the expected time of 5 seconds. This may be due to connection to Discord Gateway API not responding or your connection is not stable enough if you are running in local. If this issue occured in Github Runner, please try again. If persisting, contact (CodexLink) the developer."
                )  # ! Keep an extra information in README.md where you can check the connection by going through any voice channel and see the status of your connection.
                os._exit(-1)

            # # Keep in mind that, we could make this inline whenever the script is running in local mode.

            if (
                len(all_tasks()) <= 1
            ):  # todo: Add seconds I think before we process this code-block.
                self.logger.info(
                    "No other tasks were detected aside from Main Event Loop. Closing some sessions."
                )

                await self.close()
                self.logger.info("Closing Sessions (1 of 2) | discord -> Done.")
                await self._api_session.close()
                self.logger.info("Closing Sessions (2 of 2) | aiohttp -> Done.")

                break

            self.logger.info(
                f"Waiting for other {len(__tasks)} tasks to finish. | Time Execution: {__this_time:.2f}/{MAXIMUM_RUNTIME_SECONDS} seconds."
            )
            # self.logger.debug(f"All Tasks in Queue | {all_tasks()}")

            await asyncio_sleep(0.4)

    # # Utility Functions
    def _check_dotenv(self) -> None:  # # Mandatory.
        """
        Step 0.2 | Prepare the .env file to load in this script.
        If function "find_dotenv" raise an error, the script won't run.
        Or else, run Step 0.2.

        Pre-req: Argument -l or --local. Or otherwise, this function will not run.
        """
        try:
            self.logger.info(f"Invoked -l / --local, importing `dotenv` packages.")
            from dotenv import find_dotenv, load_dotenv

        except ModuleNotFoundError:
            self.logger.critical(
                "Did you installed dotenv from poetry? Try 'poetry install' to install dev dependencies."
            )

        try:
            self.logger.info(f"Attempting to locate {ROOT_LOCATION}/{ENV_FILENAME}")
            load_dotenv(
                find_dotenv(
                    filename=ROOT_LOCATION + ENV_FILENAME,
                    raise_error_if_not_found=True,
                )
            )
            self.logger.info(
                f"Env File at {ROOT_LOCATION + ENV_FILENAME} was validated."
            )

        except IOError:
            self.logger.critical(
                f"File {ENV_FILENAME} at {ROOT_LOCATION} is malformed or does not exists!"
            )
            raise DotEnvFileNotFound(RET_DOTENV_NOT_FOUND)

    def _init_logger(  # # Mandatory.
        self,
        level_coverage: Optional[int] = logging.DEBUG,
        log_to_file: Optional[bool] = False,
        out_to_console: Optional[bool] = False,
        verbose_client: Optional[bool] = False,
    ) -> None:
        """
        Step 0.3 | Loads the logger for all associated modules.

        Args:
            level_coverage (Optional[int], optional): Sets the level (and above) to cover it in the logs or in stream. Defaults to logging.DEBUG.
            log_to_file (Optional[bool], optional): Creates a file and logs the data if set to True, or otherwise. Defaults to False.
            out_to_console (Optional[bool], optional): Output the log reports in the console, if enabled. Defaults to False.
            verbose_client (Optional[bool], optional): Bind discord to the logger to log other events that is out of scope of entrypoint.
        Summary: todo.
        """
        _levels = [
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
        ]

        # Expressed Statements
        __LOGGER_HANDLER_FORMATTER: Optional[logging.Formatter] = logging.Formatter(
            LOGGER_OUTPUT_FORMAT
        )
        __LOGGER_LEVEL_COVERAGE: int = (
            level_coverage if level_coverage in _levels else logging.DEBUG
        )

        self.logger: logging.Logger = logging.getLogger(
            __name__ if not verbose_client else "discord"
        )
        self.logger.setLevel(__LOGGER_LEVEL_COVERAGE)

        if log_to_file:
            file_handler = logging.FileHandler(
                filename=LOGGER_FILENAME, encoding="utf-8", mode="w"
            )
            file_handler.setFormatter(__LOGGER_HANDLER_FORMATTER)
            self.logger.addHandler(file_handler)

        if out_to_console:
            console_handler = logging.StreamHandler(stdout)
            console_handler.setFormatter(__LOGGER_HANDLER_FORMATTER)
            self.logger.addHandler(console_handler)

        if not level_coverage in _levels:
            self.logger.warning(
                "Argument level_coverage is invalid from any of the list in __level__. setLevel() will use a default value (logging.DEBUG) instead."
            )

        else:
            self.logger.debug(
                f"Logger Coverage Level was set to {level_coverage}."
            )  # todo: Make it enumerated to show the name.

        self.logger.info("The logger has been loaded.")

    def _resolve_envs(self) -> None:  # # Mandatory.
        self.envs: dict[str, Any] = {}  # * (1)

        for idx, (env_key, _) in enumerate(ENV_STRUCT_CONSTRAINTS.items()):  # * (3)

            try:
                _env_literal_val: Any = os.environ.get(env_key)
                _env_cleaned_name: str = env_key.removeprefix("INPUT_")
                # # For Github Actions.
                self.logger.debug(
                    "[%i] Env. Var. %s contains %s to be evaluated in %s."
                    % (
                        idx + 1,
                        env_key,
                        _env_literal_val if len(_env_literal_val) else "None",
                        ENV_STRUCT_CONSTRAINTS[env_key]["expected_type"]
                        if not hasattr(
                            ENV_STRUCT_CONSTRAINTS[env_key]["expected_type"], "__call__"
                        )
                        else ENV_STRUCT_CONSTRAINTS[env_key]["expected_type"].__name__,
                    )
                )
            except KeyError as Err:
                self.logger.critical(
                    f"Dictionary Key doesn't exists. This is a bug, please report this to the developer! | Info: {Err}"
                )
                os._exit(-1)

            try:  # Catch whenever environments does not exists under that instance (runner).
                if not len(
                    _env_literal_val
                ):  # Are they optional environments? Length should be 0 when performed in Github Action Runner.

                    # todo: check if optional with no default values has a true type of `str` or just NoneType.

                    self.logger.debug(
                        f"Env. Var. {env_key} doesn't have any value but exists. Checking if they are labelled as `required`..."
                    )

                    if not ENV_STRUCT_CONSTRAINTS[env_key]["is_required"]:
                        # self.logger.debug("It's not required, but is it None? > %s" % ENV_STRUCT_CONSTRAINTS[env_key]["fallback_value"] is None)
                        self.envs[_env_cleaned_name] = (
                            ENV_STRUCT_CONSTRAINTS[env_key]["expected_type"](
                                ENV_STRUCT_CONSTRAINTS[env_key]["fallback_value"]
                            )
                            if ENV_STRUCT_CONSTRAINTS[env_key]["fallback_value"]
                            is not None
                            else None
                        )

                        self.logger.info(
                            "Env. Var. %s has now a resolved value of %s! (with type %s)"
                            % (
                                env_key,
                                ENV_STRUCT_CONSTRAINTS[env_key]["fallback_value"],
                                type(ENV_STRUCT_CONSTRAINTS[env_key]["fallback_value"]),
                            )
                        )
                        continue

                    else:
                        self.logger.critical(
                            f"[{idx + 1}] Env. Var. {env_key} does not exist or does not have a supplied value! Please fill up the required fields (in constants.py) to be able to use this script."
                        )
                        os._exit(-1)

                if ENV_STRUCT_CONSTRAINTS[env_key]["expected_type"] in [int, str]:
                    self.envs[_env_cleaned_name] = (
                        ENV_STRUCT_CONSTRAINTS[env_key]["expected_type"](
                            _env_literal_val
                        )
                        # ! Evaluate this. Because this doesn't seem in the right place.
                        if ENV_STRUCT_CONSTRAINTS[env_key]["fallback_value"] is None
                        else None
                    )

                elif ENV_STRUCT_CONSTRAINTS[env_key]["expected_type"] is bool:
                    try:
                        self.envs[_env_cleaned_name] = bool(
                            strtobool((_env_literal_val))
                        )
                    except ValueError:
                        _fallback_bool_val: bool = ENV_STRUCT_CONSTRAINTS[env_key][
                            "fallback_value"
                        ]
                        self.envs[_env_cleaned_name] = _fallback_bool_val
                        self.logger.warning(
                            f"Env. Var. {env_key} has an invalid key that can't be serialized to boolean. Using a fallback value {_fallback_bool_val} instead."
                        )

                elif issubclass(ENV_STRUCT_CONSTRAINTS[env_key]["expected_type"], Enum):
                    self.logger.debug(
                        f"Env. Var. {env_key} expected type is a subclass of Enum! Attempting to resolve its value..."
                    )
                    _enum_candidates: list[Type[Enum]] = [
                        ContextOnSubject,
                        PreferredActivityDisplay,
                        PreferredTimeDisplay,
                    ]

                    is_valid: Union[None, bool] = None

                    # Since all enums are declared in upper case. User might intend to apply values in non-case-sensitive form. Hence, we gonna explicitly uppercase them.
                    _enum_case_env_val: str = _env_literal_val.upper()
                    if len(_enum_case_env_val):
                        for each_enums in _enum_candidates:  # This is gonna hurt.
                            for _each_cls in each_enums:
                                is_valid = _enum_case_env_val == _each_cls.name
                                self.envs[_env_cleaned_name] = (
                                    _each_cls
                                    if _enum_case_env_val == _each_cls.name
                                    else ENV_STRUCT_CONSTRAINTS[env_key][
                                        "fallback_value"
                                    ]
                                )
                                print(_enum_case_env_val, _each_cls.name)
                                if is_valid:
                                    break
                            if is_valid:
                                break

                        self.logger.info(
                            (f"Env. Var. {env_key} now has a value of %s!" % _each_cls)
                            if is_valid
                            else f"Env. Var. {env_key} was unable to resolve the given argument ({_enum_case_env_val}). Reverting to %s..."
                            % (ENV_STRUCT_CONSTRAINTS[env_key]["fallback_value"])
                        )

                else:
                    self.logger.critical(
                        f"Env. Var. '{_enum_case_env_val}' cannot be resolved / serialized due to its expected_type not a candidate for serialization. Please contact the developer about this for more information."
                    )

            except Exception as Err:  # We can't catch <class 'NoneType'> here. Use Exception instead.
                self.logger.critical(
                    f"Environment Variable {env_key} cannot be found. Are you running on local? Invoke --local if that would be the case. If persisting, check your environment file. If this was deployed, please report this issue to the developer. | Info: {Err}"
                )
                os._exit(-1)

        self.logger.info(f"Environment Variables stored in-memory and resolved!")
        self.logger.debug(f"Result of Env. Serialization |> {self.envs}")


# # Entrypoint Code
loop_instance: AbstractEventLoop = get_event_loop()
entry_instance: AbstractEventLoop = loop_instance.run_until_complete(
    ActivityBadgeServices()
)
