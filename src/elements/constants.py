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
    from .exceptions import IsolatedExecNotAllowed

    raise IsolatedExecNotAllowed

from datetime import datetime
from enum import Enum, IntEnum, auto, unique
from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING
from time import strftime
from typing import Any, Final, TypedDict, Union

from discord import Intents, Status

from .typing import BadgeElements, BadgeStructure, ColorHEX, HttpsURL, RegExp

# # Badge Generator Constants
BADGE_BASE_URL: Final[HttpsURL] = HttpsURL("https://badgen.net/badge/")
BADGE_REDIRECT_BASE_DOMAIN: Final[HttpsURL] = HttpsURL("https://github.com/")
BADGE_NO_COLOR_DEFAULT: Final[ColorHEX] = ColorHEX("#434343")
BADGE_ICON: Final[BadgeElements] = BadgeElements("discord")
BADGE_BASE_SUBJECT: Final[BadgeElements] = BadgeElements("Discord User")

BADGE_BASE_MARKDOWN: BadgeStructure = BadgeStructure(
    "[![{0}]({1})]({2})"
)  # todo: Document this one later.

BADGE_REGEX_STRUCT_IDENTIFIER: Final[RegExp] = RegExp(
    r"(?P<Delimiter>\[\!\[)(?P<badge_identifier>([a-zA-Z0-9_()-]+(\s|\b)){1,6})\]\((?P<badge_url>https://[a-z]+.[a-z]{2,4})/(?P<entrypoint>\w+)/(?P<subject_badge>[^...]+\b)/(?P<status_badge>[^?]+)\?(?P<params>[^)]+)\)\]\((?P<redirect_url>https://[a-z]+.[a-z]{2,4}/[^)]+)\)"
)

# # Base64 Actions and Related Classiications
@unique
class Base64Actions(IntEnum):
    DECODE_B64_TO_BUFFER = auto()
    ENCODE_BUFFER_TO_B64 = auto()


B64_ACTION_FILENAME: str = "._temp"

# # Classified Arguments Information
ARG_CONSTANTS: Final[dict[str, str]] = {
    "ENTRY_PARSER_DESC": "An application that runs under workflow to evaluate User's Discord Activity Presence to Displayable Badge for their README.md.",
    "ENTRY_PARSER_EPILOG": "The use of arguments are intended for debugging purposes only. Please be careful.",
    "HELP_DESC_DRY_RUN": "Runs the whole script without commiting changes to external involved factors (ie. README.md)",
    "HELP_DESC_LOG_TO_CONSOLE": "Prints the log output to the console, whenever the case.",
    "HELP_DESC_NO_ALERT_USR": "Does not alert the user / developer from the possible crashes through Direct Messages (this also invokes the do-not-send logs.)",
    "HELP_DESC_NO_LOG_TO_FILE": "Disables logging to file but does not surpress outputting logs to console, if specified.",
    "HELP_DESC_RUNNING_LOCALLY": "Allows the script from loading .env. This can raise or terminate if '.env' cannot be found.",
    "HELP_DESC_VERBOSE_CLIENT": "Allows Discord Client API to log. This is useful to check if Discord.py is doing something while the log is silent.",
}

# # Constraints
_date_on_exec: datetime = datetime.now()
_eval_date_on_exec: str = _date_on_exec.strftime("%m/%d/%y — %I:%M:%S %p")
MAXIMUM_RUNTIME_SECONDS = 10

# # Enumerations
@unique
class ContextOnSubject(IntEnum):
    CONTEXT_DISABLED = auto()
    DETAILS = auto()
    STATE = auto()

class ExitReturnCodes(IntEnum): # todo: Add exception that can weak refer to EXIT_SUCCESS despite different return code.
    EXCEPTION_EXIT = -1
    EXIT_HELP = 0
    EXIT_SUCCESS = 0

@unique
class GithubRunnerActions(IntEnum):
    FETCH_README = auto()
    COMMIT_CHANGES = auto()


@unique
class LoggerLevelCoverage(IntEnum):
    DEBUG = DEBUG
    INFO = INFO
    WARNING = WARNING
    ERROR = ERROR
    CRITICAL = CRITICAL


@unique
class PreferredActivityDisplay(IntEnum):
    CUSTOM_ACTIVITY = auto()
    GAME_ACTIVITY = auto()
    RICH_PRESENCE = auto()
    STREAM_ACTIVITY = auto()
    UNSPECIFIED_ACTIVITY = auto()


