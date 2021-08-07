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

from os import _exit as exit
from asyncio import (
    AbstractEventLoop,
    Task,
    all_tasks,
    create_task,
    current_task,
    get_event_loop,
)
from asyncio import sleep as asyncio_sleep, gather, wait
from time import time as curr_exec_time
from typing import Any, Generator, Iterable, Set, Type, Union

from api import AsyncGithubAPI
from badge import BadgeConstructor
from client import DiscordClientHandler
from elements.typing import Base64String, ResolvedClientResponse
from utils import UtilityFunctions
from elements.constants import (
    ENV_FILENAME,
    ENV_STRUCT_CONSTRAINTS,
    LoggerLevelCoverage,
    MAXIMUM_RUNTIME_SECONDS,
    GithubRunnerActions,
)


class ActivityBadgeServices(
    UtilityFunctions, AsyncGithubAPI, DiscordClientHandler, BadgeConstructor
):
    """The heart of the Discord Activity Badge. Everything runs in Object-Oriented Approach. Please check each functions for the progress."""

    def __await__(self) -> Generator:
        return self.__start__().__await__()

    async def __start__(self) -> None:
        """
        Instantiates all subclasses and runs other necessary functions (both async and non-async) for the whole process.
        Notes:

            1. Resolve Arguments first.
            2. Then call Avoid raising error by using getattr(). This mechanism is similar to resolve_envs() in self.initialize().

            From 1 to 2. Theses functions should be faster enough.

            Anything that is being called by super() in this case is pointed to class `UtilityFunctions`.
        """

        super().resolve_args()  # * (1)

        super().init_logger(  # * (2)
            level_coverage=LoggerLevelCoverage.DEBUG,  # todo: Handle this one after we fix all confirmed parameters in resolve_args.
            log_to_file=getattr(self.args, "no_file"),
            out_to_console=getattr(self.args, "log_to_console"),
            verbose_client=getattr(self.args, "verbose_client"),
        )

        if not isinstance(ENV_STRUCT_CONSTRAINTS, dict):  # * (3)
            self.logger.critical(
                f"Constraint Structure `ENV_STRUCT_CONSTRAINTS` is not a {type(dict)}! Please contact the developer if this script is executed under Github Actions."
            )
            exit(-1)

        (super().check_dotenv(), super().resolve_envs()) if getattr(  # * (4)
            self.args, "local"
        ) else self.logger.info(
            f"Running local mode invocation detected. Skipping checks for '{ENV_FILENAME}'."
        )

        self._cascade_init_cls: Task = create_task(  # (5)
            super().__ainit__(),
            name="Classes_AsyncGithubAPI_Child_Initialization",
        )

        # These two tasks are seperated for a reason. IT was due to referencing and static async mechanism.
        self._discord_client_task: Task = create_task(
            self.start(self.envs["DISCORD_BOT_TOKEN"]),
            name="DiscordClient_UserFetching",
        )  # * (4)

        self.readme_data: Union[Any, ResolvedClientResponse, Base64String] = create_task(
            self.exec_api_actions(GithubRunnerActions.FETCH_README),
            name="GithubAPI_README_Fetching"
        )

        self.badge_task: Task = create_task(self.construct_badge(), name="BadgeConstructor_Construct") # This relies to self._discord_client_task

        await wait({self.readme_data}) # Implicitly declare this wait instead inside of the function. There's nothing much to do while we wait to fetch README data.
        badge_updater: Task = create_task(self.check_and_update_badge(self.readme_data.result()[1]), name="README_BadgeChecker_Updater")

        await wait({badge_updater}) # This may be invoked inside of this function and waits inside with self!
        create_task(self.exec_api_actions(GithubRunnerActions.COMMIT_CHANGES, data=[self.readme_data.result()[0], badge_updater.result()])) # No need for variable reference since it's the last step.

        await self.__end__()
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

        """
        """
        Notes:
        1.Authenticate first before we do something.

        todo: Create error when it was unable to connect or the README does not exist.

        todo: Annotate better to feel the seperation of two intention code here.
        """

    async def __end__(self) -> None:
        """
        An end-part of the entrypoint functionality. This contains handler for when to end the script and display logs when it can't.
        It should wait 0.5 sec for every changes. Anything below 0.5 will cause the log to be unreadable.
        """

        self.logger.info("Done loading modules and necessary elements for the process.")

        __timeout_start = curr_exec_time()
        prev_tasks: Set[Any] = set({})

        while True:
            this_time = curr_exec_time() - __timeout_start

            if (this_time >= MAXIMUM_RUNTIME_SECONDS) and not getattr(
                self.args, "local"
            ):
                self.logger.critical(
                    "The script took longer to finish than the expected time of 5 seconds. This may be due to connection to Discord Gateway API not responding or your connection is not stable enough if you are running in local. If this issue occured in Github Runner, please try again. If persisting, contact (CodexLink) the developer."
                )  # ! Keep an extra information in README.md where you can check the connection by going through any voice channel and see the status of your connection.
                exit(-1)

            if (
                len(all_tasks()) <= 1
            ):  # todo: Add timeout before we process this code-block.
                self.logger.info(
                    "No other tasks detected. Cleaning up..."
                )

                await gather(self.close(), self._api_session.close())
                self.logger.info("Sessions closed. (Github API and Discord Client)")

                break

            tasks: Set[Task] = all_tasks()
            n_tasks: int = len(tasks)

            try:
                if prev_tasks != tasks:
                    self.logger.info(
                        f"{n_tasks} tasks left to finish the loop. | Time Execution: {this_time:.2f}/{MAXIMUM_RUNTIME_SECONDS}s."
                    )
                    prev_tasks = tasks

                    # self.logger.debug(
                    #     f"Current Tasks: {current_task()} | All Tasks in Queue | {all_tasks()}"
                    # )


            except TypeError:
                prev_tasks = tasks

            await asyncio_sleep(0)


# # Entrypoint Code
loop_instance: AbstractEventLoop = get_event_loop()
entry_instance: AbstractEventLoop = loop_instance.run_until_complete(
    ActivityBadgeServices()
)
