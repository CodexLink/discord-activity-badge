if __name__ == "__main__":
    raise SystemExit(
        "You're about to run an Attribute Module which is not allowed! Run the src/entrypoint.py instead!"
    )
else:
    from discord import Intents
    from typing import Final

    client_intents = Intents.none()
    client_intents.presence = True