@unique
class PreferredTimeDisplay(IntEnum):
    TIME_DISABLED = auto()
    HOURS = auto()
    HOURS_MINUTES = auto()
    MINUTES = auto()
    SECONDS = auto()


@unique
class ResponseTypes(IntEnum):
    RESPONSE = 0
    RESPONSE_STATUS = 1
    IS_OKAY = 2


"""
    # Map Structure
    The following constants is a mapped dictionary structure. It will be used to evaluate environment variable's values
    and serialize as they respect the `expected_type` per fields. A `fallback_value` will be used if a certain function fails
    to serialize a certain value. Keep in mind that fallback is supported for optional inputs only! Required inputs will error
    if they fail to meet the expected type.
"""

ENV_STRUCT_CONSTRAINTS: Final[
    dict[str, Any]
] = {  # ! Check /action.yml for more information.
    # # Github Actions Environmental Variables
    "GITHUB_API_URL": {
        "expected_type": str,
        "fallback_value": None,
        "is_required": True,
    },
    "GITHUB_ACTOR": {
        "expected_type": str,
        "fallback_value": None,
        "is_required": True,
    },
    # # Required Parameters
    "INPUT_BADGE_IDENTIFIER_NAME": {
        "expected_type": str,
        "fallback_value": "(Script) Discord Activity Badge",
        "is_required": False,
    },
    "INPUT_COMMIT_MESSAGE": {
        "expected_type": str,
        "fallback_value": f"Discord Activity Badge Updated as of {_eval_date_on_exec}",
        "is_required": False,
    },
    "INPUT_DISCORD_BOT_TOKEN": {
        "expected_type": str,
        "fallback_value": None,
        "is_required": True,
    },
    "INPUT_DISCORD_USER_ID": {
        "expected_type": int,
        "fallback_value": None,
        "is_required": True,
    },
    "INPUT_PROFILE_REPOSITORY": {
        "expected_type": str,
        "fallback_value": None,
        "is_required": False,
    },
    "INPUT_URL_TO_REDIRECT_ON_CLICK": {
        "expected_type": str,
        "fallback_value": None,
        "is_required": False,
    },
    "INPUT_WORKFLOW_TOKEN": {
        "expected_type": str,
        "fallback_value": None,
        "is_required": True,
    },
    # # Optional Parameters — Colors and Intentions.
    "INPUT_CUSTOM_ACTIVITY_STRING": {
        "expected_type": str,
        "fallback_value": None,
        "is_required": False,
    },
    "INPUT_GAME_ACTIVITY_STRING": {
        "expected_type": str,
        "fallback_value": "Playing Game",
        "is_required": False,
    },
    "INPUT_RICH_PRESENCE_STRING": {
        "expected_type": str,
        "fallback_value": "Currently Playing",
        "is_required": False,
    },
    "INPUT_STREAM_ACTIVITY_STRING": {
        "expected_type": str,
        "fallback_value": "Currently Streaming",
        "is_required": False,
    },
    "INPUT_UNSPECIFIED_ACTIVITY_STRING": {
        "expected_type": str,
        "fallback_value": "???",  # todo: This.
        "is_required": False,
    },
    "INPUT_ONLINE_STATUS_STRING": {
        "expected_type": str,
        "fallback_value": "Online",
        "is_required": False,
    },
    "INPUT_IDLE_STATUS_STRING": {
        "expected_type": str,
        "fallback_value": "Idle",
        "is_required": False,
    },
    "INPUT_DND_STATUS_STRING": {
        "expected_type": str,
        "fallback_value": "Do-Not-Disturb",
        "is_required": False,
    },
    "INPUT_OFFLINE_STATUS_STRING": {
        "expected_type": str,
        "fallback_value": "Offline",
        "is_required": False,
    },
    "INPUT_CUSTOM_ACTIVITY_COLOR": {
        "expected_type": ColorHEX,
        "fallback_value": "#c70094",
        "is_required": False,
    },
    "INPUT_GAME_ACTIVITY_COLOR": {
        "expected_type": ColorHEX,
        "fallback_value": "#00cd90",
        "is_required": False,
    },
    "INPUT_RICH_PRESENCE_COLOR": {
        "expected_type": ColorHEX,
        "fallback_value": "#df1473",
        "is_required": False,
    },
    "INPUT_STREAM_ACTIVITY_COLOR": {
        "expected_type": ColorHEX,
        "fallback_value": "#4d14df",
        "is_required": False,
    },
    "INPUT_UNSPECIFIED_ACTIVITY_COLOR": {
        "expected_type": ColorHEX,
        "fallback_value": "???",  # todo: This.
        "is_required": False,
    },
    "INPUT_ONLINE_STATUS_COLOR": {
        "expected_type": ColorHEX,
        "fallback_value": "#61d800",
        "is_required": False,
    },
    "INPUT_IDLE_STATUS_COLOR": {
        "expected_type": ColorHEX,
        "fallback_value": "#edca00",
        "is_required": False,
    },
    "INPUT_DND_STATUS_COLOR": {
        "expected_type": ColorHEX,
        "fallback_value": "#fc4409",
        "is_required": False,
    },
    "INPUT_OFFLINE_STATUS_COLOR": {
        "expected_type": ColorHEX,
        "fallback_value": "#545454",
        "is_required": False,
    },
    "INPUT_STATIC_SUBJECT_STRING": {
        "expected_type": str,
        "fallback_value": None,
        "is_required": False,
    },
    # # Optional Parameters — Context
    "INPUT_TIME_DISPLAY_SHORTHAND": {
        "expected_type": bool,
        "fallback_value": False,
        "is_required": False,
    },
    "INPUT_PREFERRED_PRESENCE_CONTEXT": {
        "expected_type": ContextOnSubject,
        "fallback_value": ContextOnSubject.DETAILS,
        "is_required": False,
    },
    "INPUT_TIME_DISPLAY_OUTPUT": {
        "expected_type": PreferredTimeDisplay,
        "fallback_value": PreferredTimeDisplay.TIME_DISABLED,
        "is_required": False,
    },
    "INPUT_TIME_DISPLAY_ELAPSED_OVERRIDE_STRING": {
        "expected_type": str,
        "fallback_value": "elapsed.",
        "is_required": False,
    },
    "INPUT_TIME_DISPLAY_REMAINING_OVERRIDE_STRING": {
        "expected_type": str,
        "fallback_value": "remaining.",
        "is_required": False,
    },
    # # Optional Parameters — Preferences
    "INPUT_PREFERRED_ACTIVITY_TO_DISPLAY": {
        "expected_type": PreferredActivityDisplay,
        "fallback_value": PreferredActivityDisplay.RICH_PRESENCE,
        "is_required": False,
    },
    "INPUT_SHIFT_STATUS_ACTIVITY_COLORS": {
        "expected_type": bool,
        "fallback_value": False,
        "is_required": False,
    },
    "INPUT_STATUS_CONTEXT_SEPERATOR": {
        "expected_type": str,
        "fallback_value": None,
        "is_required": False,
    },  # ! Bug, cannot process the variable and turns to None whenver there's no fallback_value and there's a value inside of the .env.
    # # Development Parameters
    "INPUT_IS_DRY_RUN": {
        "expected_type": bool,
        "fallback_value": False,
        "is_required": False,
    },
}

