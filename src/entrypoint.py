#
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

from venv import create


if __name__ != "__main__":
    from elements.exceptions import EntryImportNotAllowed

    raise EntryImportNotAllowed

else:
    from args import ArgumentResolver
    from typing import Generator, Any, Tuple
    from asyncio import (
        AbstractEventLoop,
        create_task,
        Future,
        gather,
        get_event_loop,
        sleep as asyncio_sleep,
        shield,
        Task,
    )
    from client import DiscordClientHandler
    from dotenv import find_dotenv, load_dotenv
    import os
    from sys import stdout
    import logging
    from typing import Optional

    from elements.exceptions import DotEnvFileNotFound

    from elements.constants import (
        ENV_FILENAME,
        DISCORD_CLIENT_INTENTS,
        RET_DOTENV_NOT_FOUND,
        LOGGER_FILENAME,
        LOGGER_OUTPUT_FORMAT,
        ROOT_LOCATION,
    )

    class ActivityBadgeServices(
        ArgumentResolver,
        DiscordClientHandler,
        # BadgeGenerator
    ):
        """The start of everything. This is the core from initializing the workflow to generating the badge."""

        def __init__(self, **kwargs: dict[Any, Any]) -> None:
            """
            Step 0.1 | Prepare non-async functions to load other assets that will be needed later.
            If function "find_dotenv" raise an error, the script won't run.
            Or else, run Step 0.2.
            """
            try:
                load_dotenv(
                    find_dotenv(
                        filename=ROOT_LOCATION + ENV_FILENAME,
                        raise_error_if_not_found=True,
                    )
                )
            except IOError:
                raise DotEnvFileNotFound(RET_DOTENV_NOT_FOUND)

        async def __preload_subclasses(self) -> Any:
            """
            Step 0.2 | Instantiates all subclasses to prepare the module for the process.

            Notes:
                (1.a) Let's load the logger first to enable backtracking incase if there's anything happened wrong. [If explicitly stated to run based on arguments.]
                (1.b) We migh want to shield this async function to avoid corruption. We don't want a malformed output.
                (2) Await the first super().__init__() which instantiates ArgumentResolver, this is required before we do tasking since we need to evaluate the given arguments.
                (3.a) Instantiate the super().__init__(intents) which belongs to DiscordClientHandler. This is required to load other properties that is required by its methods.
                (3.b) We cannot await this one because discord.__init__ is not a coroutine. And it shouldn't be, which is right.
                (4) And once we load the properties, we can now asynchronously load discord in task.
                (5) There will be another task that is gathered into one so that it is distinguishly different than other await functions. They are quite important under same context.

            Credits:
                (1) https://stackoverflow.com/questions/33128325/how-to-set-class-attribute-with-await-in-init.
                (2) https://stackoverflow.com/questions/9575409/calling-parent-class-init-with-multiple-inheritance-whats-the-right-way/55583282#55583282
            """
            await shield(
                self.__load_logger(
                    level_coverage=logging.DEBUG, log_to_file=False, out_to_console=True
                )
            )  # * (1) [a,b]
            await super().__init__()  # * (2)

            super(ArgumentResolver, self).__init__(
                intents=DISCORD_CLIENT_INTENTS
            )  # * (3) [a,b]

            self.discord_client_task: Task = create_task(
                super(ArgumentResolver, self).start(os.environ.get("DISCORD_TOKEN"))
            )  # * (4)

            self.constraint_checkers: Future[Tuple[Any, None]] = gather(
                self.__requirement_validation(), self.__param_eval()
            )  # * (5)

            await self.constraint_checkers

            self.logger.debug("Done.")

            await self.discord_client_task  # If this is still not yet done then let's await.

        def __await__(self) -> Generator:
            return self.__preload_subclasses().__await__()

        async def __load_logger(
            self,
            level_coverage: Optional[int] = logging.DEBUG,
            log_to_file: Optional[bool] = False,
            out_to_console: Optional[bool] = False,
        ) -> None:
            """
            Step 0.3 | Loads the logger for all associated modules.

            Args:
                level_coverage (Optional[int], optional): Sets the level (and above) to cover it in the logs or in stream. Defaults to logging.DEBUG.
                log_to_file (Optional[bool], optional): Creates a file and logs the data if set to True, or otherwise. Defaults to False.
                out_to_console (Optional[bool], optional): Output the log reports in the console, if enabled. Defaults to False.

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

            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(__LOGGER_LEVEL_COVERAGE)

            if log_to_file:
                file_handler = logging.FileHandler(
                    filename=LOGGER_FILENAME, encoding="utf-8", mode="w"
                )
                file_handler.setFormatter(__LOGGER_HANDLER_FORMATTER)
                self.logger.addHandler(file_handler)

                await asyncio_sleep(0.2)

            if out_to_console:
                console_handler = logging.StreamHandler(stdout)
                console_handler.setFormatter(__LOGGER_HANDLER_FORMATTER)
                self.logger.addHandler(console_handler)

                await asyncio_sleep(0.2)

            if not level_coverage in __levels__:
                self.logger.warning(
                    "Argument level_coverage is invalid from any of the list in __level__. setLevel() will use a default value (logging.DEBUG) instead."
                )

            else:
                self.logger.info(
                    f"Logger Coverage Level was set to {level_coverage}."
                )  # todo: Make it enumerated to show the name.

            self.logger.info("The logger has been loaded.")

        async def __requirement_validation(self) -> Any:
            # Step 0.4a | Checking of parameters before doing anything.
            # 1.1 | Parameter Key Validatation.
            # 1.2 | README Checking Indicators.
            pass

        async def __param_eval(self) -> None:
            # Step 0.4b | Evaluation of Parameters from Discord to Args.
            pass

        # Wrapper of other steps.
        async def __process(self) -> None:
            pass

        # Step 3 | Discord Accessing and Caching of Data.
        def __discord_presence_check(self) -> None:
            # todo: Create a container class about this one.
            pass

        # Step 4 | Badge Generation.
        def __badge_gen(self) -> None:
            # todo: Create a container class about this one.
            pass

        # Step 5 | Submit changes.
        # ! If we can invoke the workflow credentials here. Then we can push this functionality.
        # * Or else, we have to make the steps in the workflow (yaml) to push the changes.
        # def __git_commit(self) -> None:
        #     # todo: Create a Todo about the enums that this function can emit.
        #     pass

        @property
        def current_state(self) -> bool:  # todo: Create a classification here.
            return True  # Placeholder for now.

        def __repr__(self) -> str:
            return f"<Activity Badge Service, State: n/a | Discord User: n/a | Curr. Process: n/a>"

        def __del__(self) -> None:
            pass
            # logging.shutdown()  # todo: Refer to handler.

    if __name__ == "__main__":
        loop_instance: AbstractEventLoop = get_event_loop()
        entry_instance = loop_instance.run_until_complete(ActivityBadgeServices())

        # if entry_instance.current_state:
        #     exit(0)
        # else:
        #     pass # Raise the error and exit it under that error code.
