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
    sleep as asyncio_sleep,
)

from sys import stdout
from time import time as curr_exec_time

from typing import Any, Generator, Optional, Tuple, Set
from discord.errors import LoginFailure
from github import Github
from github.GithubException import UnknownObjectException
from args import ArgumentResolver
from badge import BadgeConstructor
from client import DiscordClientHandler
from elements.constants import (
    ENV_FILENAME,
    LOGGER_FILENAME,
    LOGGER_OUTPUT_FORMAT,
    RET_DOTENV_NOT_FOUND,
    ROOT_LOCATION,
    MAXIMUM_RUNTIME_SECONDS,
)
from elements.exceptions import DotEnvFileNotFound
class ActivityBadgeServices(
    ArgumentResolver, DiscordClientHandler, BadgeConstructor
):
    """The start of everything. This is the core from initializing the workflow to generating the badge."""

    # # Special Methods.
    def __repr__(self) -> str:
        return f"<Activity Badge Service, ???>"

    def __await__(self) -> Generator:
        return self.__start__().__await__()

    async def __start__(self, *args: list[Any], **kwargs: dict[Any, Any]) -> Any:
        """
        Step 0.1 | Instantiates all subclasses to prepare the module for the process.

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
        await self.prepare()
        await self.prereq()

        await self._init_logger(
            level_coverage=logging.DEBUG,
            log_to_file=False,
            out_to_console=True,
        )  # * (1) [a,b]

        # await super().__ainit__()  # * (2)
        # await self._check_dotenv()

        # self.discord_client_task: Task = ensure_future(
        #     self.start(os.environ.get("INPUT_DISCORD_BOT_TOKEN"))
        # )  # * (4), start while we check something else

        # self.constraint_checkers: Task = self.prereq()  # * (5)

        # await self.constraint_checkers # Not sure of this one.

        # self.logger.info("Entrypoint: Done loading all tasks. Reaching Endpoint...")
        # await self.__end__()

    # # User Space Functions
    async def prereq(self) -> Any:

        # __abs_path : str = os.path.abspath(os.getcwd())
        # print(os.path.isfile(__abs_path + "/README.md"))
        # __list_dir : Any = os.listdir(__abs_path)
        # print(__list_dir) # Print either way if that's the case.

        try:
            _a = Github(os.environ.get("INPUT_WORKFLOW_TOKEN"))
            _repo = _a.get_repo(os.environ.get("INPUT_PROFILE_REPOSITORY"))

            _target_file = _repo.get_contents("README.md")

        except AssertionError:
            print("The token or the supplied vlaue of PROFILE_REPOSITORY is invalid. Please check and try again.")
            os._exit(-1)

        except UnknownObjectException:
            print(f"README.md does not exist or supplied custom name does not exist from the repository {_a.name}")
            os._exit(-1)

        # Step 0.4a | Checking of parameters before doing anything.
        # 1.1 | Parameter Key Validatation.
        # 1.2 | README Checking Indicators.
        # Step 0.4b | Evaluation of Parameters from Discord to Args.
        pass

    async def postreq(self) -> Any:
        # Step 0.4a | Checking of parameters before doing anything.
        # 1.1 | Parameter Key Validatation.
        # 1.2 | README Checking Indicators.
        # Step 0.4b | Evaluation of Parameters from Discord to Args.
        pass

    async def prepare(self) -> Any:
        self.time_on_hit = curr_exec_time()  # * ???
        self.__last_n_task: int = 0  # todo: Annotate these later.

    # Wrapper of other steps.
    async def process(self) -> None:
        # Step 3 | Discord Accessing and Caching of Data.
        # Step 4 | Badge Generation.
        # Step 5 | Submit changes.
        # ! If we can invoke the workflow credentials here. Then we can push this functionality.
        # * Or else, we have to make the steps in the workflow (yaml) to push the changes.

        pass

    async def __end__(self) -> None:
        """
        An end-part of the entrypoint functionality. This contains handler for when to end the script and display logs when it can't.
        It should wait 0.5 sec for every changes. Anything below 0.5 will cause the log to be unreadable.
        """
        while True:
            __this_time = curr_exec_time() - self.time_on_hit

            if __this_time >= MAXIMUM_RUNTIME_SECONDS:
                self.logger.critical(
                    "Time's up! We are taking too much time. Somethign is wrong... Terminating the script..."
                )
                os._exit(-1)

            self.logger.debug(
                f"Current Time Execution: {__this_time} | Constraint Set: {MAXIMUM_RUNTIME_SECONDS} seconds."
            )

            if len(all_tasks()) <= 1:
                self.logger.info(
                    "No other tasks were detected aside from Main Event Loop. Closing some sessions."
                )

                self.logger.info("Closing Sessions (2 of 2) | aiohttp -> Awating.")
                await self.request_session.close()
                self.logger.info("Closing Sessions (2 of 2) | aiohttp -> Done.")

                if not self.is_closed():
                    self.logger.info(
                        "Discord Client WebSocket is still open. Re-issuing Closing Session -> Awaiting."
                    )

                    try:
                        await self.discord_client_task

                    # todo: TRY TO CREATE A FUNCTION DOES THIS IN ENTRYPOINT OR SOMEWHERE ELSE. SEE CLIENT HANDLING OF ERROR WHICH IS THE SAME AS THIS.
                    except AttributeError as Err:
                        self.logger.critical(
                            f"The referred Env Variable is missing which results to NoneType. This is a developer's fault, please issue this problem to the author's repository. | Info: {Err}"
                        )
                        os._exit(-1)

                    except LoginFailure:
                        self.logger.critical(
                            "The provided DISCORD_BOT_TOKEN is malformed. Please copy and replace your secret token and try again."
                        )
                        os._exit(-1)

                    self.logger.info(
                        "Discord Client WebSocket is still open. Re-issuing Closing Session -> Done."
                    )

                break

            else:
                __tasks: Set[Task] = all_tasks()

                if self.__last_n_task != len(__tasks):
                    self.__last_n_task = len(__tasks)

                    self.logger.info(
                        f"Waiting for other {self.__last_n_task} tasks to finish."
                    )
                    self.logger.debug(f"Tasks -> {__tasks}")

                await asyncio_sleep(0.5)

    # # Utility Functions
    async def _init_logger(
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

        __levels__ = [
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
            level_coverage if level_coverage in __levels__ else logging.DEBUG
        )

        self.logger = logging.getLogger(
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

        if not level_coverage in __levels__:
            self.logger.warning(
                "Argument level_coverage is invalid from any of the list in __level__. setLevel() will use a default value (logging.DEBUG) instead."
            )

        else:
            self.logger.info(
                f"Logger Coverage Level was set to {level_coverage}."
            )  # todo: Make it enumerated to show the name.

        self.logger.info("The logger has been loaded.")

    async def _check_dotenv(self) -> None:
        """
        Step 0.2 | Prepare the .env file to load in this script.
        If function "find_dotenv" raise an error, the script won't run.
        Or else, run Step 0.2.

        Pre-req: Argument -rl or --run-locally. Or otherwise, will not run this function.
        """
        if self.args_container.running_on_local:
            try:
                from dotenv import find_dotenv, load_dotenv

            except ModuleNotFoundError:
                self.logger.critical(
                    "Did you installed dotenv from poetry? Try 'poetry install' to install dev dependencies."
                )

            self.logger.info(
                "Argument -rl / --running-on-local is invoked. Checking for '.env' file."
            )

            try:
                load_dotenv(
                    find_dotenv(
                        filename=ROOT_LOCATION + ENV_FILENAME,
                        raise_error_if_not_found=True,
                    )
                )
                self.logger.info(
                    "File exists and is indeed valid. Loaded in the script."
                )

            except IOError:
                self.logger.critical(
                    "File '.env' is either malformed or does not exists!"
                )
                raise DotEnvFileNotFound(RET_DOTENV_NOT_FOUND)

        else:
            self.logger.info(
                "Argument -rl / --running-on-local is not invoked. Skipping '.env' checking... (at self.__check_dotenv)"
            )

# # Entrypoint Code
loop_instance: AbstractEventLoop = get_event_loop()
entry_instance: AbstractEventLoop = loop_instance.run_until_complete(
    ActivityBadgeServices()
)
loop_instance.stop()
