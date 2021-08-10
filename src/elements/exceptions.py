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

from .constants import ExitReturnCodes

if __name__ != "__main__":
    from typing import Final

    # The following inherited `Exception` classes are the only ones retained. Other Exception implementations may take time and thurs, inlined along with the methods instead.

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


else:
    exit(ExitReturnCodes.ILLEGAL_IMPORT_EXIT.value)
