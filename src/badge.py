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
from asyncio import ensure_future, Future, sleep as asyncio_sleep, wait
from re import compile, MULTILINE, Pattern
from typing import Any, Union
from datetime import datetime, timedelta

from elements.constants import (
    B64_ACTION_FILENAME,
    BADGE_REGEX_STRUCT_IDENTIFIER,
    Base64Actions,
    BADGE_BASE_MARKDOWN,
    PreferredActivityDisplay,
    PreferredTimeDisplay,
)
from elements.typing import (
    ActivityDictName,
    BadgeStructure,
    Base64,
    HttpsURL,
    ResolvedHTTPResponse,
)
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
            try:
                _match = self._re_pattern.search(_.read(), MULTILINE)
                self._is_badge_identified: bool = (
                    _match.group("badge_identifier") is None
                )

                self.logger.info(  # # PLEASE NOTE THAT BADGE_IDENTIFIER_NAME shouldn't be required as how we handle the condition here. Evaluate the condition...
                    "Badge with identifier (%s) found!."
                    % _match.group(
                        "badge_identifier"
                    )  # todo: Add some container to avoid direct reference.
                    if self.envs["BADGE_IDENTIFIER_NAME"]
                    == _match.group("badge_identifier")
                    else "Badge with identifier (%s) not found! Will attempt to append the badge on the top of the contents of README.md. Please fix this later!"
                    % self.envs["BADGE_IDENTIFIER_NAME"]
                )  # And also discord as well. This assume its the user's first time.

            except IndexError as Err:
                self.logger.warn(
                    "The RegEx can't find any badge with Identifier in README. If you think that this is a bug then please let the developer know."
                )

    async def construct_badge(self) -> None:
        """
        For every possible arguments declared in actions.yml, the output of the badge will change.

        Let the following be the construction recipe for the badge: [![<badge_identifier>](<badge_url>)](redirect_url)

        Where:
            - badge_identifier: Unique Name of the Badge
            - badge_url: The badge URL that is rendered in Markdown (README).
            - redirect_url: The url to redirect when the badge is clicked.

        ! The badge itself should be recognizable by RegEx declared in elements/constants.py:49 (BADGE_REGEX_STRUCT_IDENTIFIER)

        There are two parts that makes up the whole structure:
            - Subject
            - Status

            * These are basically left and right parts of the badge, more of a pill illustration, but I hope you get the point.

        The badge consists of multiple parts, the following is the diminished structure on how we can manipulate it.
            Subject consists of  [Icon > Text (Either UserState or ActivityState) > Foreground (HEX from UserState or ActivityState)]
            Badge consists of [User State or DerivedBaseActivity > Detail > Denoter > Time Elapsed or Remaining > Foreground(HEX from UserState or ActivityState)]] (2)

        ! The way how it represents by order does not mean the handling of parameters are by order!
        * Every User State represents Derived Classes from disocord.BaseActivity.

        # Further Examples: is declared under README.md. (Subsection Activity States)

        Conditions for badge_identifier:
            - Should be similar that is declared under workflows.
            - () and - _ can be invoked and identified by the Regex.
            - Whenever we have one in the README: We can just replace that string and use re.sub then commit and push.
            - If otherwise: we will create a badge and put it on top. Let the user put it somewhere else they like.

        @o: There's no impactful changes even with per condition. Just references.

        Conditions for redirect_url:
            - The output of this would probably be the repository of the special repository or anything else.

        """

        # These variables shouldn't be de-alloc until we finish the whole function, not just from the try-except scope.
        _subject_output: BadgeStructure = BadgeStructure("")
        _status_output: BadgeStructure = BadgeStructure("")
        _preferred_activity: ActivityDictName = ActivityDictName("")
        _is_preferred_exists: bool = False

        try:
            _redirect_url: HttpsURL = (
                self.envs["REDIRECT_TO_URL_ON_CLICK"]
                if self.envs["REDIRECT_TO_URL_ON_CLICK"]
                else "{0}/{0}".format(self.envs["GITHUB_ACTOR"])
            )  # Let's handle this one first before we attempt to do everything thard.

            _presence_ctx: dict[str, Union[int, str]] = self._client_ctx.user[
                "presence"
            ]  # * Append any activity if there's one. We assure that this is dict even with len() == 0.

            if len(_presence_ctx):  # Does _presence_ctx really contains something?

                # If yes, check what activity is it so that we could process other variables by locking into it.
                # This is were we gonna check if preferred activity exist.


                for (
                    each_cls
                ) in (
                    PreferredActivityDisplay
                ):  # We cannot do key to value lookup, iterate through enums instead.
                    if self.envs["PREFERRED_ACTIVITY_TO_DISPLAY"] is each_cls:
                        if (
                            _presence_ctx.get(each_cls.name) is not None
                        ):  # Is activity really exists?
                            _preferred_activity = ActivityDictName(each_cls.name)
                            _is_preferred_exists = True
                            break

                    if (
                        not _is_preferred_exists
                    ):  # If we fail to lookup, perform exporting keys and convert them to list to use the first activity (if there's any).
                        _fallback_activity: list[str] = list(_presence_ctx.keys())

                        # Do _presence_ctx contain more than one? Let's assert that.
                        if not _fallback_activity:
                            self.logger.warn(
                                "There's are no other activities existing, even with the preferred activity! Fallback to Basic Badge Formation."
                            )
                        else:
                            _preferred_activity = ActivityDictName(
                                _fallback_activity[0]
                            )

                self.logger.info(
                    f"Preferred Activity {each_cls.name} %s" % "exists!"
                    if _is_preferred_exists
                    else f"does not exists. Using other activity such as {each_cls}"
                )

            else:
                self.logger.warning(
                    "There's no activities detected by the time it was fetched."
                )

            # Check if we should append User's State instead of Activity State.
            _subject_output = self.envs[
                "%s_STATE"
                % (
                    f"ACTIVITY_{_preferred_activity}"
                    if self.envs["APPEND_STATE_ON_SUBJECT"] and _is_preferred_exists
                    else "BADGE_%s"
                    % self._client_ctx.user["status"]["status"].name.upper()
                )
            ]

            self.logger.debug(f"Output is {_subject_output}")

            return
            # Handle the time.
            if self.envs["TIME_TO_DISPLAY"] is not PreferredTimeDisplay.DISABLED:

                # Handle if the preferred activity exists or otherswise.

                _current_time: datetime = datetime.now()

                # Add funcitonality to consider end.
                # if isinstance(self._client_ctx["presence"][]["timestamps"].get(), type(None)):
                _difference: timedelta = _current_time - datetime.fromtimestamp(
                    int(
                        self._client_ctx["presence"][_preferred_activity]["timestamps"][
                            "start"
                        ]
                    )
                    / 1000
                )
                self.logger.debug(_difference)
                # if self.envs["TIME"]

        except KeyError as Err:  # todo: I don't know what error should I handle here. But I know that there's something that I have to handle here.
            self.logger.error(
                f"Environment Processing has encountered an error. Please let the developer know about the following. | Info: {Err}"
            )
            os._exit(-1)

        self.logger.info(
            "Evaluating Conditons from Optional Extensibility and Customizations..."
        )

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
    # if os.environ.get("INPUT_PREFERRED_ACTIVITY_TO_DISPLAY") in ["CUSTOM_ACTIVITY", "RICH_PRESENCE", "GAME_ACTIVITY"]:
    # pass
    # else:
    # 	self.logger.error("The supplied value of PREFERRED_ACTIVITY_TO_DISPLAY is invalid. Please check the documentation, check your workflow secret/input and try again.")
    # 	os._exit(-7)

    # self.logger.info("Badge Metadata Preparation is done. Waiting for appending Discord's Data.")

    # I need to fiugre out something first.
