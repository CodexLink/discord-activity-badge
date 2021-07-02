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

# todo: Whenever as possible, do DRY principles here.

from typing import Any, Final

# # Discord Exceptions
class MutualGuildsNotFound(Exception):
    """Cannot find a guild where the bot is residing with the user who requests for presence badge.

    Args:
            Exception (Subclass): Inherits Exception Class.
    """

    pass

class IsolatedExecNotAllowed(Exception):
    """The use of modules under isolation is not allowed; hence, raising this error."""

    def __init__(self) -> None:
        messages: Final[
            str
        ] = "The use of modules without instantiating the entrypoint is not allowed."
        super().__init__(messages)


class EntryImportNotAllowed(Exception):
    """The use of entrypoint for other use is not allowed."""

    def __init__(self) -> None:
        messages: Final[
            str
        ] = "The use of entrypoint for other use (importing to other package) is not allowed."
        super().__init__(messages)


class DotEnvFileNotFound(Exception):
    """An exception that expands the capabilities of exception SystemExit by adding message and the return code + name."""

    def __init__(self, *args) -> None:
        messages: Final[
            str
        ] = f"Error Code: {args[0]=} | Dotenv File cannot be found. Please check your specified path or the name of the file and try again."

        super().__init__(messages)
