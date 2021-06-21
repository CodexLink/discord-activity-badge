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
