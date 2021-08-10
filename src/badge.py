"""
Copyright 2021 Janrey "CodexLink" Licas

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

from asyncio import Future, Task, create_task, wait
from base64 import b64decode, b64encode
from datetime import datetime, timedelta
from logging import Logger
from os import _exit as terminate
from re import Match, Pattern, compile
from typing import Any, Optional, Union
from urllib.parse import quote

from elements.constants import (
    BADGE_BASE_MARKDOWN,
    BADGE_BASE_SUBJECT,
    BADGE_BASE_URL,
    BADGE_ICON,
    BADGE_NO_COLOR_DEFAULT,
    BADGE_REDIRECT_BASE_DOMAIN,
    BADGE_REGEX_STRUCT_IDENTIFIER,
    DISCORD_USER_STRUCT,
    TIME_STRINGS,
    Base64Actions,
    ContextOnSubject,
    ExitReturnCodes,
    PreferredActivityDisplay,
    PreferredTimeDisplay,
)
from elements.typing import (
    ActivityDictName,
    BadgeElements,
    BadgeStructure,
    Base64Bytes,
    Base64String,
    ColorHEX,
    HttpsURL,
    READMEContent,
)


class BadgeConstructor:
    # * The following variables are declared for weak reference since there's no hint-typing inheritance.

    badge_task: Task
    discord_client_task: Task
    envs: Any
    logger: Logger
    user_ctx: DISCORD_USER_STRUCT

    """
    A child class that contains the logic for badge construction with respect to a variety of options for displaying a badge.
    This class also handles decoding and encoding of Base64 README since its the one who modifies the badge.
    """

    async def _handle_b64(
        self,
        action: Base64Actions,
        ctx_inout: Union[Base64String, READMEContent],
    ) -> Union[Base64Bytes, READMEContent]:
        """
        A private child class that handles README content by decoding and encoding it, to be stored in the memory buffer.

        Args:
            action (Base64Actions): The action that this method will perform. Choices are DECODE_B64_TO_BUFFER and ENCODE_BUFFER_TO_B64.
            ctx_inout (READMEContent): A variable that hold the data from decoding to encoding.

        Returns:
            Union[Base64Bytes, READMEContent]: Each action returns different type of data, those can be Base64String for decoding and READMEContent (str) encoding, respectively.
        """

        if ctx_inout is Base64String(str(ctx_inout)):
            if action is Base64Actions.DECODE_B64_TO_BUFFER:
                self.logger.info(
                    "Conversion from Base64 (String) to Readable README Markdown Format is done and is loaded into the memory!"
                )

                return READMEContent(str(b64decode(ctx_inout), encoding="utf-8"))

            elif action is Base64Actions.ENCODE_BUFFER_TO_B64:
                self.logger.info(
                    "Conversion from README Readable Raw Content to a Base64 (Bytes) is done and is loaded into the variable for committing changes!"
                )
                return Base64Bytes(b64encode(bytes(str(ctx_inout), encoding="utf-8")))

            else:
                self.logger.critical(
                    f"Passed `action` parameter is not a {Base64Actions}! Please contact the developer if this issue occured in Online Runner."
                )
                terminate(ExitReturnCodes.ILLEGAL_CONDITION_EXIT)
        else:
            self.logger.error(
                f"The given value in `ctx_inout` parameter is not a {Base64String.__name__}! Please contact the developer about this issue."
            )
            terminate(ExitReturnCodes.ILLEGAL_CONDITION_EXIT)

    async def check_and_update_badge(self, readme_ctx: Base64String) -> Base64Bytes:
        """
        A method that checks the badge inside of README and updates it if possible.

        Args:
            readme_ctx (Base64String): The content of README to be decoded, this expects a Base64 in string form, not in bytes!

        Returns:
            Base64Bytes: This returns a Base64 in bytes since the changes has been reflected and is encoded by `_handle_b64()`
        """

        self.logger.info("Converting README to a Readable Format...")
        readme_decode: Future = create_task(
            self._handle_b64(Base64Actions.DECODE_B64_TO_BUFFER, readme_ctx),
            name="READMEContents_Decode",
        )

        self._re_pattern: Pattern = compile(BADGE_REGEX_STRUCT_IDENTIFIER)
        self.logger.debug(
            f"RegularExpression for Badge Identification in README was compiled successfully. | Pattern: {self._re_pattern}"
        )

        await wait([readme_decode])

        try:
            self.logger.info("Attempting to identify the badge inside README...")
            is_matched: bool = False

            while not is_matched:
                line_ctx: READMEContent = READMEContent(readme_decode.result())
                match: Optional[Match[Any]] = self._re_pattern.search(line_ctx)

                self.logger.debug(
                    f"re.Search Result: {match}"
                )  # todo: Check if duplicating the badge would affect the other badge as well. This should be only one-to-one.

                if match:
                    is_matched = True
                    identifier_name: str = match.group("badge_identifier")
                    is_badge_identified: bool = (
                        identifier_name == self.envs["BADGE_IDENTIFIER_NAME"]
                    )

                    self.logger.info(
                        (
                            f"Badge with Identifier {identifier_name} found! Substituting the old badge."
                        )
                        if self.envs["BADGE_IDENTIFIER_NAME"] == identifier_name
                        else "Badge with Identifier (%s) not found! New badge will append on the top of the contents of README.md. Please arrange/move the badge once changes has been pushed!"
                        % self.envs["BADGE_IDENTIFIER_NAME"]
                    )

                    self.logger.info(
                        "Awaiting for the badge construction task to finish..."
                    )
                    await wait([self.badge_task])

                    constructed_badge: BadgeStructure = self.badge_task.result()

                    line_ctx = READMEContent(
                        line_ctx.replace(match.group(0), constructed_badge)
                        if is_badge_identified
                        else f"{constructed_badge}\n\n{line_ctx}"
                    )
                    self.logger.debug(f"README Contents with Changes Reflected!")
                    break

        except IndexError as e:
            self.logger.warn(
                f"The RegEx can't find any badge with Identifier in README. If you think that this is a bug then please let the developer know. | Info: {e} at line {e.__traceback__.tb_lineno}"  # type: ignore
            )

        return await self._handle_b64(Base64Actions.ENCODE_BUFFER_TO_B64, line_ctx)  # type: ignore # Will check this one in the future since I can't explicitly invoke or typecast NewType -> Base64Bytes.

    async def construct_badge(self) -> BadgeStructure:
        """
        This method holds the logic for constructing the badge based on the state and the activity of the user.

        Notes:
        For every possible arguments declared in actions.yml, the output of the badge will change.
        Let the following be the construction recipe for the badge: [![<badge_identifier>](<badge_url>)](redirect_url)

        Where:
            - badge_identifier: Unique Name of the Badge
            - badge_url: The badge URL that is rendered in Markdown (README).
            - redirect_url: The url to redirect when the badge is clicked.

        ! The badge itself should be recognizable by RegEx declared in elements/constants.py (BADGE_REGEX_STRUCT_IDENTIFIER)

        There are two parts that makes up the whole structure:
            - Subject
            - Status

            * These are basically left and right parts of the badge, more of a pill illustration, but I hope you get the point.

        The badge consists of multiple parts, the following is the diminished structure on how we can manipulate it.

            - Subject consists of  [Icon > Text (Either UserState or ActivityState) > Foreground (HEX from UserState or ActivityState)]
            - Badge consists of [User State or DerivedBaseActivity > Detail > Denoter > Time Elapsed or Remaining > Foreground(HEX from UserState or ActivityState)]] (2)

        ! The way how it represents by order does not mean the handling of parameters are by order!
        * Every user state represents Derived Classes from disocord.BaseActivity.

        # Further Examples: is declared under README.md. (Subsection Activity States)

        Conditions for badge_identifier:
            - Should be similar that is declared under workflows.
            - () and - _ can be invoked and identified by the Regex.
            - Whenever we have one in the README: We can just replace that string and use re.sub then commit and push.
            - If otherwise: we will create a badge and put it on top. Let the user put it somewhere else they like.

        Conditions for redirect_url:
            - The output of this would probably be the repository of the special repository or anything else.

        """

        # * These variables shouldn't be de-alloc'd until we finish the whole method, not just from the try-except scope.
        subject_output: Union[BadgeStructure, BadgeElements] = BadgeStructure("")
        status_output: Union[BadgeStructure, BadgeElements] = BadgeStructure("")
        picked_activity: ActivityDictName = ActivityDictName(
            ""
        )  # This inherits to preferred_activity but also used when the preferred_activity does not exist.
        is_preferred_exists: bool = False  # This boolean contains true whenever the user's choice of activity to display exists.

        try:
            redirect_url: HttpsURL = BADGE_REDIRECT_BASE_DOMAIN + (
                self.envs["URL_TO_REDIRECT_ON_CLICK"]
                if self.envs["URL_TO_REDIRECT_ON_CLICK"]
                else "{0}/{0}".format(self.envs["GITHUB_ACTOR"])
            )  # Let's handle the redirect url while we wait for Discord Client Task to finish.

            self.logger.info(
                "Other non-important elements loaded, waiting for the Discord Client Task to finish before continuing..."
            )
            await wait([self.discord_client_task])
            self.logger.info("Discord Client Task is done. Processing the badge...")

            presence_ctx: dict[str, Any] = self.user_ctx[
                "activities"
            ]  # * Append any activities here, if there's one. We assert that this variable will represent as dict even when len() is equal to 0.

            contains_activities: bool = bool(
                len(presence_ctx)
            )  # To prevent other part of the code to call the method for bool evaluation, lets point to this variable for reference.

            if contains_activities:  # Does presence_ctx contains something?

                # If that's the case, then check for `PREFERRED_ACTIVITY_TO_DISPLAY` inside presence_ctx (dict).

                # Since we cannot do key-to-value lookup, let's iterate through `Enums` instead.
                for each_cls in PreferredActivityDisplay:
                    if self.envs["PREFERRED_ACTIVITY_TO_DISPLAY"] is each_cls:
                        if presence_ctx.get(each_cls.name) is not None:
                            picked_activity = ActivityDictName(each_cls.name)
                            is_preferred_exists = True
                            break

                # If we fail to lookup the preferred activity, then perform exporting keys and convert them to a list to use the first activity (if there's any).
                if not is_preferred_exists:
                    picked_activity = ActivityDictName(list(presence_ctx.keys())[0])

                self.logger.info(
                    f"Preferred Activity %s %s"
                    % (
                        self.envs["PREFERRED_ACTIVITY_TO_DISPLAY"],
                        "exists!"
                        if is_preferred_exists
                        else f"does not exists. Using other activity such as {picked_activity}.",
                    )
                )

            else:
                self.logger.warning(
                    "There's no activity detected by the time it was fetched!"
                )

            # # Badge Construction
            """
            ! Keep in mind that every string manipulation is inlined and that's because I don't want to make things longer.
            I hope the formatter compensate this.
            """

            # This is a component of subject_output. Check if we should append User's State instead of Activity State in the Subject.
            state_string = "%s_STRING" % (
                picked_activity
                if len(picked_activity)
                else "%s_STATUS" % self.user_ctx["statuses"]["status"].name.upper()
            )

            # ! CLARFIY THIS CONDITION, Add Static Subject String. If that is included, disabled this condition.
            # Are there an no activity present and STATIC_SUBJECT_STRING is empty? Then use `BADGE_BASE_SUBJECT`.
            # Only if, STATIC_SUBJECT_STRING is not empty, otherwise, use the string concatenation performed in variable `state_string`.
            subject_output = (
                BADGE_BASE_SUBJECT
                if not contains_activities
                and self.envs["STATIC_SUBJECT_STRING"] is None
                else (
                    self.envs[
                        state_string
                        if self.envs["STATIC_SUBJECT_STRING"] is None
                        else "STATIC_SUBJECT_STRING"
                    ]
                )
            )

            # This part is where do we need to embed the state under Subject or Status.
            # There are lot more conditions to consider to this point.
            """
            If there's no presence ctx and there's not
            """

            # When dealing with seperators, sometiemes we have to do some management for dealing with spaces.
            # Display the default if `STATUS_CONTEXT_SEPERATOR` is empty, otherwise, add spacing for both ends along with the custom seperator.
            seperator: BadgeElements = BadgeElements(
                (
                    ", "
                    if self.envs["STATUS_CONTEXT_SEPERATOR"] is None
                    else " %s " % self.envs["STATUS_CONTEXT_SEPERATOR"]
                )
                # ! This only works whenever there's an activity and PREFERRED_PRESENCE_CONTEXT or TIME_DISPLAY_OUTPUT is not disabled.
                # * Otherwise, we don't have to output anything since there's no context to seperate.
                if (
                    self.envs["PREFERRED_PRESENCE_CONTEXT"]
                    is not ContextOnSubject.CONTEXT_DISABLED
                    or self.envs["TIME_DISPLAY_OUTPUT"]
                    is not PreferredTimeDisplay.TIME_DISABLED
                )
                and contains_activities
                else ""
            )

            # As we handle the seperator, we have to handle how we display the string in the status part of the badge.
            status_output = BadgeStructure(
                (  # * Appends Activity or User's State if `STATIC_SUBJECT_STRING` is not None, otherwise, use the STATIC_SUBJECT_STRING.
                    "%s " % self.envs[state_string]
                    if self.envs["STATIC_SUBJECT_STRING"] is not None
                    else ""
                )
                + (
                    (  # * Appends the User's State whenever presence_ctx is zero or otherwise, append the activity's application name.
                        self.envs[
                            "%s_STATUS_STRING"
                            % self.user_ctx["statuses"]["status"].name.upper()
                        ]
                    )
                    if not contains_activities
                    else presence_ctx[picked_activity]["name"]
                )
                + (  # Append the seperator. This one is a condition-hell since we have to consider two other values and the state of the badge.
                    (
                        seperator  # ! Seperator #1, This contains the `PREFERRED_PRESENCE_CONTEXT` of the activity, if available and its a RICH_PRESENCE.
                        + (
                            presence_ctx[picked_activity][
                                "state"
                                if self.envs["PREFERRED_PRESENCE_CONTEXT"]
                                is ContextOnSubject.STATE
                                else "details"
                            ]
                        )
                    )
                    if picked_activity == PreferredActivityDisplay.RICH_PRESENCE.name
                    and self.envs["PREFERRED_PRESENCE_CONTEXT"]
                    is not ContextOnSubject.CONTEXT_DISABLED  # Other activities is not included at this point since it only gives minimal info.
                    else ""
                )
            )

            # Since we handled the RICH_PRESENCE, now it's time for the `time` to be handled.
            if (
                self.envs["TIME_DISPLAY_OUTPUT"]
                is not PreferredTimeDisplay.TIME_DISABLED
                and contains_activities  # This handles all activities, no exemptions.
            ):
                # ! Seperator #2, Literally invoke the seperator since we assert that the time display is enabled.
                # * Also, since this mf doesn't like '+=', let's do the manual with type.
                status_output = BadgeStructure(status_output + seperator)

                # Since activities can display time remaining or elapsed, check the context if timestamps exists so that it can display `remaining` instead of `elapsed`.
                has_remaining: Union[None, str] = presence_ctx[picked_activity][
                    "timestamps"
                ].get("end")

                # At this point, we have calculate from the time the application or activity has been started. Note that the epoch given by discord is by milliseconds.
                start_time: datetime = datetime.fromtimestamp(
                    int(presence_ctx[picked_activity]["timestamps"]["start"]) / 1000
                )
                running_time: timedelta = (
                    datetime.now() - start_time
                )  # This one calculates the current time to be compatible for any operations with `start_time`.

                # Resolve the time display as it was detected with `timestamps`, thus identified as `remaining`.
                if has_remaining:
                    end_time = (
                        datetime.fromtimestamp(int(has_remaining) / 1000) - start_time
                    )

                    # ! Keep note, that this one is for Unspecified Activity (Spotify) only!!!
                    # * The development of that case will be on post-time, since I'm still doing most of the parts.
                    # For that case, we don't need to sterilize it for a while.
                    if (
                        picked_activity
                        == PreferredActivityDisplay.UNSPECIFIED_ACTIVITY.name
                    ):
                        running_time = running_time - timedelta(
                            microseconds=running_time.microseconds,
                        )
                        end_time = end_time - timedelta(
                            microseconds=end_time.microseconds
                        )

                        status_output = BadgeStructure(
                            status_output + f"{running_time} of {end_time}"
                        )

                # * Resolve for the case of `elapsed`.
                else:
                    # # We can do the MINUTES_ONLY, SECONDS_ONLY and HOURS_ONLY in the future. But for now, its not a priority and its NotImplemented.
                    parsed_time = int(running_time.total_seconds() / 60)

                    # Calculate if some left over minutes can still be converted to hours.
                    hours = 0
                    minutes = 0
                    seconds = 0

                    # * Timedelta() only returns seconds and microseconds. Sadly we have to do the computation on our own.
                    while True:
                        if parsed_time / 60 >= 1:
                            hours += 1
                            parsed_time -= 60
                            continue

                        break

                    minutes = parsed_time

                    # Resolve time strings based on numbers. # ! This costs us readibility.
                    for idx, each_time_string in enumerate(TIME_STRINGS):
                        if self.envs["TIME_DISPLAY_SHORTHAND"]:
                            TIME_STRINGS[idx] = each_time_string[0]

                        # * We have to handle if we should append suffix 's' if the value for each time is greater than 1 or not.
                        else:
                            TIME_STRINGS[idx] = (
                                each_time_string[:-1]
                                if locals()[f"{each_time_string}"] < 1
                                else each_time_string
                            )

                    self.logger.debug(
                        f"Resolved Time Output: {hours} %s {minutes} %s {seconds} seconds."
                        % (TIME_STRINGS[0], TIME_STRINGS[1])
                    )

                    is_time_displayable: bool = hours >= 1 or minutes >= 1

                    # Once we identified some constraints and how it should look, combine it and have it as one string.
                    status_output = BadgeElements(
                        status_output
                        + (
                            (f"{hours} %s" % TIME_STRINGS[0] if hours >= 1 else "")
                            + (" " if hours and minutes else "")
                            + (
                                f"{minutes} %s" % TIME_STRINGS[1]
                                if minutes >= 1
                                else ""
                            )
                            + (
                                f" %s"
                                % self.envs[
                                    "TIME_DISPLAY_%s_OVERRIDE_STRING" % "ELAPSED"
                                    if not has_remaining
                                    else "REMAINING"
                                ]
                            )
                        )
                        if is_time_displayable
                        else "Just started."
                    )

                self.logger.debug(
                    f"Application is identified to be running with remaining time. And is currently under {running_time} / %s."
                    % end_time
                    if has_remaining
                    else f"The application is running endless and has been opened for {running_time}."
                )

            # ! These logger debug output will not be changed, since it shows every possible aspect to which leads to the output of the badge.
            self.logger.debug(
                f"Activity Context (Chosen or Preferred) > {picked_activity}"
            )
            self.logger.debug(
                f"State Output > {state_string} | Subject Output > {subject_output}"
            )
            self.logger.debug(f"Status Output > {status_output}")
            self.logger.debug(f"Final Output > {subject_output} | {status_output}")

            # ! Since we are done with the construction of the output. It's time to manage the colors.
            # * I know that state_string is similar to this case. But I want more control and its reasonable to re-implement it and that's because its main focus was to display a string.
            status_color: ColorHEX = ColorHEX(
                (
                    self.envs[
                        "%s_COLOR"
                        % state_string.removesuffix(
                            "_STRING"
                        )  # Same logic as output (first modification) except we change the suffix from _STRING to _COLOR.
                        + (
                            ""
                            if picked_activity
                            == PreferredActivityDisplay.RICH_PRESENCE.name
                            or contains_activities
                            else ""
                        )
                    ]
                )
                if self.envs["STATIC_SUBJECT_STRING"] is not None or contains_activities
                else BADGE_NO_COLOR_DEFAULT
            )

            # For now, the color only supports HEX which is something that I have to limit for sometime in the future since some logical color declaration is not supported by Badgen.
            if status_color.startswith("#"):
                status_color = ColorHEX(status_color[1:])

            # subject_color logic was the same as similar to state_string + subject_output.
            # Except that instead of focusing in the picked_activity, it was now considering any activity.
            subject_color: ColorHEX = ColorHEX(
                self.envs[
                    "%s_COLOR"
                    % (
                        "%s_STATUS" % self.user_ctx["statuses"]["status"].name.upper()
                        if contains_activities
                        or self.envs["STATIC_SUBJECT_STRING"] is None
                        else state_string.removesuffix("_STRING")
                    )
                ]
            )

            # For now, the color only supports HEX which is something that I have to limit for sometime in the future since some logical color declaration is not supported by Badgen.
            if subject_color.startswith("#"):
                subject_color = ColorHEX(subject_color[1:])

            self.logger.debug(
                f"Status Color: {status_color} | Subject Color: {subject_color}."
            )

            # Sometimes, user's want to display the colors other way around, so we gave them that option since it also looks cool if you think about it.
            if self.envs["SHIFT_STATUS_ACTIVITY_COLORS"]:
                status_color, subject_color = subject_color, status_color

            # At this point, construct the badge as fully as it is.
            constructed_url: BadgeStructure = BadgeStructure(
                f"{BADGE_BASE_URL}{quote(subject_output)}/{quote(status_output)}?color={subject_color}&labelColor={status_color}&icon={BADGE_ICON}"
            )

            # Store it in a variable for a while, so that we can output it when Logging Level Coverage considers DEBUG.
            final_output: BadgeStructure = BadgeStructure(
                BADGE_BASE_MARKDOWN.format(
                    self.envs["BADGE_IDENTIFIER_NAME"],
                    constructed_url,
                    redirect_url,
                )
            )

            self.logger.info(f"The Badge URL has been generated. Link: {final_output}")

            return final_output

        except KeyError as e:
            self.logger.error(
                f"Environment Processing has encountered an error. Please let the developer know about the following. | Info: {e} at line {e.__traceback__.tb_lineno}."  # type: ignore
            )
            terminate(ExitReturnCodes.ILLEGAL_CONDITION_EXIT)
