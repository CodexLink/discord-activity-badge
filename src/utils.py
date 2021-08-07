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

import logging
from argparse import ArgumentParser
from distutils.util import strtobool
from enum import Enum, IntEnum
from os import _exit as exit
from os import environ as env
from sys import stdout
from typing import Any, Optional, Type, Union

from elements.constants import (
    ARG_CONSTANTS,
    ENV_FILENAME,
    ENV_STRUCT_CONSTRAINTS,
    LOGGER_FILENAME,
    LOGGER_OUTPUT_FORMAT,
    LoggerLevelCoverage,
    ROOT_LOCATION,
    ContextOnSubject,
    PreferredActivityDisplay,
    PreferredTimeDisplay,
)


class UtilityFunctions:
    """
    A class designed to be a child class to the superclass. (ActivityBadgeServices)
    """

    def check_dotenv(self) -> None:
        """
        Prepares the .env file to loaded in this script instance.

        If function "find_dotenv" raise an error, the script won't run.

        Pre-req: Argument -l or --local. Or otherwise, this function will not run.
        """
        try:
            self.logger.info(f"Invoked -l / --local, importing `dotenv` packages.")
            from dotenv import find_dotenv, load_dotenv

        except ModuleNotFoundError:
            self.logger.critical(
                "Did you installed dotenv from poetry? Try 'poetry install' to install dev dependencies."
            )

        try:
            self.logger.info(f"Attempting to locate {ROOT_LOCATION}/{ENV_FILENAME}...")
            load_dotenv(
                find_dotenv(
                    filename=ROOT_LOCATION + ENV_FILENAME,
                    raise_error_if_not_found=True,
                )
            )
            self.logger.info(
                f"Env File at {ROOT_LOCATION + ENV_FILENAME} was validated."
            )

        except IOError:
            self.logger.critical(
                f"File {ENV_FILENAME} at {ROOT_LOCATION} is malformed or does not exists!"
            )

            # todo: I don't know about this one.
            # raise DotEnvFileNotFound(RET_DOTENV_NOT_FOUND)

    def init_logger(
        self,
        level_coverage: IntEnum,
        log_to_file: Optional[bool] = False,
        out_to_console: Optional[bool] = False,
        verbose_client: Optional[bool] = False,
    ) -> None:
        """
        Step 0.3 | Loads the logger for all associated modules.

        Args:
                level_coverage (Optional[int], optional): Sets the level (and above) to cover it in the logs or in stream. Defaults to logging.DEBUG.
                log_to_file (Optional[bool], optional): Creates a file and logs the data if set to True, or otherwise. Defaults to False.
                out_to_console (Optional[bool], optional): Output the log reports in the console, if enabled. Defaults to False.
                verbose_client (Optional[bool], optional): Bind discord to the logger to log other events that is out of scope of entrypoint.
        Summary: todo.
        """

        # Expressed Statements
        LOGGER_HANDLER_FORMATTER: Optional[logging.Formatter] = logging.Formatter(
            LOGGER_OUTPUT_FORMAT
        )
        LOGGER_LEVEL_COVERAGE: IntEnum = (
            level_coverage if level_coverage in LoggerLevelCoverage else LoggerLevelCoverage.DEBUG
        )

        self.logger: logging.Logger = logging.getLogger(
            # todo: This is not intended.
            __name__ if not verbose_client else "discord"
            # "discord"
        )

        self.logger.setLevel(LOGGER_LEVEL_COVERAGE.value)

        if log_to_file:
            file_handler = logging.FileHandler(
                filename=LOGGER_FILENAME, encoding="utf-8", mode="w"
            )
            file_handler.setFormatter(LOGGER_HANDLER_FORMATTER)
            self.logger.addHandler(file_handler)
            self.logger.debug(f"Log to file has been enabled. Expect log file to be rendered in {LOGGER_FILENAME}.")

        if out_to_console:
            console_handler = logging.StreamHandler(stdout)
            console_handler.setFormatter(LOGGER_HANDLER_FORMATTER)
            self.logger.addHandler(console_handler)
            self.logger.debug(f"Out to Console (Render Log to Console) has been enabled. Expect more outputs here.")


        self.logger.info(f"The logger has been loaded with Coverage Level {level_coverage.value}. ({level_coverage.name})")

    def resolve_args(self) -> None:
        _parser = ArgumentParser(
            description=str(ARG_CONSTANTS["ENTRY_PARSER_DESC"]),
            epilog=str(ARG_CONSTANTS["ENTRY_PARSER_EPILOG"]),
        )

        _parser.add_argument(
            "-dr",
            "--dry-run",
            action="store_true",
            help=ARG_CONSTANTS["HELP_DESC_DRY_RUN"],
        )  # todo: This is conflicting with the other way to enable dry run. To be evaluated later.

        _parser.add_argument(
            "-lc",
            "--log-to-console",
            action="store_true",
            help=ARG_CONSTANTS["HELP_DESC_LOG_TO_CONSOLE"],
            required=False,
        )

        _parser.add_argument(
            "-dn",
            "--do-not-alert-user",
            action="store_true",
            help=ARG_CONSTANTS["HELP_DESC_NO_ALERT_USR"],
            required=False,
        )

        _parser.add_argument(
            "-nl",
            "--no-file",
            action="store_true",
            help=ARG_CONSTANTS["HELP_DESC_NO_LOG_TO_FILE"],
            required=False,
        )

        _parser.add_argument(
            "-l",
            "--local",
            action="store_true",
            help=ARG_CONSTANTS["HELP_DESC_RUNNING_LOCALLY"],
            required=False,
        )

        _parser.add_argument(
            "-vc",
            "--verbose-client",
            action="store_true",
            help=ARG_CONSTANTS["HELP_DESC_VERBOSE_CLIENT"],
            required=False,
        )

        try:
            self.args = _parser.parse_args()  # todoL Annotate this one.

        #  ArgumentParser invoke raising SystemExit by default. Catching this exception will ensure that there will be no exceptions shown upon exit.
        # I assume that this one emits only when -h is invoked in the terminal or for when this script has been launched.
        except SystemExit:
            exit(0)  # todo: Annotate this code.

    def resolve_envs(self) -> None:
        """
        This function resolves everything that is exists under Environment Variables by Loop (2). Keep note that, it only tracks certain variables
        declared under constants.py (ENV_STRUCT_CONSTRAINTS).

        Once we resolved those environment variables, they can be placed under `self.envs` (1), which is going to be used by any other modules.
        This was done so that the references are more clear and less redundant from keeping at calling os.environ.get().

        """
        self.envs: dict[str, Any] = {}  # * (1)

        for idx, (env_key, _) in enumerate(ENV_STRUCT_CONSTRAINTS.items()):  # * (2)

            try:
                # * Attempt to fetch the parameter (3.a) and remove any unnecessary from the environment variable name (3.b).
                _env_literal_val: Any = env.get(env_key)  # * 3.a
                _env_cleaned_name: str = env_key.removeprefix("INPUT_")  # 3.b

                # * Attempt to display it in the Console to see if it would emit errors before the other code-blocks do.
                self.logger.debug(
                    "[%i] Env. Var. %s contains %s to be evaluated in %s."
                    % (
                        idx + 1,
                        env_key,
                        _env_literal_val if len(_env_literal_val) else "None",
                        ENV_STRUCT_CONSTRAINTS[env_key]["expected_type"]
                        if not hasattr(
                            ENV_STRUCT_CONSTRAINTS[env_key]["expected_type"], "__call__"
                        )
                        else ENV_STRUCT_CONSTRAINTS[env_key]["expected_type"].__name__,
                    )
                )

            # ! This except block expects only Dictionary Errors. If you think there's something else to consider, please let me know.
            except KeyError as Err:
                self.logger.critical(
                    f"Dictionary Key doesn't exists under `constants.py`. This is a bug or a left-out problem, please report this to the developer! | Info: {Err}"
                )
                exit(-1)

            try:
                if not len(
                    _env_literal_val
                ):  # The value seemes None (""). Are they optional environments?

                    self.logger.debug(
                        f"Env. Var. {env_key} doesn't have any value but exists. Checking if they are `required`."
                    )

                    if not ENV_STRUCT_CONSTRAINTS[env_key]["is_required"]:
                        self.logger.debug(
                            "Fallback Value for Optional | %s (is None?) -> %s"
                            % (
                                ENV_STRUCT_CONSTRAINTS[env_key]["fallback_value"]
                                is None,
                                ENV_STRUCT_CONSTRAINTS[env_key]["fallback_value"],
                            )
                        )
                        self.envs[_env_cleaned_name] = (
                            ENV_STRUCT_CONSTRAINTS[env_key]["expected_type"](
                                ENV_STRUCT_CONSTRAINTS[env_key]["fallback_value"]
                            )
                            if ENV_STRUCT_CONSTRAINTS[env_key]["fallback_value"]
                            is not None
                            else None
                        )

                        self.logger.info(
                            "Env. Var. %s has now a resolved value of %s! (with type %s)"
                            % (
                                env_key,
                                ENV_STRUCT_CONSTRAINTS[env_key]["fallback_value"],
                                type(ENV_STRUCT_CONSTRAINTS[env_key]["fallback_value"]),
                            )
                        )
                        continue

                    else:
                        self.logger.critical(
                            f"[{idx + 1}] Env. Var. {env_key} does not exist or does not have a supplied value! Please fill up the required fields (in constants.py) to be able to use this script."
                        )
                        exit(-1)

                if ENV_STRUCT_CONSTRAINTS[env_key]["expected_type"] in [int, str]:
                    self.envs[_env_cleaned_name] = (
                        ENV_STRUCT_CONSTRAINTS[env_key]["expected_type"](
                            _env_literal_val
                        )
                        if len(_env_literal_val)
                        else ENV_STRUCT_CONSTRAINTS[env_key]["fallback_value"]
                    )

                elif ENV_STRUCT_CONSTRAINTS[env_key]["expected_type"] is bool:
                    try:
                        self.envs[_env_cleaned_name] = bool(
                            strtobool((_env_literal_val))
                        )
                    except ValueError:
                        _fallback_bool_val: bool = ENV_STRUCT_CONSTRAINTS[env_key][
                            "fallback_value"
                        ]
                        self.envs[_env_cleaned_name] = _fallback_bool_val
                        self.logger.warning(
                            f"Env. Var. {env_key} has an invalid key that can't be serialized to boolean. Using a fallback value {_fallback_bool_val} instead."
                        )

                elif issubclass(ENV_STRUCT_CONSTRAINTS[env_key]["expected_type"], Enum):
                    _enum_candidates: list[Type[Enum]] = [
                        ContextOnSubject,
                        PreferredActivityDisplay,
                        PreferredTimeDisplay,
                    ]

                    is_valid: Union[None, bool] = None

                    # Since all enums are declared in upper case. User might intend to apply values in non-case-sensitive form. Hence, we gonna explicitly uppercase them.
                    _enum_case_env_val: str = _env_literal_val.upper()

                    if len(_enum_case_env_val):
                        for each_enums in _enum_candidates:  # This is gonna hurt.
                            for _each_cls in each_enums:
                                is_valid = _enum_case_env_val == _each_cls.name
                                self.envs[_env_cleaned_name] = (
                                    _each_cls
                                    if _enum_case_env_val == _each_cls.name
                                    else ENV_STRUCT_CONSTRAINTS[env_key][
                                        "fallback_value"
                                    ]
                                )

                                if is_valid:
                                    break
                            if is_valid:
                                break

                        self.logger.info(
                            (f"Env. Var. {env_key} now has a value of %s!" % _each_cls)
                            if is_valid
                            else f"Env. Var. {env_key} was unable to resolve the given argument ({_enum_case_env_val}). Reverting to %s..."
                            % (ENV_STRUCT_CONSTRAINTS[env_key]["fallback_value"])
                        )

                else:
                    self.logger.critical(
                        f"Env. Var. '{_enum_case_env_val}' cannot be resolved / serialized due to its expected_type not a candidate for serialization. Please contact the developer about this for more information."
                    )

            except Exception as Err:  # We can't catch <class 'NoneType'> here. Use Exception instead.
                self.logger.critical(
                    f"Environment Variable {env_key} cannot be found. Are you running on local? Invoke --local if that would be the case. If persisting, check your environment file. If this was deployed, please report this issue to the developer. | Info: {Err}"
                )
                exit(-1)

        self.logger.info(
            f"Environment Variables stored in-memory are successfully resolved!"
        )
        self.logger.debug(f"Env. Serialization Context -> {self.envs}")
