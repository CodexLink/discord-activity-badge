"""
Copyright 2021 Janrey "Codexlink" Licas

licensed under the apache license, version 2.0 (the "license");
you may not use this file except in compliance with the license.
you may obtain a copy of the license at

	http://www.apache.org/licenses/license-2.0

unless required by applicable law or agreed to in writing, software
distributed under the license is distributed on an "as is" basis,
without warranties or conditions of any kind, either express or implied.
see the license for the specific language governing permissions and
limitations under the license.
"""

if __name__ == "__main__":
    from elements.exceptions import IsolatedExecNotAllowed

    raise IsolatedExecNotAllowed

import os
from asyncio import ensure_future
from re import Pattern, compile
from typing import Any

from elements.constants import BADGE_REGEX_STRUCT_IDENTIFIER


class BadgeConstructor:
    """
    An async-class module that generate badge over-time.

    """

    # By this point, there are a variety of Activities. We need to select one and avail to resolve from what the user wants.
    # First let's evaluate what user wants to display in their badge.
    # todo: We need a parameter that PREFER_CUSTOM_ACTIVITY_OVER_PRESENCE.

    # First we have to understand that, the way how discord displays the status of user by order.
    # CustomActivity (Custom Status) > Activity (Rich Presence) > Game (Game)
    # The way how Discord.py stores activities: CustomActivity(Custom Status) > Game (Game) > Activity (Rich Presence)

    # We will follow how Discord Client displays it.

    """
		Example:
		Set of Activities:  (<CustomActivity name='I wanna hug and pat teri~' emoji=<PartialEmoji animated=True name='TeriPats' id=???>>,
		<Game name='Honkai Impact 3'>,
		<Activity type=<ActivityType.playing: 0> name='osu!' url=None details=None application_id=??? session_id=None emoji=None>,
		<Activity type=<ActivityType.playing: 0> name='Visual Studio Code' url=None details='Editing client.py: 165:79 (211)' application_id=??? session_id='??? emoji=None>)
	"""

    # todo: Let's push this one on the BadgeGenerator instead.
    # if os.environ.get("INPUT_PREFERRED_ACTIVITY_TO_DISPLAY") in ["ALL_ACTIVITIES", "CUSTOM_ACTIVITY", "RICH_PRESENCE", "GAME_ACTIVITY"]:
    # pass
    # else:
    # 	self.logger.error("The supplied value of PREFERRED_ACTIVITY_TO_DISPLAY is invalid. Please check the documentation, check your workflow secret/input and try again.")
    # 	os._exit(-7)

    async def __ainit__(self) -> None:

        self._re_pattern: Pattern = compile(BADGE_REGEX_STRUCT_IDENTIFIER)
        self.logger.info("RegEx for Badge Identification in README Compiled.")

    async def prepare_badge(self) -> None:

        self.logger.info("Converting README to Markdown File...")

        await self._write_file_from_b64()

        self.logger.info("Checking README for Identification of Badge...")

        self.logger.critical(
            "There was no identifier inside of README.md. Please add one and run this script again."
        )
        pass

    async def _b64_encode(self) -> None:
        pass

    async def _write_file_from_b64(self) -> None:
        pass

    async def append_data_to_badge(self, ctx: object) -> None:
        # I need to fiugre out something first.
        pass

    async def wat(self) -> None:
        pass
