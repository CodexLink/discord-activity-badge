#
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

# # entrypoint.py | A Client's Workflow of Entrypoint.
# * Executed in Docker Container as Main Entrypoint.
# ! Created by Janrey "CodexLink" Licas

from .attributes.constants import *
from sys import argv
import discord

class DiscBadgeWorkflow(object):
    def __init__(self, entryMode, **discPresenceMap=None):
        if not entryMode:
            raise SystemExit(
                "Error, you cannot launch this Script with a Missing Parameter!"
            )

if __name__ == "__main__":
    print(argv) # To be removed. Soon.
    client_instance = DiscBadgeWorkflow(entryMode=argv[1], discPresenceMap=literal_eval(argv[2]))

    # exit(EXIT_SUCCESS)
