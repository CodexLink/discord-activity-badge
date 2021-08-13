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

from argparse import ArgumentParser
from distutils.util import strtobool
from enum import Enum
from logging import FileHandler, Formatter, Logger, StreamHandler, getLogger
from os import _exit as terminate
from os import environ as env
from sys import stdout
from typing import Any, Optional, Type, Union

from elements.constants import (
    ARG_CONSTANTS,
    ENV_FILENAME,
    ENV_STRUCT_CONSTRAINTS,
    LOGGER_FILENAME,
    LOGGER_OUTPUT_FORMAT,
    ROOT_LOCATION,
    ContextOnSubject,
    ExitReturnCodes,
    GithubRunnerLevelMessages,
    LoggerLevelCoverage,
    LoggerRootLevel,
    PreferredActivityDisplay,
    PreferredTimeDisplay,
)


class UtilityMethods:
    """
    A child class designed to store and handle every utility methods. (used by superclass, DiscordActivityBadge)
    """

    def check_dotenv(self) -> None:
        """
        Prepares the .env file to be loaded on runtime.

        This requires Argument -l or --local. Or otherwise, this method will not run.
        ! Note: If method "find_dotenv" raise an error, the script will raise an Exception (ModuleNotFoundError | DotenvFileNotFound).
        """

        try:
            from dotenv import find_dotenv, load_dotenv

            self.logger.info(
                f"Argument --rol / --running-on-local detected, `dotenv` packages were imported."
            )

            self.logger.info(f"Attempting to locate {ROOT_LOCATION}/{ENV_FILENAME}...")
            load_dotenv(
                find_dotenv(
                    filename=ROOT_LOCATION + ENV_FILENAME,
                    raise_error_if_not_found=True,
                )
            )
            self.logger.info(
                f"`dotenv` file ({ROOT_LOCATION + ENV_FILENAME}) was loaded in runtime."
            )

        except ModuleNotFoundError as e:
            msg: str = "Did you installed dotenv from poetry? Try 'poetry install' to install dev dependencies and try again."
            self.logger.critical(msg)

            self.print_exception(GithubRunnerLevelMessages.ERROR, msg, e)

        except IOError as e:
            msg: str = f"File {ENV_FILENAME} at {ROOT_LOCATION} is malformed or does not exists! | Info: {e} at line {e.__traceback__.tb_lineno}."  # type: ignore
            self.logger.critical(msg)

            self.print_exception(GithubRunnerLevelMessages.ERROR, msg, e)

    def init_logger(
        self,
        level_coverage: LoggerLevelCoverage,
        root_level: LoggerRootLevel,
        log_to_file: bool,
        out_to_console: bool,
    ) -> None:
        """
        Loads the logger to be used and referred by all associated classes in superclass (DiscordActivityBadge).

        Args:
            level_coverage: Sets the level of the log coverage. | Defaults to logging.INFO (LoggerLevelCoverage.INFO).
            root_level: Sets the root level coverage in a module. Top module covers all other modules that needs logging. | Defaults to LoggerLevelCoverage.SCRIPT_LEVEL.
            log_to_file: Creates a file and logs the data if set to True, or otherwise. | Defaults to False.
            out_to_console: Output the log reports in the console, if enabled. | Defaults to True.
        """

        LOGGER_HANDLER_FORMATTER: Formatter = Formatter(LOGGER_OUTPUT_FORMAT)

        # Since we invoke Enums in Environment Variables, we have to resolve them here to get the true value of Logger Level.
        self.logger: Logger = getLogger(
            __name__
            if root_level is LoggerRootLevel.SCRIPT_LEVEL
            else LoggerRootLevel.SCRIPT_PLUS_DISCORD.name
            if root_level is LoggerRootLevel.SCRIPT_PLUS_DISCORD
            else LoggerRootLevel.LOOP_LEVEL.name
            if root_level is LoggerRootLevel.LOOP_LEVEL
            else None
        )

        # This asserts that the LoggerLevel is fetched from an Enum, not by natural value. If invalid, it will automatically set to LoggerLevelCoverage.INFO.
        LOGGER_LEVEL_COVERAGE: LoggerLevelCoverage = (
            level_coverage
            if level_coverage in LoggerLevelCoverage
            else LoggerLevelCoverage.INFO
        )
        self.logger.setLevel(LOGGER_LEVEL_COVERAGE.value)

        if log_to_file:
            file_handler = FileHandler(
                filename=LOGGER_FILENAME, encoding="utf-8", mode="w"
            )
            file_handler.setFormatter(LOGGER_HANDLER_FORMATTER)
            self.logger.addHandler(file_handler)
            self.logger.debug(
                f"Log to file has been enabled. Expect log file to be rendered in {LOGGER_FILENAME}."
            )

        if out_to_console:
            console_handler = StreamHandler(stdout)
            console_handler.setFormatter(LOGGER_HANDLER_FORMATTER)
            self.logger.addHandler(console_handler)
            self.logger.debug(
                f"Out to Console (Render Log to Console) has been enabled. Expect more outputs here."
            )

        self.logger.info(
            f"The logger has been loaded with Coverage Level {level_coverage.value}. ({level_coverage.name})"
        )

    def resolve_args(self) -> None:
        # Resolves the arguments given to which was handled by ArgumentParser.

        # Two of the choices require immediate evaluation of values to Enum, thus, we programmatically load it in the script.
        _ll_choices: dict = {}
        _v_choices: dict = {}

        # Each dictionary (_ll_choices and _v_choices) will contain all of their Enum elements, respectively.
        # This will help me adjust the enums and have their possible values assigned correctly.
        for each_enum in [LoggerLevelCoverage, LoggerRootLevel]:
            for each_element in each_enum:
                locals()[
                    ("_ll" if each_element in LoggerLevelCoverage else "_v")
                    + "_choices"
                ][each_element.name] = each_element

        parser = ArgumentParser(
            prog=ARG_CONSTANTS["ENTRY_PARSER_PROG"],
            description=ARG_CONSTANTS["ENTRY_PARSER_DESC"],
            epilog=ARG_CONSTANTS["ENTRY_PARSER_EPILOG"],
        )

        parser.add_argument(
            "-dna",
            "--do-not-alert",
            action="store_true",
            help=ARG_CONSTANTS["HELP_DESC_NO_ALERT_LOCAL_USR"],
            required=False,
        )
        parser.add_argument(
            "-dnc",
            "--do-not-commit",
            action="store_true",
            help=ARG_CONSTANTS["HELP_DESC_DONT_COMMIT"],
            required=False,
        )
        parser.add_argument(
            "-glf",
            "--generate-log-file",
            action="store_true",
            help=ARG_CONSTANTS["HELP_DESC_GENERATE_LOG_FILE"],
            required=False,
        )
        parser.add_argument(
            "-ncl",
            "--no-console-log",
            action="store_false",
            help=ARG_CONSTANTS["HELP_DESC_DONT_LOG_TO_CONSOLE"],
            required=False,
        )
        parser.add_argument(
            "-rol",
            "--running-on-local",
            action="store_true",
            help=ARG_CONSTANTS["HELP_DESC_RUNNING_LOCALLY"],
            required=False,
        )
        parser.add_argument(
            "-ll",
            "--logger-level",
            choices=_ll_choices.keys(),
            default=LoggerLevelCoverage.INFO,
            help=ARG_CONSTANTS["HELP_DESC_LOGGER_LEVEL"],
            required=False,
        )
        parser.add_argument(
            "-v",
            "--verbosity",
            choices=_v_choices.keys(),
            default=LoggerRootLevel.SCRIPT_LEVEL,
            help=ARG_CONSTANTS["HELP_DESC_VERBOSITY"],
            required=False,
        )

        try:
            # Once we add arguments, we parse the sys.argv by default here. (assumption)
            self.args = parser.parse_args()

            # Ever since `parser.add_arguments()` don't have the extensibility to invoke a function when it receives a value, we will do it after parsing them.
            for args_to_resolve in [
                "logger_level",
                "verbosity",
            ]:  # Get the arguments to resolve.

                arg = getattr(self.args, args_to_resolve)  # Assign their value here.

                for each_enum in [LoggerLevelCoverage, LoggerRootLevel]:
                    for each_elem in each_enum:
                        if arg == each_elem.name:
                            setattr(
                                self.args, args_to_resolve, each_elem
                            )  # As the values given by the user matched the name of Enum elements, we use setAttr() as we loop to those Enums.
                            break

        #  ArgumentParser invoke raising SystemExit by default. Catching this exception will ensure that there will be no exceptions shown upon exit.
        except SystemExit:
            terminate(ExitReturnCodes.EXIT_HELP)

    def resolve_envs(self) -> None:
        """
        This method resolves Environment Variables by Loop.
        ! Keep note that, it only tracks certain variables declared under constants.py (ENV_STRUCT_CONSTRAINTS) because of its capability of assigning fallback values.

        Once we resolved those environment variables, they can be placed under `self.envs`, which is going to be used by any other modules.

        This is intentional so that other modules won't need to evaluate them individually. And also to keep the user inputs serialized respectively.
        """

        self.envs: dict[str, Any] = {}  # Setup our container here.

        for idx, (env_key, _) in enumerate(
            ENV_STRUCT_CONSTRAINTS.items()
        ):  # We don't need the value, just the key.

            try:
                # * Attempt to fetch the parameter (3.a) and remove any unnecessary from the environment variable name (3.b).
                env_literal_val: Any = env.get(env_key)
                env_cleaned_name: str = env_key.removeprefix(
                    "INPUT_"
                )  # Since, the script will run in Github Runner, we expect that every environment variable has a pre-fix of "INPUT", so we remove them here.

                # * Assert the existance of environment variables by displaying it in the Console.
                self.logger.debug(
                    "[%i] Env. Var. %s contains %s to be evaluated in %s."
                    % (
                        idx + 1,
                        env_key,
                        env_literal_val if len(env_literal_val) else "None",
                        ENV_STRUCT_CONSTRAINTS[env_key]["expected_type"]
                        if not hasattr(
                            ENV_STRUCT_CONSTRAINTS[env_key]["expected_type"], "__call__"
                        )
                        else ENV_STRUCT_CONSTRAINTS[env_key]["expected_type"].__name__,
                    )
                )

            # ! This except block expects only Dictionary Errors. If you think there's something else to consider, please let me know.
            except KeyError as e:
                msg: str = f"Dictionary Key doesn't exists under `constants.py`. This is a bug or a left-out problem, please report this to the developer! | Info: {e} in line {e.__traceback__.tb_lineno}."  # type: ignore
                self.logger.critical(msg)

                self.print_exception(GithubRunnerLevelMessages.ERROR, msg, e)
                terminate(ExitReturnCodes.ENV_KEY_DOES_NOT_EXISTS_ON_DICT)

            except TypeError as e:
                msg: str = f"Environment Variable {env_key} cannot be found. Are you running on local? Check if you invoked -rol / --running-on-local otherwise it won't run in local. If persisting, check your environment file. If this was deployed, please report this issue to the developer. | Info: {e} in line {e.__traceback__.tb_lineno}."  # type: ignore
                self.logger.critical(msg)

                self.print_exception(GithubRunnerLevelMessages.ERROR, msg, e)
                terminate(ExitReturnCodes.ENV_KEY_DOES_NOT_EXISTS_ON_MACHINE)

            # !!! At this point, the environment must assert that it contains data! If codeblock still hits with an exception, there will be an improvment later on.

            # * The value seemes None (""). Are they optional environments?
            if not env_literal_val:

                self.logger.debug(
                    f"Env. Var. {env_key} doesn't have any value but exists. Checking if they are `required`."
                )

                # We handle some Environment Variables that is not required (is_required -> False).
                if not ENV_STRUCT_CONSTRAINTS[env_key]["is_required"]:
                    self.logger.debug(
                        "Fallback Value of %s for Optional | %s (is None?) -> %s"
                        % (
                            env_key,
                            ENV_STRUCT_CONSTRAINTS[env_key]["fallback_value"] is None,
                            ENV_STRUCT_CONSTRAINTS[env_key]["fallback_value"],
                        )
                    )

                    # Do they have fallback_value assigne> Then typecast their expected_type to the actual value to ensure type-safe.
                    self.envs[env_cleaned_name] = (
                        ENV_STRUCT_CONSTRAINTS[env_key]["expected_type"](
                            ENV_STRUCT_CONSTRAINTS[env_key]["fallback_value"]
                        )
                        if ENV_STRUCT_CONSTRAINTS[env_key]["fallback_value"] is not None
                        else None
                    )

                    self.logger.debug(
                        "Env. Var. `%s` has a resolved value of `%s`! (with type %s)"
                        % (
                            env_key,
                            ENV_STRUCT_CONSTRAINTS[env_key]["fallback_value"],
                            type(ENV_STRUCT_CONSTRAINTS[env_key]["fallback_value"]),
                        )
                    )
                    continue

                # If they are required (is_required -> False) then terminate the script.
                else:
                    msg = f"Env. Var. {env_key} does not exist in local environment file or the repository secret does not exists or invalid! To the developer: Please fill up the required fields (in constants.py) to be able to use this script."
                    self.logger.critical(msg)

                    self.print_exception(GithubRunnerLevelMessages.ERROR, msg, None)
                    terminate(ExitReturnCodes.ILLEGAL_CONDITION_EXIT)

            # ! If the Environment Variable has a value, then we will check their `expected_type` and evaluate them with respect to their type.

            if ENV_STRUCT_CONSTRAINTS[env_key]["expected_type"] in [int, str]:
                # Type cast the given value with the `expected_type` or else assign the `fallback_value` with typecast of `expected_type`.
                # This ensures that the output will be the respected type.

                self.envs[env_cleaned_name] = (
                    ENV_STRUCT_CONSTRAINTS[env_key]["expected_type"](env_literal_val)
                    if len(env_literal_val)
                    else ENV_STRUCT_CONSTRAINTS[env_key]["expected_type"](
                        ENV_STRUCT_CONSTRAINTS[env_key]["fallback_value"]
                    )
                )

            elif ENV_STRUCT_CONSTRAINTS[env_key]["expected_type"] is bool:
                # For the case of boolean values, we have to use the distutils.util.strtobool to evalute them.
                # If the utility method can't serialize it, then we have to use the fallback_value instead.

                try:
                    self.envs[env_cleaned_name] = bool(strtobool(env_literal_val))
                except ValueError:
                    fallback_bool_val: bool = ENV_STRUCT_CONSTRAINTS[env_key][
                        "fallback_value"
                    ]
                    self.envs[env_cleaned_name] = fallback_bool_val

                    msg = f"Env. Var. {env_key} has an invalid key that can't be serialized to boolean. Using a fallback value {fallback_bool_val} instead."
                    self.logger.warning(msg)

                    self.print_exception(GithubRunnerLevelMessages.WARNING, msg, None)

            elif issubclass(ENV_STRUCT_CONSTRAINTS[env_key]["expected_type"], Enum):
                # Handling Enums and resolving them is such a pain in the [...].

                enum_candidates: list[Type[Enum]] = [
                    ContextOnSubject,
                    PreferredActivityDisplay,
                    PreferredTimeDisplay,
                ]  # * We have to fetch these Enums and iterate through them as we try to match the user input's to the names of those Enum elements.

                # is_valid: Union[None, bool] = None

                # Since all enums are declared in upper case. User might intend to apply values in non-case-sensitive form. Hence, we gonna explicitly uppercase them.
                enum_case_env_val: str = env_literal_val.upper()
                assigned_enum_val: Optional[Enum] = None

                if enum_case_env_val:
                    for each_enums in enum_candidates:
                        for each_cls in each_enums:
                            # `is_valid` will be used to break
                            is_valid: bool = bool(
                                enum_case_env_val == each_cls.name
                            )  # If the name matches, then set to `True` or otherwise.

                            self.envs[env_cleaned_name] = (
                                each_cls
                                if enum_case_env_val == each_cls.name
                                else ENV_STRUCT_CONSTRAINTS[env_key]["fallback_value"]
                            )

                            if is_valid:
                                assigned_enum_val = each_cls
                                break

                        if is_valid:
                            break

                    self.logger.info(
                        (
                            f"Env. Var. {env_key} now has a value of %s!"
                            % assigned_enum_val
                        )
                        if is_valid
                        else f"Env. Var. {env_key} was unable to resolve the given argument ({enum_case_env_val}). Reverting to %s..."
                        % (ENV_STRUCT_CONSTRAINTS[env_key]["fallback_value"])
                    )

            else:
                msg = f"Env. Var. '{enum_case_env_val}' cannot be resolved / serialized due to its `expected_type` not a candidate for serialization. Please contact the developer about this for more information."
                self.logger.critical(msg)

                self.print_exception(GithubRunnerLevelMessages.ERROR, msg, None)
                terminate(ExitReturnCodes.NO_CONDITION_IMPLEMENTED_EXIT)

        self.logger.info(
            f"Environment Variables stored in-memory are successfully resolved!"
        )
        self.logger.debug(f"Env. Serialization Context -> {self.envs}")

    def print_exception(
        self,
        message_type: GithubRunnerLevelMessages,
        error_message: str,
        traceback_info: Union[
            Union[Exception, IOError, KeyError, ModuleNotFoundError, TypeError], None
        ],
    ) -> None:
        """
        A utility function that utilizes the error and warning display messages for every runner instance. Quite redundant to be honest...

        Args:
            message_type (GithubRunnerLevelMessages): The level or severity of the message, warning or error. Debug is not used since we don't debug in Runner.
            error_message (str): The message to send in the runner, typically used by the ones who utilizes the logger.
            traceback_info (Union[Type[Exception], None]): The exception that contains the traceback. Usually sent by loggers that is in except code blocks.
        """

        line_no: int = 1  # By default, if traceback_info weren't given.

        if not getattr(
            self.args, "running_on_local"
        ):  # Ensure that we don't display this in local since it destroys logging display consistency.
            if message_type is GithubRunnerLevelMessages:

                if traceback_info is not None:
                    # if isinstance(traceback_info, Exception):
                    # if isinstance(traceback_info, (Exception, IOError, KeyError, ModuleNotFoundError, TypeError)):
                    self.logger.warning(
                        "Traceback information were not provided for this exception. Displaying filename instead."
                    )
                    line_no = (
                        traceback_info.__traceback__.tb_lineno  # type: ignore # ! Investigate this later.
                    )  # Get that last line number :3

                # Then print it, Github Action runner typically resolves or understand this print.
                print(
                    f"::{0} file={1},line={2},col=1::{3}. {4}".format(
                        message_type.value,
                        __file__,
                        line_no,
                        error_message,
                        (
                            "Please refer to the logs for more information about the exception!"
                            if traceback_info is None
                            else ""
                        ),
                    )
                )  # ! Keep note that, we can't get the exact infromation in terms of displaying the line. For column, this seems to be not supported.

            else:
                msg: str = f"Given Enum (message_type) is not a {GithubRunnerLevelMessages}! This isn't supposed to happen, please contact the developer by reporting this issue."
                self.logger.warning(msg)
                print(
                    f"::warning file={__file__}, line=480,col=1::{msg}"
                )  # Have to call this manual, can't call this function alone or we will hit infinite loop.
