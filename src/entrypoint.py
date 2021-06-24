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
# Insert the module here.

from multiprocessing import Condition
from typing import Literal
import asyncio
from modules import DiscordClientHandler


if __name__ != "__main__":
    from elements.exceptions import EntryImportNotAllowed
    raise EntryImportNotAllowed

else:
    from utils import InconstantArguments
    from typing import Any

    class ActivityBadgeServices(InconstantArguments, DiscordClientHandler):
        """ The start of everything. This is the core from initializing the workflow to generating the badge. """

        # Step 0 | Ensure that we fill up properties of certain things only. /???
        def __init__(self, **kwargs: dict[Any, Any]) -> None:

            super(ActivityBadgeServices, self).__init__(**kwargs) # This was intended for the subclass. Ensure that this one receives the argv.


            self.evaluated_args = super().return_args
            print(self.evaluated_args)
            print(dir(self.evaluated_args))
            print(super().loaded_by_who)
            exit(0)

            self.__condition_checks() # Step 1 | Check anything before we start. Assume that everything is clean.


        def __initiate_proc(self) -> None:
            pass

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
        def __git_commit(self) -> None:
            # todo: Create a Todo about the enums that this function can emit.
            pass

        @property
        def current_state(self) -> bool: # todo: Create a classification here.
            return True # Placeholder for now.

        def __repr__(self) -> str:
            return f"<Activity Badge Service, State: n/a | Discord User: n/a>"

    if __name__ == "__main__":
        entry_instance = ActivityBadgeServices()

        if entry_instance.current_state:

            exit(0)
        else:
            pass # Raise the error and exit it under that error code.