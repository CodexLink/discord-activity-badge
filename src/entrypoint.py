# Add Shebang here later.

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
