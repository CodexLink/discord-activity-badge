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

# Classifications of constants of any kind. (limiters, choices, etc.) | constants.py
# Version dev.0.06232021


if __name__ == "__main__":
    from exceptions import IsolatedExecNotAllowed

    raise IsolatedExecNotAllowed

else:
    from datetime import timedelta as timeConstraint
    from typing import Any, Final, List
    from enum import Enum, IntEnum

    """
    This is an intentional implementation, I just prefer to keep long strings to another file.
    And let short constants intact so that the context is not out of blue.
    """

    # # Classified Arguments Information
    ARG_CONSTANTS: Final[dict[str, str]] = {  # Cannot evaluate less.
        "ENTRY_PARSER_DESC": "An application that runs under workflow to evaluate User's Discord Activity Presence to Displayable Badge for their README.md.",
        "ENTRY_PARSER_EPILOG": "The use of arguments are intended for debugging purposes only. Please be careful.",
        "HELP_DESC_NO_LOGGING": "Disables logging but does not surpress outputting logs to console, if enabled.",
        "HELP_DESC_DRY_RUN": "Runs the whole script without commiting changes to external involved factors (ie. README.md)",
        "HELP_DESC_NO_ALERT_USR": "Does not alert the user / developer from the possible crashes through Direct Messages (this also invokes the do-not-send logs.)",
        "HELP_DESC_LOG_TO_CONSOLE": "Prints the log output to the console, whenever the case.",
    }

    # # Class Container Metadata
    ARG_PLAIN_CONTAINER_NAME: Final[str] = "ArgsContainer"
    ARG_PLAIN_DOC_INFO: Final[
        str
    ] = "This is a plain class to where the args has been living after being evaluated."

    # # Discord Client Bot Message Context
    DISCORD_DATA_CONTAINER: Final[str] = "DiscUserCtxContainer"
    DISCORD_DATA_CONTAINER_ATTRS: Final[
        dict[str, Any]
    ] = {  # todo: Fill it up later. +  Ref: https://stackoverflow.com/questions/3603502/prevent-creating-new-attributes-outside-init
        "__usr__": {},  # Contains user's information, this excludes the Discord Rich Presence.
        "__guild__": {},  # Contains guild information.
        "__presence__": {},  # Contains user's presence activity.
    }
    DISCORD_ON_READY_MSG: Final[
        str
    ] = "Client (%s) is ready for evaluation of user's activity presence."

    # # Logger Information
    LOGGER_FILENAME: Final[
        str
    ] = "idk.log"  # todo: be dynamic about this. Use Date.
    LOGGER_LOG_LOCATION: Final[str] = "../../" # todo: resolve unresolved class name.
    LOGGER_OUTPUT_FORMAT: Final[str] = "[%(asctime)s] Some Class @ %(filename)s [%(lineno)d] -> %(levelname)s | %(message)s"
    LOGGER_DATETIME_FORMAT: Final[str] = "" # todo.

    # # Logger Code Enumerations

    class LoggerCodeRet(IntEnum):
        # todo: Clean this later.

        NO_RECORDED_RET_CODE = -1
        OP_SUCCESS = 0
        OP_FAILED  = 1

        SET_LEVEL_SUCCESS = 2
        SET_LEVEL_FAILED = 3

        NO_CHILD_REGISTERED = 4

        REFERRED_CHILD_DOES_NOT_EXIST = 8
        INVALID_REFERRED_LEVEL_FUNC = 9

        REFERRED_ATTR_IS_INVALID = 10

        SUPPLIED_INVALID_ELEMENT = 11
        DOES_NOT_CONTAIN_VALUE = 12

        VALID_REGISTERED_CLS = 7
        INVALID_REGISTERED_CLS = 5

        UNREGISTER_SUCCESS = 6
        UNREGISTER_FAILED  = 7

    # # Logger Code Raised Error Messages



    # # Pre-Condition Constraints
    ALLOWABLE_TIME_TO_COMMIT: Final[object] = timeConstraint(
        minutes=30
    )  # todo: Clarify this. This is connected from the workflow recommended refresh rate. Also rate-limits.
