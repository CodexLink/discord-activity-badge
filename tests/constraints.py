if __name__ == "__main__":
    raise SystemError("You cannot launch the constraints! This might be a mistake. Please launch unit_entrypoint.py instead!")
else:
    from typing import Final

    CONSTRAINTS_CASES : Final = {
        "INTERACTION_CASES": {
        "CONTACTABLE_ON_CLICK":
            {
                "expects": "",
            }
        },
        "OVERRIDE_CASES": {
        "OVERRIDE_DEFAULT_COLOR":
            {
                "expects": "",
            },
        "OVERRIDE_BADGE_ONLINE_COLOR":
            {
                "expects": "",
            },
        "OVERRIDE_BADGE_OFFLINE_COLOR":
            {
                "expects": "",
            },
        "OVERRIDE_BADGE_DND_COLOR":
            {
                "expects": "",
            },
        "OVERRIDE_BADGE_IDLE_COLOR":
            {
                "expects": "",
            },
        },
        "DEPENDENT_CASES": {
        "HIDE_PRESENCE_STATE":
            {
                "expects": "",
            },
        "SHOW_CUSTOM_STATUS_INSTEAD":
            {
                "expects": "",
            },
        "SHOW_DETAIL_INSTEAD":
            {
                "expects": "",
            },
        "SHOW_TIME_DURATION":
            {
                "expects": "",
            },
        },
        "MIN_PRESENCE_CASES": {
        "OVERRIDE_MIN_PRESENCE_ONLINE_COLOR":
            {
                "expects": "",
            },
        "OVERRIDE_MIN_PRESENCE_IDLE_COLOR":
            {
                "expects": "",
            },
        "OVERRIDE_MIN_PRESENCE_DND_COLOR":
            {
                "expects": "",
            },
        "OVERRIDE_MIN_PRESENCE_OFFLINE_COLOR":
            {
                "expects": "",
            },
        "OVERRIDE_NO_PRESENCE_ONLINE_COLOR":
            {
                "expects": "",
            }
        },
        "NO_PRESENCE_CASES": {
        "OVERRIDE_NO_PRESENCE_IDLE_COLOR":
            {
                "expects": "",
            },
        "OVERRIDE_NO_PRESENCE_DND_COLOR":
            {
                "expects": "",
            },
        "OVERRIDE_NO_PRESENCE_OFFLINE_COLOR":
            {
                "expects": "",
            },
        "CUSTOM_NO_PRESENCE_ONLINE_STATUS":
            {
                "expects": "",
            },
        "CUSTOM_NO_PRESENCE_IDLE_STATUS":
            {
                "expects": "",
            },
        "CUSTOM_NO_PRESENCE_DND_STATUS":
            {
                "expects": "",
            },
        "CUSTOM_NO_PRESENCE_OFFLINE_STATUS":
            {
                "expects": "",
            },
        },
    }
