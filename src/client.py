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

import os
from asyncio import ensure_future
from typing import Any, List

from discord import Activity, ActivityType, Member
from discord import Client as DiscordClient
from discord import Status
from discord.activity import Activity, CustomActivity, Game
from discord.errors import HTTPException, NotFound
from discord.guild import Guild
from discord.user import User

from elements.constants import (
    DISCORD_CLIENT_INTENTS,
    DISCORD_DATA_CONTAINER,
    DISCORD_DATA_CONTAINER_ATTRS,
    DISCORD_DATA_FIELD_CUSTOM,
    DISCORD_DATA_FIELD_GAME,
    DISCORD_DATA_FIELD_PRESENCE,
    DISCORD_DATA_FIELD_UNSPECIFIED,
)


class DiscordClientHandler(DiscordClient):
    """
    A DiscordClient Async Wrapper for handling request of user's related activities for badge processing.

    Args:
        DiscordClient (object): The class "Client" that is normally used to instantiate from a variable.
    """

    def __init__(self) -> None:
        """
        A constructor that initializes another constructor, which is directly referring to DiscordClient (known as discord.Client) to instantiate resources.
        """
        super().__init__(intents=DISCORD_CLIENT_INTENTS)

    async def on_ready(self) -> None:
        """
        An entrypoint function to load attributes and properties to be used in the latter process.
        This is the part where discord.py takes awhile to initialize because of Discord's API Rules.

        Notes:
                        (1.a) Creates an object container (class) that contains necessarity information user and it's activity/ies.
                        (1.b) The following class contains a dict() that maps the user's status and its activity later. For more information, go check elements.constants | Discord Client Container Metadata.
                        (2) Instantiates Presence Activity in the Bot, this was done just for an indicator. So it's not a big deal at all.
                        (3.a) Two-stacked awaitable functions are done in order to ensure that we have the user's context first, and then we get the status and its activity via outer scope function.
                        (3.b) The use of asyncio.gather() or Queue() won't work here because we need to wait for the inner scope function to finish first. Can't do asynchronously on this space.

        """
        # ensure_future(super().__ainit__())  # * ?? [a, b], Subject to change later.

        self.logger.info(f"Discord Client {self.user} is ready for evaluation of user's activity presence.")

        self._client_ctx: object = type(
            DISCORD_DATA_CONTAINER, (object,), DISCORD_DATA_CONTAINER_ATTRS
        )  # * (1) [a, b]


        ensure_future(
            (
                self.change_presence(
                    status=Status.online,
                    activity=Activity(
                        name=" your activities.", type=ActivityType.watching
                    ),
                )
            )
        )  # * (2)
        self.logger.info(f"Pushed Rich Presence Context Discord API to Display {self.user}'s status.")


        self.logger.info(f"Fetching Discord User's Data.") # todo: Annotate this later.

        await self.get_activities_via_guild(await self.get_user())  # * 3 [a, b]
        self.logger.info(
            "Discord Client is finished fetching data and is saved for badge processing."
        )

        await self.close()
        self.logger.info("Closing Sessions (1 of 2) | discord.Client -> Done.")

        # We might wanna catch it here to provide accurate information about the possible occurence of the error.

    async def get_user(self) -> User:
        """
        Obtains Discord User's Basic Information and returns it as a "discord.user.User".

        The obtained information will be used to find the user in the guild to get the "Activity" of the user.
        Sadly, we can't just do it directly with User. It's the Discord's API limitation, as far as I know.

        Notes:
                        (1) The implementation of variable assignments is quite uncommon in this case. The self._client_container.user is non-existent
                        (1) unless instantiated. Please refer to elements.constants | Discord Client Container Metadata to see the elements that is mypy unable to find.

        Returns:
                        User: Contains information of the user encapsulated in <class 'discord.user.Users'>.
        """

        self.logger.info(
            "Step 1.a of 2 | Attempting to fetch discord user's info for validation use."
        )

        try:
            _user_info = await self.fetch_user(
                os.environ.get("INPUT_DISCORD_USER_ID")
            )

            self.some_data_later = _user_info

            # * (1) and similar.
            self._client_ctx.user["id"] = _user_info.id
            self._client_ctx.user["name"] = _user_info.name
            self._client_ctx.user["discriminator"] = _user_info.discriminator

            self.logger.info(
                "Step 1.b of 2 | Finished fetching user information."
            )

            return _user_info

        except NotFound as Err:
            await self.__exit_client_on_error(
                f"The user cannot be found. Did you input your Discord ID properly? | Result: {Err}"
            )

        except HTTPException as Err:
            await self.__exit_client_on_error(
                f"Failed to make request due to malformed data given under DISCORD_USER_ID key. Which results to: {Err} | This can be a developer's fault upon assigning non-existent Env Key, please make an issue about this problem."
            )

    async def get_activities_via_guild(self, fetched_user: User) -> None:
        """
        Retrieves User Activities by accessing a (Mutual) Guild with the Bot.

        Args:
            _fetched_user (User): The context of the inner scope function, which should contain the User's Information.

        Notes:
            (1.1.a) Before we get the guild, check if we have the bot and the user reside on a certain guilds (ie. mutual guilds).
            (1.1.b) If ever there will be a context, ensure that the types we are seeing is a type of <class 'discord.guild.Guild'>
            (2) Fetch the guild from the user and fetch it as a member from that guild.
            (3) Fetch all activities from the user and serialize it in a way where it can be contained in self.__client_container under key "presence" (self.__client_container["presence"])
            (3) Every attributes can be a dict() by calling to_dict() that is embedded from the activity.
            (3) Each Activity Type will be renamed to accomodate the lower-case, underscore-space key and consistency.
            (3) Once done, push the activity name (__cls_name__) to __activity_picked__ (List) so that no other duplicates can be inserted to the container.
            (4) The discord.user.User itself doesn't provide much information of the user in real-time. I have to go through Guilds to see what's their current status.
            (4) This is the exact reason of why this scope is not included to the DiscordClientHandler.__get_user() context.

        Concept Notes:
            (3) Keep in note that the loop only fetch the first object of a certain type of the activity. This means that, at the end of the loop, for every n has their distinct types.
            (3) They cannot have more than 1 but should be exactly 1. This is similar to first-in, first-out.

        """

        self.logger.info(
            "Step 2 of 2 | Attempting to fetch guild context from where the bot also resides."
        )

        # * (1.1.a)
        if not fetched_user.mutual_guilds:
            await self.__exit_client_on_error(
                f"Discord User doesn't have any Mutual Guilds with {self.user}. Please add the bot to your server and try again."
            )

        # * (1.1.b)
        for each_guilds in fetched_user.mutual_guilds: # todo: Add something to message to the user so that they know the error.
            if not isinstance(each_guilds, Guild):
                await self.__exit_client_on_error(
                    f"The list of mutual guild/s is/are expected to be {Guild}, but received a type {type(each_guilds)}"
                )

        # * (1.2)
            _fetched_member: Member = each_guilds.get_member(fetched_user.id)

            if _fetched_member: # todo: Check if this one work.
                break

        # * (2)
        if not (_fetched_member.activities):
            self.logger.warning(
                "This user doesn't have any activity. Letting BadgeConstructor to fill it."
            )

        else:
            self.logger.info(
                f"{_fetched_member} contains {len(_fetched_member.activities)} activit%s." % ("y" if not len(_fetched_member.activities) > 1 else "ies")
            )

            _activity_picked: List[str] = []

            # * (3)
            for idx, each_activities in enumerate(_fetched_member.activities):
                self.logger.debug(
                    f"Activities Iteration {idx + 1} of {len(_fetched_member.activities)} | {each_activities}"
                )

                if not each_activities.__class__.__name__ in _activity_picked:
                    self.logger.debug(
                        f"{each_activities.__class__.__name__} was not in _activity_picked. (Contains {_activity_picked})"
                    )
                    __activity: dict = each_activities.to_dict()
                    __cls_name: str = each_activities.__class__.__name__ # should be ClassName?

                    __resolved_activity_name = (
                        DISCORD_DATA_FIELD_CUSTOM
                        if __cls_name == CustomActivity.__name__
                        else DISCORD_DATA_FIELD_PRESENCE
                        if __cls_name == Activity.__name__
                        else DISCORD_DATA_FIELD_GAME
                        if __cls_name == Game.__name__
                        else DISCORD_DATA_FIELD_UNSPECIFIED
                    )

                    self.logger.debug(
                        f"Pushing context '{__resolved_activity_name}' to self._client_container.user -> in key 'presence'..."
                    )

                    self._client_ctx.user["presence"][
                        __resolved_activity_name
                    ] = __activity

                    self.logger.debug(
                        f"Pushed to self._client_container.user in key 'presence' as '{__resolved_activity_name}.'"
                    )

                    _activity_picked.append(__cls_name)
                    self.logger.debug(
                        f"Appended {__resolved_activity_name} to _activity_picked. (Now contains: {_activity_picked})"
                    )

                else:
                    self.logger.debug(
                        f"Ignored {each_activities} since one data of same type was appended in _activity_picked (Contains: {_activity_picked})"
                    )

            # * (4)
            self._client_ctx.user["status"][
                "status"
            ] = _fetched_member.status.value
            self._client_ctx.user["status"][
                "on_web"
            ] = _fetched_member.web_status.value
            self._client_ctx.user["status"][
                "on_desktop"
            ] = _fetched_member.desktop_status.value
            self._client_ctx.user["status"][
                "on_mobile"
            ] = _fetched_member.mobile_status.value

            self.logger.info(
                "Step 2 of 2 | Finished Fetching Discord User's Rich Presence and Other Activities."
            )
            self.logger.debug(
                f"Client Container ({DISCORD_DATA_CONTAINER}) now contains the following: {self._client_ctx.user}"
            )

    async def __exit_client_on_error(self, err_message: str) -> None:
        self.logger.error(err_message)
        await self.close()
        self.logger.error("Closed Connection to Discord Gateway API due to error.")
        os._exit(-1)
