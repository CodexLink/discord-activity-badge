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

import asyncio
import os
from asyncio import ensure_future, Future, sleep as asyncio_sleep, wait
from re import compile, MULTILINE, Pattern
from typing import Any, Union

from elements.constants import (
    B64_ACTION_FILENAME,
    BADGE_REGEX_STRUCT_IDENTIFIER,
    Base64Actions,
    BADGE_BASE_MARKDOWN,
)
from elements.typing import BadgeStructure, Base64, ResolvedHTTPResponse
from base64 import b64decode, b64encode


class BadgeConstructor:
    """
    An async-class module that generate badge over-time.
    """

    async def _handle_b64(
        self, action: Base64Actions, base64_str: Base64
    ) -> Union[Any, None]:  # To be annotated later.
        if action is Base64Actions.DECODE_B64_TO_FILE:
            try:

                _out: bytes = b64decode(base64_str)

                with open(B64_ACTION_FILENAME, "w", errors="ignore") as _:
                    _.write(_out.decode("ascii", errors="replace"))
                    await asyncio_sleep(0.001)

                self.logger.debug(
                    "Convertion from Base64 to README Markdown Format is done!"
                )

            except Exception as Err:
                self.logger.error(
                    f"Something happened while writing the file from Base64. Exceptions are not documented by this part. Maybe in the future. | More Info: {Err}"
                )

    async def check_badge_identifier(self, readme_ctx: Base64) -> None:
        self.logger.info("Converting README to Markdown File...")
        _readme_decode: Future = ensure_future(
            self._handle_b64(Base64Actions.DECODE_B64_TO_FILE, readme_ctx)
        )

        self._re_pattern: Pattern = compile(BADGE_REGEX_STRUCT_IDENTIFIER)
        self.logger.info("RegEx for Badge Identification in README Compiled.")

        await wait([_readme_decode])
        self.logger.info("Identifying the badge inside README.md...")

        with open(B64_ACTION_FILENAME, "r") as _:
            _match = self._re_pattern.search(_.read(), MULTILINE)

            self._is_badge_identified: bool = _match.group("badge_identifier") is None

            self.logger.info(
                "Badge with identifier (%s) found!."
                % self.envs["BADGE_IDENTIFIER_NAME"]
                if self.envs["BADGE_IDENTIFIER_NAME"] == _match.group("Identifier")
                else "Badge with identifier (%s) not found! Will attempt to append the badge on the top of the contents of README.md. Please fix this later!"
                % self.envs["BADGE_IDENTIFIER_NAME"]
            )  # And also discord as well. This assume its the user's first time.

    async def evaluate_badge_conditions(self) -> None:
        """
            For every possible arguments declared in actions.yml, the output of the badge will change.

            Let the following be the construction recipe for the badge: [![<badge_identifier>](<badge_url>)](redirect_url)

            Where:
                - badge_identifier: Unique Name of the Badge
                - badge_url: The badge URL that is rendered in Markdown (README).
                - redirect_url: The url to redirect when the badge is clicked.

            ! The badge itself should be recognized by RegEx declared in elements/constants.py:49 (BADGE_REGEX_STRUCT_IDENTIFIER)

            As for how it looks, Level 1:
                Icon > Badge [Name, Foreground] (1) > Status [Name, Foreground] (2)

            Deeper Structure with involvement of Discord Data, Level 2:
                Icon > Badge [Name, Foreground] (1) > Prefix + (User State (State if Activity does not exist) or Custom State) + Denoter + Time Elapsed + Postfix [Name, Foreground] (2)

            * Every User State represents CustomActivity.

            Further Examples:
                - Discord Activity, Currently Offline ()
                - Discord Activity, Playing Honkai Impact 3, 6 hours elapsed ()
                - Discord Activity, Playing Honkai Impact 3, 6h 9m elapsed ()
                - Discord Activity, Doing something for fun. (Currently Online) ()
                - Status, Visual Studio Code, Editing entrypoint.py:159, 6 hours elapsed
                - Status, Visual Studio Code, Debugging for 6 hours (this is a pre and post modified)
                - Visual Studio Code, Editing entrypoint.py:159, 6 hours elapsed
                - Listening to, Some Music in Spotify
                - Playing, Honkai Impact 3, 69 minutes remain.
                - Streaming, in Twitch (this wasnt supported yet but will try after post-development)
                - Online, There is no end to learning.


            At this point, I came to realize that there are lots of configurations that I have to invoke.

            Conditions for badge_identifier:
                - Should be similar that is declared under workflows.
                - () and - _ can be invoked and identified by the Regex.
                - Whenever we have one in the README: We can just replace that string and use re.sub then commit and push.
                - If otherwise: we will create a badge and put it on top. Let the user put it somewhere else they like.

            @o: There's no impactful changes per condition. Just references.

            Conditions for badge_url:
                For this group, this is where we have to put all arguments managed in one place.
                ! First prioritize `Extensibility and Customization` section, .
                - As w

            Conditions for redirect_url:
                - The output of this would probably be the repository of the special repository or anything else. todo: Add arguments [REDIRECT_ON_BADGE_CLICK]

        """
        _sketch_badge: BadgeStructure = BadgeStructure("")


        self.logger.info(
            "Evaluating Conditons from Optional Extensibility and Customizations..."
        )

        if self.envs["APPEND_DETAIL_PRESENCE"]:
            # self.env
            pass

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

    # self.logger.info("Badge Metadata Preparation is done. Waiting for appending Discord's Data.")

    # I need to fiugre out something first.

    async def append_data_to_badge(self, ctx: object) -> None:
        pass
