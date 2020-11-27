#
# # entrypoint.py |  A Client's Workflow of Entrypoint. Used by Github Workflows...
# ! Created by Janrey "CodexLink" Licas

from .attributes.constants import *
from sys import argv
from ast import literal_eval
import discord

class DiscBadgeWorkflow(object):
    # * Parameter Checking with Optional Argument "discPresenceMap".
    # * discPresenceMap is used for Updating User's README.md.
    def __init__(self, entryMode, **discPresenceMap=None):
        if not entryMode:
            raise SystemExit(
                "Error, you cannot launch this Script with a Missing Parameter!"
            )

if __name__ == "__main__":
    print(argv) # To be removed. Soon.
    client_instance = DiscBadgeWorkflow(entryMode=argv[1], discPresenceMap=literal_eval(argv[2]))

    # exit(EXIT_SUCCESS)
