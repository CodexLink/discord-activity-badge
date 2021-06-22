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

# # Discord Exceptions
class MutualGuildsNotFound(Exception):
	"""Cannot find a guild where the bot is residing with the user who requests for presence badge.

	Args:
		Exception (Subclass): Inherits Exception Class.
	"""
	pass


class UserDoesNotExists(Exception):
	"""[Handles exception 'when received object is not a discord.user.User, exclusively.']

	Args:
		Exception ([type]): [description]
	"""
	pass

# # Module Exceptions

class IsolateExecNotAllowed(Exception):
	"""The use of modules under isolation is not allowed; hence, raising this error.
	Args:
		Exception (Class): Inherits Exception Class.
	"""
	def __init__(self: object) -> None:
		messages : str = "The use of modules without instantiating the entrypoitn is not allowed."
	  	super().__init__(messages)
