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

from typing import Coroutine


if __name__ == "__main__":
    from elements.exceptions import IsolatedExecNotAllowed

    raise IsolatedExecNotAllowed

else:
    from argparse import ArgumentParser
    from elements.constants import (
        ARG_CONSTANTS,
        ARG_PLAIN_CONTAINER_NAME,
    )
    from asyncio import ensure_future

    class ArgumentResolver:
        """
        A class designed to wrap argparse for better accessibility for other subclasses.
        """

        async def __ainit__(self) -> None:
            """
            An async version of __init__ to be accessed by async-based classes.

            Note:
                (1) This blocking super() instantiates next subclass, which in our case, the class DiscordClientHandler.
                (2) This await is probably fast, but await is still invoked just to make sure, maybe we can miss about ~300ms of time without it being loaded.
            """

            super().__init__()  # * (1)
            self.logger.debug(
                f"Instantiated Class DiscordClientHandler to prepare for long load."
            )

            await ensure_future(self.__load_args())
            self.logger.debug(
                f"Awaited inlined (ensure_future) on self.__load_args() | Assumes done."
            )

            self.logger.info(
                f"ArgumentResolver has done evaluating arguments. Check self.args_container to see evaluated arguments."
            )

        async def __load_args(self) -> None:
            """
            Loads the arguments given by the user or the machine upon running this script, if instructed.
            """

            self.__parser = ArgumentParser(
                description=str(ARG_CONSTANTS["ENTRY_PARSER_DESC"]),
                epilog=str(ARG_CONSTANTS["ENTRY_PARSER_EPILOG"]),
            )

            self.logger.debug(f"ArgumentParser: Instantiated. | {self.__parser}")

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

            try:
                # We create an object for use later by other subclasses right after self.__parser.parse_args().
                self.args_container: object = type(
                    ARG_PLAIN_CONTAINER_NAME, (object,), {}
                )
                self.__parser.parse_args(namespace=self.args_container)

                self.logger.debug(
                    f"ArgumentParser has its arguments evaluated and sent to {self.args_container}."
                )

            # This exception is invoked by ArgumentParser by default. Invoking this exception will ensure that there will be no exceptions shown upon exit.
            except SystemExit:
                self.logger.info(f"ArgumentParser raised SystemExit, exiting now...")
                exit(0)
