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

from argparse import Namespace
from asyncio import create_task
from logging import Logger
from os import _exit as terminate
from typing import Any, Callable, List, NoReturn, Optional, Union

from discord import Activity, ActivityType, Client, ClientUser, Member, Status
from discord.activity import CustomActivity, Game
from discord.errors import HTTPException, NotFound
from discord.guild import Guild
from discord.user import User

from elements.constants import (
    BLUEPRINT_INIT_VALUES,
    DISCORD_CLIENT_INTENTS,
    DISCORD_USER_STRUCT,
    ExitReturnCodes,
    GithubRunnerLevelMessages,
    PreferredActivityDisplay,
)


class DiscordClientHandler(Client):
    # * The following variables are declared for weak reference since there's no hint-typing inheritance.

    args: Namespace
    envs: Any
    logger: Logger
    print_exception: Callable
    user: ClientUser

    # A Client Wrapper Child Class that extracts Discord User's Activities from Rich Presence to Activity Status.
    # Subclass -> Client (object): The subclass that is actually the DiscordClient.

    def __init__(self) -> None:
        # A constructor that initializes another constructor, which is directly referring to DiscordClient (known as discord.Client) to instantiate resources.

        super().__init__(intents=DISCORD_CLIENT_INTENTS)

    async def on_ready(self) -> None:
        """
        A called method from a dispatch method when everything is ready. This means of WebSocket must be on and everything must be loaded (cached).
        This is the part where discord.py takes awhile to initialize because of Discord's API Rules.
        """

        self.logger.debug(
            f"Connection to Discord via WebSocket is success! | Rate-Limited: {self.is_ws_ratelimited()}."
        )

        create_task(  # This is optional, but I made it so that we can see if the Bot was active.
            (
                self.change_presence(
                    status=Status.online,
                    activity=Activity(
                        name=" your activities.", type=ActivityType.watching
                    ),
                )
            )
        )

        self.logger.info(
            f"Changed / Pushed Rich Presence to display {self.user}'s status."
        )

        # I ! cannot do reference by variable of this blank blueprint because TypedDict and other elements associated to it is complaining about it.
        self.user_ctx: DISCORD_USER_STRUCT = BLUEPRINT_INIT_VALUES

        # Perform two async actions with one on top of it as an input from the outer method.
        # ! We cannot create_tasks for them since one of them is a dependency and there's no room for more actions.
        await self._get_activities_via_guild(
            await self._get_discord_user()
        )  # * 3 [a, b]

        self.logger.info(
            "Discord Client is finished fetching data and is saved for badge processing."
        )

        await self.close()
        self.logger.info("Closing Sessions (1 of 2) | discord.Client -> Done.")

        # We might wanna catch it here to provide accurate information about the possible occurence of the error.

    async def _get_discord_user(self) -> User:
        """
        A private method that obtains Discord User's Information for further query with the Mutual Guilds.
        This is required ever since direct access to User's information is not included with the API, so we have to make some extra steps to obtain it.

        Returns:
            User: Contains information of the user.
        """

        self.logger.info("Fetching Discord User's info...")

        try:
            user_info = await self.fetch_user(self.envs["DISCORD_USER_ID"])

            self.user_ctx["id"] = user_info.id
            self.user_ctx["name"] = user_info.name
            self.user_ctx["discriminator"] = user_info.discriminator

            self.logger.info(
                "Discord User %s Fetched."
                % (self.user_ctx["name"] + self.user_ctx["discriminator"])
            )

        except NotFound as e:
            await self._exit_client_on_error(
                f"The user cannot be found. Did you input your Discord ID properly? | Info: {e} on line {e.__traceback__.tb_lineno}."  # type: ignore
            )

        except HTTPException as e:
            await self._exit_client_on_error(
                f"Failed to make a request due to malformed data given under `DISCORD_USER_ID` key. Which results to: {e} on line {e.__traceback__.tb_lineno}. | This can be a developer's fault upon assigning non-existent Env Key, please make an issue about this problem."  # type: ignore
            )

        return user_info

    async def _get_activities_via_guild(self, fetched_user: User) -> None:
        """
        Retrieves User Activities by accessing a Mutual Guild with the Bot.

        Args:
            fetched_user (User): Discord User's Information, which is the inner scope method returned.

        Notes:
            (3) Fetch all activities from the user and serialize it in a way where it can be contained in self.__client_container under key "presence" (self.__client_container["presence"])
            (3) Every attributes can be a dict() by calling to_dict() that is embedded from the activity.
            (3) Each Activity Type will be renamed to accomodate the lower-case, underscore-space key and consistency.
            (3) Once done, push the activity name (__cls_name__) to __activity_picked__ (List) so that no other duplicates can be inserted to the container.
            (4) The discord.user.User itself doesn't provide much information of the user in real-time. I have to go through Guilds to see what's their current status.
            (4) This is the exact reason of why this scope is not included to the DiscordClientHandler.__get_user() context.

        """

        self.logger.info("Fetching mutual guild from the cached instance client...")

        # Before we get the guild, check if we mutual guilds between the User and the Bot.
        if not fetched_user.mutual_guilds:
            await self._exit_client_on_error(
                f"Discord User {fetched_user.name} doesn't have any Mutual Guilds with {self.user}. Please add the bot to your server and try again.",
                fetched_user,
            )

        # If there is a mutual guild, then ensure that it is class 'discord.guild.Guild'> and fetch the first one.
        if not isinstance(fetched_user.mutual_guilds[0], Guild):
            await self._exit_client_on_error(
                f"The list of mutual guild/s is/are expected to be {Guild}. This is an issue that the developer can solve. Please report this issue in https://github.com/CodexLink/discord-activity-badge",
                fetched_user,
            )

        # Once type checked, fetch the user from guild and fetch it as a member from that guild.
        fetched_member: Optional[Member] = fetched_user.mutual_guilds[0].get_member(
            fetched_user.id
        )

        if (
            fetched_member
        ):  # ! Since `get_member` enforce Optional, then we assert here that it will never be Optional or lead to None.
            if not fetched_member.activities:
                self.logger.warning(f"User {fetched_member} doesn't have any activity.")

            else:
                self.logger.info(
                    f"User {fetched_member} contains {len(fetched_member.activities)} activit%s."
                    % ("y" if not len(fetched_member.activities) > 1 else "ies")
                )

                # For every activity exists, we store them uniquely. This means duplicated activities (same activity) will be ignored.
                unique_activities: List[str] = []

                # For each activities stored in-memory, iterate through them so that we can store them in unique_activities.
                for idx, each_activities in enumerate(fetched_member.activities):
                    self.logger.debug(
                        f"Activity Assessment ${idx + 1} | {each_activities}"
                    )

                    if not each_activities.__class__.__name__ in unique_activities:
                        self.logger.debug(
                            f"Activity {each_activities.__class__.__name__} was not in the list. (The list contains {unique_activities})"
                        )

                        # ! I can't type `activity_ctx` because BaseActivity and Spotify doesn't have `to_dict` method.
                        activity_ctx: dict[Union[str, dict[Any, Any]], Any] = each_activities.to_dict()  # type: ignore # * Extract the activity in dictionary form.

                        cls_name: str = (
                            each_activities.__class__.__name__
                        )  # Get the activity class name.

                        resolved_activity_name = (  # Then we resolve it with Enums.
                            PreferredActivityDisplay.CUSTOM_ACTIVITY.name
                            if cls_name == CustomActivity.__name__
                            else PreferredActivityDisplay.RICH_PRESENCE.name
                            if cls_name == Activity.__name__
                            else PreferredActivityDisplay.GAME_ACTIVITY.name
                            if cls_name == Game.__name__
                            else PreferredActivityDisplay.SPOTIFY_ACTIVITY.name
                        )

                        self.user_ctx["activities"][
                            resolved_activity_name
                        ] = activity_ctx  # ! Once we resolve the name, have it as key and store the activity context.

                        unique_activities.append(cls_name)
                        self.logger.debug(
                            f"Activity '{resolved_activity_name}' has been pushed in the list of unique activities!"
                        )

                    else:
                        self.logger.debug(
                            f"Activity {each_activities} is ignored since one data of the same type was appended in unique_activities. (Contains: {unique_activities})"
                        )

            # As we handle the Activities, we have to handle the state of the user as a fallback output.
            self.user_ctx["statuses"]["status"] = fetched_member.status  # type: ignore # I didn't expect this one to be different from other Enums.

            # ! Other states may be utilized in the future, they are subject to change.
            self.user_ctx["statuses"]["on_web"] = fetched_member.web_status
            self.user_ctx["statuses"]["on_desktop"] = fetched_member.desktop_status
            self.user_ctx["statuses"]["on_mobile"] = fetched_member.mobile_status

            self.logger.info(
                "Step 2 of 2 | Finished fetching discord user's rich presence and other activities."
            )
            self.logger.debug(
                f"User Context Container now contains the following: {self.user_ctx}"
            )

        else:

            msg: str = "The requested user -> member (from the guild) does not exists! This was already asserted on the previous methods which means this shoudn't happen in the first place. Please contact the developer about this issue, if persists."
            self.logger.error(msg)

            self.print_exception(GithubRunnerLevelMessages.ERROR, msg, None)
            terminate(ExitReturnCodes.ILLEGAL_CONDITION_EXIT)

    async def _exit_client_on_error(
        self, err_message: str, user_to_dm: Optional[User] = None
    ) -> NoReturn:
        """
        A method that handles exceptions with the ability to message the user about it.

        Args:
            err_message (str): The error message to display and to send in user when `user_to_dm` is True.
            user_to_dm (User): A user to refer to create a DM channel for the bot to use.

        Returns:
            NoReturn: This method does not return anything since it terminates the script runtime.
        """
        if user_to_dm and not getattr(self.args, "do_not_alert"):
            dm = await user_to_dm.create_dm()
            await dm.send(err_message)

        else:
            self.logger.warning(
                "Argument -dna / --do-not-alert has been invoked or User is not provided. DM process is cancelled."
            )

        msg: str = (
            f"Discord Client Handler encountered a problem! | Info: {err_message}"
        )
        self.logger.error(msg)

        self.print_exception(GithubRunnerLevelMessages.ERROR, msg)

        await self.close()
        terminate(ExitReturnCodes.ILLEGAL_CONDITION_EXIT)
