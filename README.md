<h1 align="center">Discord Rich Presence Activity Badge Action</h1>
<h4 align="center">A containerized action that bridges the Discord User's Rich Presence to a Presentable Badge on their Special Repository (Github Profile). Powered by <b>Python + Asnycio + discord.py</b></h4>

<div align="center">

[![Container Tester](https://github.com/CodexLink/discord-rich-presence-activity-badge/actions/workflows/docker_test.yml/badge.svg)](https://github.com/CodexLink/discord-rich-presence-activity-badge/actions/workflows/docker_test.yml)
[![Containerization | Discord Rich Presence Activity Badge](https://github.com/CodexLink/discord-rich-presence-activity-badge/actions/workflows/docker_deploy.yml/badge.svg)](https://github.com/CodexLink/discord-rich-presence-activity-badge/actions/workflows/docker_deploy.yml)

[![Codacy Code Quality Grade](https://badgen.net/codacy/grade/42fcd1c143464a288522e236f929b1a8?icon=codacy&label=Codacy%20Code%20Quality)](https://app.codacy.com/gh/CodexLink/discord-rich-presence-activity-badge/dashboard)
[![CodeFactor Code Quality Grade](https://img.shields.io/codefactor/grade/github/CodexLink/discord-rich-presence-activity-badge?label=CodeFactor%20Code%20Quality&logo=codefactor)](https://www.codefactor.io/repository/github/codexlink/discord-rich-presence-activity-badge)
[![Repository License](https://img.shields.io/badge/Repo%20License-Apache%20License%202.0-blueviolet)](https://github.com/CodexLink/discord-rich-presence-activity-badge/blob/main/LICENSE)
</div>

## Development: What's missing?

To give you an overview, here is the list that contain implementations and tasks that I haven't started yet.

- Badge Constructor and Validator
- Arguments (Both Optional and Required)
- README Modifier
- Git Commit and Push as User

> The list will be updated as I push possible changes.

TL;DR: Semi-usable but cannot be used **as-is** due to components missing.

## Usage

To be constructed later.

### Workflow

Paste the following `YAML` on profile repository under directory `.github/workflows`.

``` yaml
name: Discord Rich Presence Activity Badge

on:
  schedule:
    - cron: "30 0-23 * * *" # This is customizable, At minute 30 past every hour from 0 through 23.

  workflow_dispatch:

jobs:
  BadgeUpdater:
    name: Discord Activity Static Badge Updater
    runs-on: ubuntu-latest

    steps:
      - name: Update README Discord Badge to Latest Upstream
      - uses: CodexLink/discord-rich-presence-activity-badge@main

        with:
          DISCORD_USER_ID: ${{ secrets.DISCORD_USER_ID }}
          DISCORD_BOT_TOKEN: ${{ secrets.DISCORD_BOT_TOKEN }}
          WORKFLOW_TOKEN: ${{ secrets.GITHUB_TOKEN }}

```

> This workflow will run once it has been dispatched (manually) or is on scheduled to run for every **30 minutes per hour** to check for the user's status.

### Constraints

[... Mention about the possible limitations to avoid abuse of this tool. ]

## Parameters

The following sub-sections contain a set of possible inputs that you can integrate with this workflow. These sub-sections contain elements that is subjected to change. It is not yet finalized because there are a variety of configurations that I want to include and I'm not sure if that would be useful.

### Required

These inputs are required in order to run the Docker Container.

| Inputs                                               | Description                                   |
|------------------------------------------------------|-----------------------------------------------|
| `WORKFLOW_TOKEN` | An auto-generated token for authentication use in order to make changes to the user's profile `README.md` .    |
| `DISCORD_USERNAME` | The user's discord username. Required as a target for the rich presence status lookup.    |

> Having of one them not included in your secrets will result in an error. If possible, the bot will send you a message about it in Discord.

### Optional

These inputs are optional and has the capability to override the display of the badge and the commit message.

To make ease with the usage of these optional inputs, please check the results of the table row for each command.

#### Extensibility and Customization

These parameters are extensible that may help you customize the base output of the badge.

| Input       | Type        | Default     | Description | Result                 |
| ----------- | ----------- | ----------- | ----------- | ---------------------- |
| `ALLOW_PM_ON_CLICK` | `bool` | `False` | Allows viewers to click on the badge to PM the user. Be careful if enabled. This exposes your Discord ID. (**not token!**) | [![Discord Me](https://badgen.net/badge/Discord/CodexLink%205848/7289DA?logo=discord&scale=3)](https://discord.com/channels/@me/799166063753035776) |
| `APPEND_DETAIL_PRESENCE` | `bool` | `False` | Appends `Detail` field to the Badge. | Unavailable. |
| `SHOW_HOURS_MINUTES_ELAPSED` | `bool` | `False` | Allows to display hours and minutes, instead of hours only. | Unavailable. |
| `SHOW_OTHER_STATUS` | `bool` | `False` | Allows other activities (such as game, stream, custom, etc) to display if Rich Presence is not present. | Unavailable. |
| `SHOW_TIME_DURATION` | `bool` |`False` | Enables `SHOW_OTHER_STATUS` and Rich Presence to be shown in the badge aside from User State. | Unavailable. |

#### Badge Customizations

Sometimes, you might wanna do some customizaion on different cases of your status badge. The following parameters will help you do it.

| Input       | Type        | Description | Result                 |
| ----------- | ----------- | ----------- | ---------------------- |
| `NO_ACTIVITY_[ONLINE/DND/AFK/OFFLINE]_STATUS` | `str` | Overrides the status badge whenever there's no activity is present. | Unavailable. |
| `STATE_[ONLINE/DND/AFK/OFFLINE]_COLOR` | `str` | Overrides the color of the status (right) badge for whatever the state of user is. **This will take effect if there's no rich presence | Unavaialble. |

**You got some ideas? Please generate an issue or PR, and we will talk about it.**

> Support for other acitivities like Spotify will be evaluated later.

#### Development Parameters

When developing, there are other fields that shouldn't be used in the first place. Though they are helpful.

| Input       | Type        | Default     | Description | Result                 |
| ----------- | ----------- | ----------- | ----------- | ---------------------- |
| `SHOULD_DRY_RUN` | `bool` | `False` | Overrides the status badge whenever there's no activity is present. | Unavailable. |
| `DO_NOT_SEND_ERR_REPORTS` | `bool` | `False` | Enables/Disables the Discord Client to send error reports to you. | None. |

## Examples

Coming soon. But if you want to stay tuned, please check my [Github Profile](https://github.com/CodexLink/CodexLink) featuring it.

> First 10 to 20 will be displayed here. Please PR and we will include your profile.

## Fequently Asked Questions

I will be making a FAQ or Wiki for some time in the future.

## Credits

Here contains a list of resources that I have used in any forms that contributed to the development of this repository.

### Technologies and Libraries Used

- [Discord.py](https://github.com/Rapptz/discord.py) — An API wrapper for Discord written in Python.
- [PEP 8 Guidelines Tl; DR Version](https://realpython.com/python-pep8/#naming-conventions) — Huge thanks to [Jasmine Finer](https://github.com/jasminefiner) (who made the article) for TL; DR or compressed version of PEP 8 Guidelines.
<!-- * [Shields.io](https://shields.io/) — Concise, consistent, and legible badges in SVG and raster format. -->

### Guides, Article and Stackoverflow Questions

- https://pythonspeed.com/articles/base-image-python-docker-images/
- https://stackoverflow.com/questions/36342899/asyncio-ensure-future-vs-baseeventloop-create-task-vs-simple-coroutine
- https://stackoverflow.com/questions/66381035/docker-buildx-error-rpc-error-code-unknown-desc-server-message-insuffici

> This section is still incomplete, I will put more and format it later.

## License

```text
  Copyright 2021 Janrey "CodexLink" Licas

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0
```

  You may see the [LICENSE.md](https://github.com/CodexLink/discord-rich-presence-activity-badge/blob/main/LICENSE) file for more information.
