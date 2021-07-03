<h1 align="center">Discord Rich Presence to Github Profile Badge</h1>
<h4 align="center">A dockerize-able application containing Discord Client, Bot and, Flask API Server for serving badged rich presence based from their activities.</h4>

<div align="center">

![Codacy Grade](https://img.shields.io/codacy/grade/d2da8866a48145be8c330a9056b35743?label=Codacy%20Grade&logo=codacy)
[![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/CodexLink/dquerybotboilerplate?label=CodeFactor%20Grade&logo=codefactor)](https://www.codefactor.io/repository/github/codexlink/dquerybotboilerplate)
[![Repository License](https://img.shields.io/badge/Repo%20License-Apache%20License%202.0-blueviolet)](https://github.com/CodexLink/discord-rich-presence-activity-badge/blob/main/LICENSE)
</div>

## Welcome

To be constructed.

## Usage

To be constructed.

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

      - name: Step 1 | Repository Checkout
      - uses: actions/checkout@master

      - name: Step 2 | Update README Discord Badge to Latest Upstream
      - uses: CodexLink/discord-rich-presence-activity-badge@main

        with:
          # These are required inputs.
          # More information on README - Parameters Section.
          WORKFLOW_INSTANCE_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          DISCORD_USERNAME: ${{ secrets.DISCORD_USERNAME }}
          DISCORD_USERNAME_TAG: ${{ secrets.DISCORD_USERNAME_TAG }}
          OVERRIDE_COMMIT_MESSAGE: 'Discord Activity Reading Finished.'

```

> This workflow will work once it has been dispatched (manually), and is on set, to iterate every **30 minutes per hour** to check for the user's status.


### Parameters

In this section, it contains the required inputs along with customization parameters which are optional.

#### Required Inputs

***The following are the initial possible of required inputs.***

These inputs are required in order to run the Docker Container or the action workflow that you referred, which is this repo.

| Inputs                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `WORKFLOW_TOKEN` | An auto-generated token for authentication use in order to make changes to the user's profile `README.md` .    |
| `DISCORD_USERNAME` | The user's discord username. Required as a target for the rich presence status lookup.    |
| `DISCORD_USERNAME_TAG` | The user's discord unique tag. `Required` as there are other instance were you have a same username to other users.   |

#### Optional Inputs

These inputs are optional and has the capability to override the display of the badge and the commit message.

To make ease with the usage of these optional inputs, please check the results of the table row for each command.

***To be utilized in latter cases.***

| Input       | Type        | Description | Result |
| ----------- | ----------- | ----------- | ---------------------- |
| `CONTACTABLE_ON_CLICK`      | `bool`       | Allows viewers to click on the badge to PM the user.       | <!--RESULT:TEST_CASE:CONTACTABLE_ON_CLICK> |
| `OVERRIDE_DEFAULT_COLOR`   | `bool`        | Overrides default color of the badge.<br>**Ignores the status** of user. *(Online, AFK, DND, Offline)*        | <!--RESULT:TEST_CASE:OVERRIDE_DEFAULT_COLOR> |
| `HIDE_PRESENCE_STATE`   | `bool`        | Overrides default color of the badge.<br>**Ignores the status** of user. *(Online, AFK, DND, Offline)*        | <!--RESULT:TEST_CASE:HIDE_PRESENCE_STATE> |
| `SHOW_CUSTOM_STATUS_INSTEAD`   | `bool`        | Overrides default color of the badge.<br>**Ignores the status** of user. *(Online, AFK, DND, Offline)*        | <!--RESULT:TEST_CASE:SHOW_CUSTOM_STATUS_INSTEAD> |
| `SHOW_DETAIL_INSTEAD`   | `bool`        | Overrides default color of the badge.<br>**Ignores the status** of user. *(Online, AFK, DND, Offline)*        | <!--RESULT:TEST_CASE:SHOW_DETAIL_INSTEAD> |
| `SHOW_TIME_DURATION`   | `bool`        | Overrides default color of the badge.<br>**Ignores the status** of user. *(Online, AFK, DND, Offline)*        | <!--RESULT:TEST_CASE:SHOW_TIME_DURATION> |

#### No Presence or Minimal Presence Customization

Sometimes, you might wanna do some flexibility on different cases of your status badge. The following table might help you do it.

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
| `CUSTOM_NO_PRESENCE_DND_STATUS` | `str` | To be constructed.    | <!--RESULT:TEST_CASE:CUSTOM_NO_PRESENCE_DND_STATUS> |
| `CUSTOM_NO_PRESENCE_OFFLINE_STATUS` | `str` | To be constructed.    | <!--RESULT:TEST_CASE:CUSTOM_NO_PRESENCE_OFFLINE_STATUS> |

<!-- | Parameters                                             | Result                                        |
|------------------------------------------------------|-----------------------------------------------|
| `CONTACTABLE_ON_CLICK` | To be constructed.    |
| ``   | To be constructed.    | -->

## Examples

Coming soon.


## Credits

* [Act](https://github.com/nektos/act) — Run your GitHub Actions locally 🚀
* [Discord.py](https://github.com/Rapptz/discord.py) — An API wrapper for Discord written in Python.
* [PEP 8 Guidelines Tl; DR Version](https://realpython.com/python-pep8/#naming-conventions) — Huge thanks to [Jasmine Finer](https://github.com/jasminefiner) (who made the article) for TL; DR or compressed version of PEP 8 Guidelines.
* [Shields.io](https://shields.io/) — Concise, consistent, and legible badges in SVG and raster format.
https://pythonspeed.com/articles/base-image-python-docker-images/
https://stackoverflow.com/questions/36342899/asyncio-ensure-future-vs-baseeventloop-create-task-vs-simple-coroutine

## License

  Copyright 2021 Janrey "CodexLink" Licas

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

  You may see the [LICENSE.md](https://github.com/CodexLink/discord-rich-presence-activity-badge/blob/main/LICENSE) file for more information.