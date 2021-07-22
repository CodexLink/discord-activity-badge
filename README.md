<h1 align="center">Discord Activity Badge Action</h1>
<h4 align="center">A containerized action that bridges the Discord User's Activities and State  to a Representable Badge on their Special Repository (Github Profile). Powered by <b>Docker and Python + AsnycIO + discord.py + aiohttp.</b></h4>

<div align="center">

[![Open in Visual Studio Code](https://open.vscode.dev/badges/open-in-vscode.svg)](https://open.vscode.dev/CodexLink/discord-activity-badge/)
[![Container Tester](https://github.com/CodexLink/discord-activity-badge/actions/workflows/docker_test.yml/badge.svg)](https://github.com/CodexLink/discord-activity-badge/actions/workflows/docker_test.yml)
[![Containerization | Discord Rich Presence Activity Badge](https://github.com/CodexLink/discord-activity-badge/actions/workflows/docker_deploy.yml/badge.svg)](https://github.com/CodexLink/discord-activity-badge/actions/workflows/docker_deploy.yml)

[![Codacy Code Quality Grade](https://badgen.net/codacy/grade/42fcd1c143464a288522e236f929b1a8?icon=codacy&label=Codacy%20Code%20Quality)](https://app.codacy.com/gh/CodexLink/discord-activity-badge/dashboard)
[![CodeFactor Code Quality Grade](https://img.shields.io/codefactor/grade/github/CodexLink/discord-activity-badge?label=CodeFactor%20Code%20Quality&logo=codefactor)](https://www.codefactor.io/repository/github/codexlink/discord-activity-badge)
[![Repository License](https://img.shields.io/badge/Repo%20License-Apache%20License%202.0-blueviolet)](https://github.com/CodexLink/discord-activity-badge/blob/main/LICENSE)
</div>

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
    name: Static Badge Updater
    runs-on: ubuntu-latest

    steps:
      - name: Update README Discord Badge to Latest Upstream
      - uses: CodexLink/discord-activity-badge@main

        with:
          DISCORD_USER_ID: ${{ secrets.DISCORD_USER_ID }}
          DISCORD_BOT_TOKEN: ${{ secrets.DISCORD_BOT_TOKEN }}

```

> This workflow will run once it has been dispatched (manually) or is on scheduled to run for every **30 minutes per hour** to check for the user's status.

### Constraints

> To be added later.

## Parameters

The following sub-sections contain a set of possible inputs that you can integrate with this workflow. These sub-sections contain elements that is subjected to change. It is not yet finalized because there are a variety of configurations that I want to include and I'm not sure if that would be useful.

### Required

These inputs are required in order to run the Docker Container.

| Inputs                                               | Required? | Description                            |
|------------------------------------------------------|----|-----------------------------------------------|
| `COMMIT_MESSAGE` | `str` | User's Discord Rich Presence Updated, Badge Status Changed. | The commit message that the user wants to invoke whenever there's changes. | None, will include later. |
| `DISCORD_BOT_TOKEN` | `Yes` | The token of your bot from the Discord's Developer Page. It was used to allow usage of Discord API. |
| `DISCORD_USER_ID` | `Yes` | A long integer ID used to indicate who you are in a certain mutual guild. |
| `PROFILE_REPOSITORY` | `No` | The repository from where the commits will be pushed. Fill this when you are indirectly deploying the script under different repository. |
| `WORKFLOW_TOKEN` | `No` | The token of the Github Workflow Instance used to authenticate commits deployed by the script. Fill this when you are indirectly deploying the script under different repository. |
| `BADGE_IDENTIFIER_NAME` | `No` (defaults to `Discord Activity Badge`) | The name of the badge (in markdown form) that will be utilized to replace the state of the user. If the identifier does not exists, then it will proceed to create a new one and append it on the top. You must arranged it right after. |

> Having of one the requirements left out will result in an error. If possible, the bot will send you a message about it in Discord.

### Optional

These inputs are optional and has the capability to override the display of the badge and the commit message.

To make ease with the usage of these optional inputs, please check the results of the table row for each command.

#### Extensibility and Customization

The script offers extensibility and customization that allows you to render multiple ways of designing your badge.

##### User State

[![Example Online](https://badgen.net/badge/Discord%20Activity/Currently%20Online/green?icon=discord)](https://github.com/CodexLink/discord-activity-badge)
[![Example Idle](https://badgen.net/badge/Discord%20Activity/Currently%20Idle/yellow?icon=discord)](https://github.com/CodexLink/discord-activity-badge)
[![Example DND](https://badgen.net/badge/Discord%20Activity/Do%20Not%20Disturb/red?icon=discord)](https://github.com/CodexLink/discord-activity-badge)
[![Example Offline](https://badgen.net/badge/Discord%20Activity/Currently%20Offline/black?icon=discord)](https://github.com/CodexLink/discord-activity-badge)

> The string `Discord Activity`, Status Color and Discord Icon is changeable.

| Input       | Type        | Description | Result                 |
| ----------- | ----------- | ----------- | ---------------------- |
| `[ONLINE/IDLE/DND/OFFLINE]_PREFIX` | `str` *Defaults to*: **Currently** | The string to append **before** the `state`. | [![Demo 1](https://badgen.net/badge/Discord%20Activity/Was%20Online/green?icon=discord)](https://github.com/CodexLink/discord-activity-badge) |
| `[ONLINE/IDLE/DND/OFFLINE]_STATE` | `str` | Overrides the status output in ***online / idle / dnd / offline*** mode** states. | [![Demo 2](https://badgen.net/badge/Discord%20Activity/Current%20Away-From-Keyboard/yellow?icon=discord)](https://github.com/CodexLink/discord-activity-badge) |
| `[ONLINE/IDLE/DND/OFFLINE]_POSTFIX` | `str` *Defaults to*: **None** | The string to append **after** the `state`.  | [![Demo 3](https://badgen.net/badge/Discord%20Activity/Currently%20Online%20for%20a%While/green?icon=discord)](https://github.com/CodexLink/discord-activity-badge) |
| `[ONLINE/IDLE/DND/OFFLINE]_COLOR` | `str` ***HEX RGB only*** | Overrides the status color when the user is in ***online / idle / dnd / offline*** mode** states. | [![Demo 4](https://badgen.net/badge/Discord%20Activity/Currently%20Offline/D103FA?icon=discord)](https://github.com/CodexLink/discord-activity-badge)

> These are also applicable even when there's an activity. It will automatically invoke.

##### Activity States

[![Example #2](https://badgen.net/badge/Discord%20Activity/Playing%20Honkai%20Impact%203,%206%20hours%20elapsed./?icon=discord)](https://github.com/CodexLink/discord-activity-badge)
[![Example #3](https://badgen.net/badge/Discord%20Activity/Playing%20Honkai%20Impact%203,%206%20h%209m%20%20elapsed./green?icon=discord)](https://github.com/CodexLink/discord-activity-badge)
[![Example #4](https://badgen.net/badge/Discord%20Activity/Doing%20something%20for%20fun.%20%28Currently%20Away%29/yellow?icon=discord&labelColor=red)](https://github.com/CodexLink/discord-activity-badge)
[![Example #4](https://badgen.net/badge/Currently%20Away/Doing%20something%20for%20fun./yellow?icon=discord)](https://github.com/CodexLink/discord-activity-badge)
[![Example #5](https://badgen.net/badge/Discord%20Activity/Online/green?icon=discord)](https://github.com/CodexLink/discord-activity-badge)
[![Example #6](https://badgen.net/badge/Discord%20Activity/Online/green?icon=discord)](https://github.com/CodexLink/discord-activity-badge)
[![Example #7](https://badgen.net/badge/Discord%20Activity/Online/green?icon=discord)](https://github.com/CodexLink/discord-activity-badge)
[![Example #8](https://badgen.net/badge/Discord%20Activity/Online/green?icon=discord)](https://github.com/CodexLink/discord-activity-badge)
[![Example #9](https://badgen.net/badge/Discord%20Activity/Online/green?icon=discord)](https://github.com/CodexLink/discord-activity-badge)
[![Example #10](https://badgen.net/badge/Discord%20Activity/Online/green?icon=discord)](https://github.com/CodexLink/discord-activity-badge)
[![Example #11](https://badgen.net/badge/Discord%20Activity/Online/green?icon=discord)](https://github.com/CodexLink/discord-activity-badge)
[![Example #12](https://badgen.net/badge/Discord%20Activity/Online/green?icon=discord)](https://github.com/CodexLink/discord-activity-badge)
[![Example #13](https://badgen.net/badge/Discord%20Activity/Online/green?icon=discord)](https://github.com/CodexLink/discord-activity-badge)

| Input       | Type        | Description | Result                 |
| ----------- | ----------- | ----------- | ---------------------- |
| `APPEND_DETAIL_PRESENCE` | `bool` *Defaults to*: **False** | (**_Rich Presence Only!_**) Appends `detail` field to the Status Badge alongside with the application name. | Unavailable. |
| `APPEND_STATE_ON_SUBJECT` | `bool`  *Defaults to*: **False** | Overrides `Discord Activity` (Subject String) **and** User State with the state of `Playing`, `Watching`, `Listening`, this avoids making the status longer and balanced. If this is a `CustomActivity`, it will append User's State [online, idle, dnd, offline] instead. | Unavailable. |
| `PREFERRED_ACTIVITY` | `str` *Options*: [`ALL_ACTIVITIES`] | Renders a particular activity as a prioritized activity. If the preferred activity does not exist, it will render any activity by default. (**) | Unavailabe.
| `SHIFT_STATE_ACTIVITY_COLORS` | `str` | Interchange state and activity colors. This is useful only if you want to retain your state color position even though `APPEND_STATE_ON_SUBJECT` is true. | Unavailable. |
| `SHOW_TIME_DURATION` | `bool` *Defaults to*: **False** | Appends time after the application name or detail when `APPEND_DETAIL_PRESENCE` is **True**. | Unavailable. |
| `TIME_ELAPSED_OVERRIDE_STRING` | `str` *Default to*: **elapsed** | Overrides the string appended whenever the time is displayed for elapsed. This is effective only when SHOW_TIME_DURATION is **True**. | Unavailable. |
| `TIME_REMAINING_OVERRIDE_STRING` | `str` *Default to*: **remaining** | OVerrides the stringappended whenever the time is displayed for remaining. This is effective only when SHOW_TIME_DURATION is **True**. | Unvailable. |

**You got some ideas or did I miss something out? Please generate an issue or PR (if you have declared it on your own), and we will talk about it.**

> Support for other activities like **Spotify** may be evaluated later.
> ** For more information on how the script renders the badge based on preference, please check...

#### Development Parameters

When developing, there are other fields that shouldn't be used in the first place. Though they are helpful if you are planning to contribute or replicate the project.

| Input       | Type        | Default     | Description | Result                 |
| ----------- | ----------- | ----------- | ----------- | ---------------------- |
| `IS_DRY_RUN` | `bool` | `False` | Runs the usual process except it doesn't commit changes. | Unavailable. |

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
- https://stackoverflow.com/a/41766306/5353223
- https://stackoverflow.com/questions/41351346/python-asyncio-task-list-generation-without-executing-the-function (Helped me understand more of the use of as_completed.)
- https://stackoverflow.com/a/49710946/5353223 (After knowing the O of Time for `match()` vs `search()`)
- https://stackoverflow.com/questions/3603502/prevent-creating-new-attributes-outside-init

> This section is still incomplete. I will put more and format it later.

## License

```text
  Copyright 2021 Janrey "CodexLink" Licas

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0
```

  You may see the [LICENSE.md](https://github.com/CodexLink/discord-rich-presence-activity-badge/blob/main/LICENSE) file for more information.
