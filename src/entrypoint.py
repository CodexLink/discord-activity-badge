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

if __name__ != "__main__":
    from elements.exceptions import EntryImportNotAllowed

    raise EntryImportNotAllowed

else:
    from utils import ArgumentResolver, LoggerComponent
    from typing import Any
    from typing import Generator, Any
    from asyncio import AbstractEventLoop, get_event_loop
    from modules import DiscordClientHandler  # For binding discord later.
    from dotenv import load_dotenv as LOAD_ENV

    class ActivityBadgeServices(
        ArgumentResolver, LoggerComponent, #DiscordClientHandler,# BadgeGenerator
    ):
        """The start of everything. This is the core from initializing the workflow to generating the badge."""

        def __init__(self, **kwargs: dict[Any, Any]) -> None:
            return None

        async def __preload_subclasses(self) -> Any:
            """Instantiates all subclasses (that inherits by this class, formerly known as Base Class) to prepare the module for the process.

            Notes:
                (1) The first super().__init__() instantiates ArgumentResolver, this is more of, prepare and evaluate arguments, given on launch.
                (2) The second super() instantiates LoggerComponent by moving up to ArgumentResolver as base MRO pattern function searching.
                As we evaluate the code, the await is invalid because it expects the super() to return None, it isn't.

            Credits:
                (1) https://stackoverflow.com/questions/33128325/how-to-set-class-attribute-with-await-in-init.
                (2) https://stackoverflow.com/questions/9575409/calling-parent-class-init-with-multiple-inheritance-whats-the-right-way/55583282#55583282
            """

            await super().__init__()
            await super(ArgumentResolver, self).__init__()


            print(self.__class__.__mro__)

            exit(0)
            # Register those classes in the logger.
            # await super(ArgumentResolver, self). register()

            # Once we are d
            # req_args = await super().get_parameter_value("no_logging")

            # print(f"The output of req_args is {req_args}")

        def __await__(self) -> Generator:
            return self.__preload_subclasses().__await__()

        def __preload(self) -> None:
            # We assume that anything that parameters that we received is evaluated by our InconstantArguments Subclass.
            print()

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
        # def __git_commit(self) -> None:
        #     # todo: Create a Todo about the enums that this function can emit.
        #     pass

        @property
        def current_state(self) -> bool:  # todo: Create a classification here.
            return True  # Placeholder for now.

        def __repr__(self) -> str:
            return f"<Activity Badge Service, State: n/a | Discord User: n/a | Curr. Process: n/a>"

    if __name__ == "__main__":
        LOAD_ENV(".env")
        loop_instance: AbstractEventLoop = get_event_loop()

        entry_instance = loop_instance.run_until_complete(ActivityBadgeServices())
        # # entry_instance = ActivityBadgeServices()

        # if entry_instance.current_state:

        #     exit(0)
        # else:
        #     pass # Raise the error and exit it under that error code.
