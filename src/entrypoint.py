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

if __name__ != "__main__":
	from elements.exceptions import EntryImportNotAllowed

	raise EntryImportNotAllowed

from asyncio import (
	AbstractEventLoop,
	Task,
	all_tasks,
	create_task,
	current_task,
	gather,
	get_event_loop,
	sleep,
	wait,
)
from typing import Any, Generator, Set

from api import AsyncGithubAPILite
from badge import BadgeConstructor
from client import DiscordClientHandler
from elements.constants import ENV_FILENAME, GithubRunnerActions
from utils import UtilityMethods


class DiscordActivityBadge(
	UtilityMethods, AsyncGithubAPILite, DiscordClientHandler, BadgeConstructor
):
	# The heart of the Discord Activity Badge. Everything runs in Object-Oriented Approach. Please check each methods.

	def __await__(self) -> Generator:
		"""
		This special method let the superclass run by calling another user-specified special method which is `__start__`.
		Which basically calls another special method `__await__` to invoke the class in the loop that AsyncIO wants.
		"""

		return self.__start__().__await__()

	async def __start__(self) -> None:
		"""
		Executes all subclasses's methods that are both async and non-async for the preparation of whole process.
		"""

		super().resolve_args()  # * First, we resolve the arguments given by the client before we attempt to do anything.

		super().init_logger(  # * Once the argument has been evaluated, we have to load the Logger to log everything.
			level_coverage=getattr(self.args, "logger_level"),
			root_level=getattr(self.args, "verbosity"),
			log_to_file=getattr(self.args, "generate_log_file"),
			out_to_console=getattr(self.args, "no_console_log"),
		)

		# And then, evaluate the local environment by checking for `.env` before resolve those Environment Variables.
		if getattr(self.args, "running_on_local"):
			super().check_dotenv()

		else:
			self.logger.info(
				f"Running local mode invocation not detected. Skipping checks for '{ENV_FILENAME}'."
			)

		# Once the extra step is done or skipped, evaluate the envs for other modules to use.
		super().resolve_envs()

		# Since every pre-requisite methods were done loading, we have to instantiate other subclasses to load other assets.
		self._cascade_init_cls: Task = create_task(  # (5)
			super().__ainit__(),
			name="Classes_AsyncGithubAPI_Child_Initialization",
		)

		# # The two tasks (`discord_client_task` and `readme_data`) is supposed to be a pair or in `gather()` but they are seperated
		# # because of static cooperative await. Meaning some `await wait()` is waiting at certain codeblocks.
		self.discord_client_task: Task = create_task(
			self.start(self.envs["DISCORD_BOT_TOKEN"]),
			name="DiscordClient_UserFetching",
		)  # * Load the Discord Client so that it can take some time while we load other stuff.

		self.readme_data: Task = create_task(
			self.exec_api_actions(GithubRunnerActions.FETCH_README),
			name="GithubAPI_README_Fetching",
		)  # * Fetch README (expects Base64String from result())

		self.badge_task: Task = create_task(
			self.construct_badge(), name="BadgeConstructor_Construct"
		)  # * Runs badge construction and wait for Task `discord_client_task` to finish before continuing.

		# Implicitly declare this wait instead of inside of the method. There's nothing much to do (in `badge_updater`) while we wait to fetch README data.
		await wait({self.readme_data})

		badge_updater: Task = create_task(
			self.check_and_update_badge(self.readme_data.result()[1]),
			name="README_BadgeChecker_Updater",
		)  # ! Once we got the README, check it and wait for Task `badge_task` to finish before checking if changes is required to commit.

		# Voluntarily invoke this `wait` outside of method `exec_api_action` to avoid confusion due to abstraction.
		await wait({badge_updater})

		if not getattr(self.args, "do_not_commit") and not self.envs["IS_DRY_RUN"]:
			create_task(
				self.exec_api_actions(
					GithubRunnerActions.COMMIT_CHANGES,
					data=[self.readme_data.result()[0], badge_updater.result()],
				)
			)

		else:
			self.logger.warning(
				"Argument -dnc / --do-not-commit was invoked, will skip updating README."
			)

		await self.__end__()  # Once every task/s is done spawning in the loop, await `__end__` to show the status of the tasks whenever there's a blank space in runtime.

	async def __end__(self) -> None:
		"""
		A method that handles the script whenever it waits for any other tasks to finish.
		"""

		self.logger.info("Done loading modules and necessary elements for the process.")
		prev_tasks: Set[Any] = set({})

		while True:  # We do infinite loop while we wait for other tasks to finish.

			if (
				len(all_tasks()) <= 1
			):  # If thre are no other tasks aside from the loop (it's considered a task) then end the loop by closing other sessions.
				self.logger.info(
					"All tasks successfully finished! Closing Client Sessions..."
				)

				await gather(
					self.close(), self._api_session.close()
				)  # Discord API and aiohttp.ClientSession.
				self.logger.info(
					"Connection Sessions were successfully closed. (Discord Client and Github API)"
				)

				break

			# * Otherwise, we display a string (non-redundantly) that counts the number of remaining tasks in the loop.
			tasks: Set[Task] = all_tasks()
			n_tasks: int = len(tasks)

			try:
				if (
					prev_tasks != tasks
				):  # * We also check by the context of all_tasks() if they were in the same length as before but different context, inevitably display it redundantly.
					self.logger.info(
						f"{n_tasks} task/s left to finish the runtime process."
					)
					prev_tasks = tasks
					self.logger.debug(
						f"Current Task: {current_task()} | Other Task/s in Queue | {all_tasks()}"
					)
			except TypeError:
				prev_tasks = tasks

			await sleep(
				0
			)  # We don't need await for certain n of time, we just let other tasks do their own job without disruption from this sleep.


# # Entrypoint Code
loop_instance: AbstractEventLoop = get_event_loop()
entry_instance: AbstractEventLoop = loop_instance.run_until_complete(
	DiscordActivityBadge()
)
