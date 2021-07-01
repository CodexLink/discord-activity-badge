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

from ast import FormattedValue
from logging import Formatter


if __name__ != "__main__":
    from elements.exceptions import EntryImportNotAllowed

    raise EntryImportNotAllowed

else:
    from args import ArgumentResolver
    from typing import Generator, Any
    from asyncio import AbstractEventLoop, get_event_loop
    from client import DiscordClientHandler
    from dotenv import load_dotenv
    import os
    from sys import stdout
    import logging
    from typing import Optional

    from elements.constants import (
        LOGGER_FILENAME,
        ROOT_LOCATION,
        LOGGER_OUTPUT_FORMAT,
        DISCORD_CLIENT_INTENTS,
    )

    class ActivityBadgeServices(
        ArgumentResolver,
        DiscordClientHandler,
        # BadgeGenerator
    ):
        """The start of everything. This is the core from initializing the workflow to generating the badge."""

        def __init__(self, **kwargs: dict[Any, Any]) -> None:
            load_dotenv(ROOT_LOCATION + ".env")

        async def __preload_subclasses(self) -> Any:
            """Instantiates all subclasses (that inherits by this class, formerly known as Base Class) to prepare the module for the process.

            Notes:
                (1) The first super().__init__() instantiates ArgumentResolver, this is more of, prepare and evaluate arguments, given on launch.
                (2) The second super() instantiates LoggerComponent by moving up to ArgumentResolver as base MRO pattern function searching.
                (3)
                (4)
                As we evaluate the code, the await is invalid because it expects the super() to return None, it isn't.

            Credits:
                (1) https://stackoverflow.com/questions/33128325/how-to-set-class-attribute-with-await-in-init.
                (2) https://stackoverflow.com/questions/9575409/calling-parent-class-init-with-multiple-inheritance-whats-the-right-way/55583282#55583282
            """
            await self.__load_logger(level_coverage=logging.DEBUG, log_to_file=True, out_to_console=True)

            await super().__init__()
            super(ArgumentResolver, self).__init__(intents=DISCORD_CLIENT_INTENTS)

            await super(ArgumentResolver, self).start(os.environ.get("DISCORD_TOKEN"))
            self.logger.debug("Done.")

            # req_args = await super().get_parameter_value("no_logging")
            # print(f"The output of req_args is {req_args}")

        def __await__(self) -> Generator:
            return self.__preload_subclasses().__await__()

        async def __load_logger(  # todo: Not sure with this one.
            self,
            level_coverage: Optional[int] = logging.DEBUG,
            log_to_file: Optional[bool] = False,
            out_to_console: Optional[bool] = False,
        ) -> None:
            """Loads the logger for all associated modules + this module."""

            __levels__ = [
                logging.DEBUG,
                logging.INFO,
                logging.WARNING,
                logging.ERROR,
                logging.CRITICAL,
            ]

            # Expressed Statements
            __LOGGER_HANDLER_FORMATTER: Optional[Formatter] = logging.Formatter(
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

            if out_to_console:
                console_handler = logging.StreamHandler(stdout)
                console_handler.setFormatter(__LOGGER_HANDLER_FORMATTER)
                self.logger.addHandler(console_handler)

            if not level_coverage in __levels__:
                self.logger.warning(
                    "Argument level_coverage is invalid from any of the list in __level__. setLevel() will use a default value (logging.DEBUG) instead."
                )

            else:
                self.logger.info(f"Logger Coverage Level was set to {level_coverage}.") # todo: Make it enumerated to show the name.

            self.logger.info("The logger has been loaded.")

        # Step 1 | Checking of parameters before doing anything.
        def __condition_checks(self) -> Any:
            # 1.1 | Parameter Key Validatation.
            # 1.2 | README Checking Indicators.
            pass

        # Step 2 | Evaluation of Parameters from Discord to Args.
        def __param_eval(self) -> None:
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
