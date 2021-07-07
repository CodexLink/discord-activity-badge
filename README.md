<h1 align="center">Discord Rich Presence Activity Badge Action</h1>
<h4 align="center">A containerized action that bridges the Discord User's Rich Presence to a Presentable Badge on their Special Repository (Github Profile). Powered by **Python + Asnycio + discord.py** </h4>

<div align="center">

[![Container Tester](https://github.com/CodexLink/discord-rich-presence-activity-badge/actions/workflows/docker_test.yml/badge.svg)](https://github.com/CodexLink/discord-rich-presence-activity-badge/actions/workflows/docker_test.yml)
[![Containerization | Discord Rich Presence Activity Badge](https://github.com/CodexLink/discord-rich-presence-activity-badge/actions/workflows/docker_deploy.yml/badge.svg)](https://github.com/CodexLink/discord-rich-presence-activity-badge/actions/workflows/docker_deploy.yml)

[![Codacy Code Quality Grade](https://badgen.net/codacy/grade/42fcd1c143464a288522e236f929b1a8?icon=codacy&label=Codacy%20Code%20Quality)](https://app.codacy.com/gh/CodexLink/discord-rich-presence-activity-badge/dashboard)
[![CodeFactor Code Quality Grade](https://img.shields.io/codefactor/grade/github/CodexLink/discord-rich-presence-activity-badge?label=CodeFactor%20Code%20Quality&logo=codefactor)](https://www.codefactor.io/repository/github/codexlink/discord-rich-presence-activity-badge)
[![Repository License](https://img.shields.io/badge/Repo%20License-Apache%20License%202.0-blueviolet)](https://github.com/CodexLink/discord-rich-presence-activity-badge/blob/main/LICENSE)
</div>

## Welcome

Hello! This repository is still under construction and work in progress. Progression is approximated to be 70%.

An overdetailed-async implementation........ [???]

## What's missing?

To give you an overview, here is the list that contain implementations and tasks that I haven't started yet.

- Badge Constructor and Validator
- Arguments (Both Optional and Required)
- README Modifier
- Git Commit and Push as User

> The list will be updated as I push possible changes.

TL;DR: Semi-usable but cannot be used **as-is** due to components missing.

## Usage

...

## Workflow

The following `YAML` workflow is a bare-minimum that you may need to paste on your profile's repo located in `.github/actions` .

``` yaml
name: Discord Rich Presence Activity Badge
on:
  schedule:

    - cron: "30 0-23 * * *" # Customizable 15 Minutes Less Not Allowed!, At minute 30 past every hour from 0 through 23.

  workflow_dispatch:

jobs:
  BadgeUpdater:
    name: Discord Activity Watcher
    runs-on: ubuntu-latest

    steps:
      - name: Update README Discord Badge to Latest Upstream
      - uses: CodexLink/discord-rich-presence-activity-badge@main

        with:
          DISCORD_USER_ID: ${{ secrets.DISCORD_USER_ID }}
          DISCORD_BOT_TOKEN: ${{ secrets.DISCORD_BOT_TOKEN }}
          WORKFLOW_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          IS_DRY_RUN: true

```

> This workflow will run once it has been dispatched (manually) or is on scheduled to run for every **30 minutes per hour** to check for the user's status.

## Parameters

The following sub-sections contain a set of possible inputs that you can integrate with this workflow. These sub-sections contain elements that is subjected to change. It is not yet finalized because there are a variety of configurations that I want to include and I'm not sure if that would be useful.

### Required

These inputs are required in order to run the Docker Container.

| Inputs                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `WORKFLOW_TOKEN` | An auto-generated token for authentication use in order to make changes to the user's profile `README.md` .    |
| `DISCORD_USERNAME` | The user's discord username. Required as a target for the rich presence status lookup.    |

> Having of one them not included in your secrets will result in an error. If possible, the bot will send you a message about it in Discord.

### Optional

These inputs are optional and has the capability to override the display of the badge and the commit message.

To make ease with the usage of these optional inputs, please check the results of the table row for each command.

#### Output

| Input       | Type        | Description | Result |
| ----------- | ----------- | ----------- | ---------------------- |
| `CONTACTABLE_ON_CLICK`      | `bool`       | Allows viewers to click on the badge to PM the user.       | <!--RESULT:TEST_CASE:CONTACTABLE_ON_CLICK> |
| `OVERRIDE_DEFAULT_COLOR`   | `bool`        | Overrides default color of the badge.<br>**Ignores the status** of user. *(Online, AFK, DND, Offline)*        | <!--RESULT:TEST_CASE:OVERRIDE_DEFAULT_COLOR> |
| `HIDE_PRESENCE_STATE`   | `bool`        | Overrides default color of the badge.<br>**Ignores the status** of user. *(Online, AFK, DND, Offline)*        | <!--RESULT:TEST_CASE:HIDE_PRESENCE_STATE> |
| `SHOW_CUSTOM_STATUS_INSTEAD`   | `bool`        | Overrides default color of the badge.<br>**Ignores the status** of user. *(Online, AFK, DND, Offline)*        | <!--RESULT:TEST_CASE:SHOW_CUSTOM_STATUS_INSTEAD> |
| `SHOW_DETAIL_INSTEAD`   | `bool`        | Overrides default color of the badge.<br>**Ignores the status** of user. *(Online, AFK, DND, Offline)*        | <!--RESULT:TEST_CASE:SHOW_DETAIL_INSTEAD> |
| `SHOW_TIME_DURATION`   | `bool`        | Overrides default color of the badge.<br>**Ignores the status** of user. *(Online, AFK, DND, Offline)*        | <!--RESULT:TEST_CASE:SHOW_TIME_DURATION> |

#### Customizations

Sometimes, you might wanna do some flexibility on different cases of your status badge. The following parametes will help you do it.

| Inputs | Type | Description | Result |
| -------- | ----------- | -------- | ----------- |
| `OVERRIDE_MIN_PRESENCE_ONLINE_COLOR`  | `str` | To be constructed.    | <!--RESULT:TEST_CASE:OVERRIDE_MIN_PRESENCE_ONLINE_COLOR> |
| `OVERRIDE_MIN_PRESENCE_IDLE_COLOR` | `str` | To be constructed.    | <!--RESULT:TEST_CASE:OVERRIDE_MIN_PRESENCE_IDLE_COLOR> |
| `OVERRIDE_MIN_PRESENCE_DND_COLOR` | `str` | To be constructed.    | <!--RESULT:TEST_CASE:OVERRIDE_MIN_PRESENCE_DND_COLOR> |
| `OVERRIDE_MIN_PRESENCE_OFFLINE_COLOR` | `str` | To be constructed.    | <!--RESULT:TEST_CASE:OVERRIDE_MIN_PRESENCE_OFFLINE_COLOR> |
| `OVERRIDE_NO_PRESENCE_ONLINE_COLOR` | `str` | To be constructed.    | <!--RESULT:TEST_CASE:OVERRIDE_NO_PRESENCE_ONLINE_COLOR> |
| `OVERRIDE_NO_PRESENCE_IDLE_COLOR` | `str` | To be constructed.    | <!--RESULT:TEST_CASE:OVERRIDE_NO_PRESENCE_IDLE_COLOR> |
| `OVERRIDE_NO_PRESENCE_DND_COLOR` | `str` | To be constructed.    | <!--RESULT:TEST_CASE:OVERRIDE_NO_PRESENCE_DND_COLOR> |
| `OVERRIDE_NO_PRESENCE_OFFLINE_COLOR` | `str` | To be constructed.    | <!--RESULT:TEST_CASE:OVERRIDE_NO_PRESENCE_OFFLINE_COLOR> |

| `CUSTOM_NO_PRESENCE_ONLINE_STATUS` | `str` | To be constructed.    | <!--RESULT:TEST_CASE:CUSTOM_NO_PRESENCE_ONLINE_STATUS> |
| `CUSTOM_NO_PRESENCE_IDLE_STATUS` | `str` | To be constructed.    | <!--RESULT:TEST_CASE:CUSTOM_NO_PRESENCE_IDLE_STATUS> |

## Examples

Coming soon. But if you want to stay tuned, please check my [Github Profile](https://github.com/CodexLink/CodexLink) featuring it.

## Fequently Asked Questions

I will be making a FAQ or Wiki for some time in the future.

## Credits

Here contains a list of resources that I have used in any forms that contributed to the development of this repository.

### Technologies and Libraries Used

* [Act](https://github.com/nektos/act) — Run your GitHub Actions locally 🚀
* [Discord.py](https://github.com/Rapptz/discord.py) — An API wrapper for Discord written in Python.
* [PEP 8 Guidelines Tl; DR Version](https://realpython.com/python-pep8/#naming-conventions) — Huge thanks to [Jasmine Finer](https://github.com/jasminefiner) (who made the article) for TL; DR or compressed version of PEP 8 Guidelines.
* [Shields.io](https://shields.io/) — Concise, consistent, and legible badges in SVG and raster format.

### Guides, Article and Stackoverflow Questions

* https://pythonspeed.com/articles/base-image-python-docker-images/
* https://stackoverflow.com/questions/36342899/asyncio-ensure-future-vs-baseeventloop-create-task-vs-simple-coroutine
* https://stackoverflow.com/questions/66381035/docker-buildx-error-rpc-error-code-unknown-desc-server-message-insuffici

> This section is still incomplete, I will put more and format it later.

## License

  Copyright 2021 Janrey "CodexLink" Licas

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

  You may see the [LICENSE.md](https://github.com/CodexLink/discord-rich-presence-activity-badge/blob/main/LICENSE) file for more information.