# # Discord User Client Structure


class DISCORD_USER_STRUCT(TypedDict):
    id: int
    name: str
    discriminator: str  # I don't know why it was declared as `str` when its 4-digit which is `int`.
    statuses: dict[str, Union[Enum, Status, str]]
    activities: dict[str, Any]  # To many elements to cover.


BLUEPRINT_INIT_VALUES: DISCORD_USER_STRUCT = {
    "id": 0,
    "name": "",
    "discriminator": "",
    "statuses": {},
    "activities": {},
}


# # Discord Client Intents
DISCORD_CLIENT_INTENTS: Intents = Intents.none()
DISCORD_CLIENT_INTENTS.guilds = True
DISCORD_CLIENT_INTENTS.members = True
DISCORD_CLIENT_INTENTS.presences = True

# # Identification of Return Codes
RET_DOTENV_NOT_FOUND: Final[int] = -1

# # Message of Return Codes
# ???

# # Logger Information
ROOT_LOCATION: Final[str] = "../"
ENV_FILENAME: Final[str] = ".env"
LOGGER_FILENAME: Final[str] = (
    strftime("%m%d%Y-%H%M-") + "discord-activity-badge.log"
)
LOGGER_OUTPUT_FORMAT: Final[
    str
] = "[%(relativeCreated)d ms, %(levelname)s\t]\tat %(module)s.py:%(lineno)d -> %(message)s"


# # Time Constants
TIME_STRINGS: list[str] = ["hours", "minutes"]
