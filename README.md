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

**The script is not yet finished! (around 90% is done) This is just a notice!!!**

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

The following sub-topics pinpoints some things to consider before attempting to use this script.

### Rate Limits

As this script performs changes to the badge by static, we know that we might potentially abuse the API. We need to know some limitations and conclude the best minimum time update so that we won't get flagged.

As I further check some limitations from any of the APIs, here are the following restrictions upon request.

- 5000 Requests per hour (Github API).
- 50 Requests per Second (Discord API).

> There are no rate-limitations declared in badgen.net so far. Will further investigate.

### Method

This method (describes the script) shows the very cheap way to bridge our Discord to Github. There are many other ways that can made this quite easier but I don't want to spend some money (if I have a money). Plus, this is a pet project with the practice of committing to the development + practice of design patterns and formality (even when I'm alone).

## Parameters

The following sub-sections contain a set of possible inputs that you can integrate with this workflow. These sub-sections contain elements that is subjected to change. It is not yet finalized because there are a variety of configurations that I want to include and I'm not sure if that would be useful.

### Required (In-Need-of-Evaluation) Parameters

These inputs are required in order to run the Docker Container.

 Inputs   | Type + Defaults   | Description                            |
 -------- | :---------------: | -------------------------------------- |
`BADGE_IDENTIFIER_NAME` | `str`: Discord Activity Badge | The name of the badge (in markdown form) that will be utilized to replace the badge state's contents. If the identifier does not exists, it will proceed to create a new one and append it on the top of your README. **You must arranged it right after.**
`COMMIT_MESSAGE` | `str`: Discord Activity Badge Updated as of `datetime.datetime.now().strftime("%m/%d/%y — %I:%M:%S %p")` ***See constants.py:79 (_eval_date_on_exec)*** | The commit message that will be invoked in the commit context when there's are some changes to push.
`DISCORD_BOT_TOKEN` | `str` (**Required**) | The token of your bot from the Discord's Developer Page. Note that, you have to use your own bot! Go check [Discord Developers](https://discord.com/developers/).
`DISCORD_USER_ID` | `int` (**Required**) | An integer ID used to identify you in Discord. This does not associate your name and discriminator, so you are fine.
`PROFILE_REPOSITORY` | `str`: `GITHUB_ACTOR/GITHUB_ACTOR` | The repository from where the commits will be pushed. Fill this up  when you are indirectly deploying the script under different repository.
`URL_TO_REDIRECT_ON_CLICK` | `str`: `PROFILE_REPOSITORY` value. | The URL to point when the badge has been clicked. |
`WORKFLOW_TOKEN` | `str` (**Required**) | The token of the Github Workflow Instance used to authenticate commits deployed by the script. Fill this up if you want to test locally so that you aren't going to be rate limited.

> Parameters that is required has to be explicitly stated in the workflow. Not resolving these parameters will lead to an error.

> Regardless of the `types`, it will be resolved by the script, this is just an indicator that those will be explicitly converted to what has been told here.

### Optional Parameters

These inputs are optional and has the capability to override the display of the badge and the commit message. To make ease with the usage of these optional inputs, please check the results of the table row for each command.

#### Extensibility and Customization

The script offers extensibility and customization that allows you to render multiple ways of designing your badge.

##### Examples

The following badges are the base structure that will be utilized when further parameters are stated as enabled.
For every activity, there are lots of possible combinations that can be combined with the following configurations. Keep in mind that, if some badges failed to load, please reload again as the browser will cache the output on the next visit / reload. **Hard Reload** if persisting.

<div align="center">

[![Example Online](https://badgen.net/badge/Discord%20Activity/Currently%20Online/green?icon=discord)](https://github.com/CodexLink/discord-activity-badge)
[![Example Idle](https://badgen.net/badge/Discord%20Activity/Currently%20Idle/yellow?icon=discord)](https://github.com/CodexLink/discord-activity-badge)
[![Example DND](https://badgen.net/badge/Discord%20Activity/Do%20Not%20Disturb/red?icon=discord)](https://github.com/CodexLink/discord-activity-badge)
[![Example Offline](https://badgen.net/badge/Discord%20Activity/Currently%20Offline/black?icon=discord)](https://github.com/CodexLink/discord-activity-badge)
[![Example Playing Game Basic](https://badgen.net/badge/Discord%20Activity/Playing%20Honkai%20Impact%203,%206%20hours%20elapsed./green?icon=discord)](https://github.com/CodexLink/discord-activity-badge)
[![Example CustomActivity + State](https://badgen.net/badge/Discord%20Activity/Doing%20something%20for%20fun./purple?icon=discord&labelColor=red)](https://github.com/CodexLink/discord-activity-badge)
[![Example CustomActivity + State](https://badgen.net/badge/Currently%20Busy/Managing%20and%20Observing%20Crypto.../purple?icon=discord&labelColor=red)](https://github.com/CodexLink/discord-activity-badge)
[![Example NoSubjectColor + SubjectCustomized](https://badgen.net/badge/Currently%20Away/Doing%20something%20for%20fun./yellow?icon=discord)](https://github.com/CodexLink/discord-activity-badge)
[![Example Streaming + Idle + Detail + Elapsed + Shifted + CustomColor](https://badgen.net/badge/Currently%20Streaming/Visual%20Studio%20Code,%20Debugging%20entrypoint.py:1390,%2069%20minutes%20passed%20by./FA037F?icon=discord&labelColor=purple)](https://github.com/CodexLink/discord-activity-badge)
[![Example Busy + CustomActivity](https://badgen.net/badge/Currently%20Busy/Visual%20Studio%20Code,%20Editing%20README.md:115:124%20%28187%29/yellow?icon=discord&labelColor=red)](https://github.com/CodexLink/discord-activity-badge)
[![Example Offline + CustomSubject + CustomColor](https://badgen.net/badge/My%20Status/Currently%20Offline%20At%20This%20Point%20of%20Time./red?icon=discord)](https://github.com/CodexLink/discord-activity-badge)
[![Example BotStyle + Watching + Do-Not-Disturb + Elapsed + NotShifted + CustomColor](https://badgen.net/badge/Watching%20Data/Client%20WebSocket%20Server,%20Servicing%20People%20for%20about%201024%20Minutes!/blue?icon=discord&labelColor=green)](https://github.com/CodexLink/discord-activity-badge)
[![Example UpTimeBot + NoCustomColor](https://badgen.net/badge/ServerClient%20Discord/Currently%20Online.%20Servicing%202019%20Servers%20for%2089%20hours!/orange?icon=discord)](https://github.com/CodexLink/discord-activity-badge) <!-- ! I'm not sure if this is possible with the Bot's Presence. Will further investigate later. -->
[![Example Playing Game + CustomActivityColor](https://badgen.net/badge/Currently%20Playing%20Game/Honkai%20Impact%203,%206%20hours%20elapsed./CA8216?icon=discord&labelColor=green)](https://github.com/CodexLink/discord-activity-badge)

</div>

#### Colors and Intentions

If you wanna change the things on how it should be delivered (context) and how it should look like (color), then this set of parameters will help you modify the way how it looks. Keep in mind that the labels `[n]` in the parameters, where `n` is a number, is corresponding to a set of choices. Please see more info after the parameter description.
| Parameters    | Description + Result |
| :-----------: | :------------------: |
`str` `[1]_STRING` *Note*: **Each state (as options) is almost the same context from output to choices.** | Overrides `Discord Activity` (Subject String) **and** User State with the state of `Playing`, `Watching`, and `Listening` with ***custom strings***; this avoids making the status longer and balanced. If this is a `CustomActivity`, it will append User's State **[Online, Idle, DND, Offline]** instead.[![Demo #7](https://badgen.net/badge/Currently%20Playing/Visual%20Studio%20Code/green?icon=discord)](https://github.com/CodexLink/discord-activity-badge/)
`str` `[2]_STATUS_STRING` *Note*: **Please check fallback_values in elements/constants.py** | Overrides the status output in ***online / idle / dnd / offline*** states. [![Demo 2](https://badgen.net/badge/Discord%20Activity/Current%20Away-From-Keyboard/yellow?icon=discord)](https://github.com/CodexLink/discord-activity-badge)
`str` `[1]_COLOR` *Note*:***HEX RGB only*** | Renders status badge color whenever there's a certain activity. Which renders the user's state color in the subject, if a certain activity has color specified. Leaving these settings by default (None) will result to render the user's state color. **See example of `APPEND_STATE_ON_SUBJECT`**. That should ignore `SHIFT_STATE_ACTIVITY_COLOR` if that is the case. [![Demo #7](https://badgen.net/badge/Currently%20Streaming/Visual%20Studio%20Code/purple?icon=discord&labelColor=green)](https://github.com/CodexLink/discord-activity-badge)
`str` `[2]_STATUS_COLOR` *Note*: ***HEX RGB only*** | Overrides the status color when the user is in ***online / idle / dnd / offline*** states. [![Demo 4](https://badgen.net/badge/Discord%20Activity/Currently%20Offline/D103FA?icon=discord)](https://github.com/CodexLink/discord-activity-badge)
`str` `STATIC_SUBJECT_STRING` *Defaults to*: **None** | Statically declare a certain string to display on the subject. If declared, ***[]_ACTIVITY_STRING and []_STATUS_STRING*** will be ignored. [![Demo ?](https://badgen.net/badge/Discord%20Activity/Playing%20Honkai%20Impact%203/green?icon=discord)](https://github.com/CodexLink/discord-activity-badge)

> 1. Options: ***CUSTOM_ACTIVITY***, ***GAME_ACTIVITY***, ***RICH_PRESENCE***, ***STREAM_ACTIVITY***, and ***UNSPECIFIED_ACTIVITY***.
> 2. Options: ***ONLINE***, ***IDLE***, ***DND***, and ***OFFLINE***.

*I separated the options along with the parameter to avoid confusion while reading it.*

#### Context

Whenever you want to change the context of the badge, you can use this set of parameters for extending the context or shorten it.

| Parameters    | Description + Result |
| :-----------: | :------------------: |
`str` `PREFERRED_PRESENCE_CONTEXT` *Options*: *[***DETAILS***, STATE, CONTEXT_DISABLED]* | Overrides additional information to append in the badge. So far, only`DETAILS` and`STATE` are allowed to be appended since it shows the other context of the application.
`str` `TIME_DISPLAY_OUTPUT` *Options*: *[**TIME_DISABLED**, HOURS, HOURS_MINUTES, MINUTES, SECONDS]* | Appends time (based on preference) after the application name or detail when `APPEND_PRESENCE_CONTEXT` is **True**. [![Demo #8](https://badgen.net/badge/Currently%20Playing/Visual%20Studio%20Code,%206%20hours%20Elapsed./green?icon=discord)](https://github.com/CodexLink/discord-activity-badge)
`str` `TIME_DISPLAY_ELAPSED_OVERRIDE_STRING` *Defaults to*: **elapsed.** | Overrides the string appended whenever the time is displayed for elapsed. This is effective only when SHOW_TIME_DURATION is **True**. [![Demo #9](https://badgen.net/badge/Currently%20Playing/Visual%20Studio%20Code,%206%20hours%20and%20counting./green?icon=discord)](https://github.com/CodexLink/discord-activity-badge) |
`str` `TIME_DISPLAY_REMAINING_OVERRIDE_STRING` *Defaults to*: **remaining.** | Overrides the string appended whenever the time is displayed for remaining. This is effective only when `TIME_TO_DISPLAY` is **True**. [![Demo #10](https://badgen.net/badge/Currently%20Playing/Visual%20Studio%20Code,%206%20hours%209%20minutes%20to%20finish./green?icon=discord)](https://github.com/CodexLink/discord-activity-badge)
`bool` `TIME_DISPLAY_SHORTHAND` *Defaults to*: **False** | Displays the time with **hours** and **minutes** shorthanded to **h** and **m**. [![Demo #9](https://badgen.net/badge/Currently%20Playing/Visual%20Studio%20Code,%206%20h./green?icon=discord)](https://github.com/CodexLink/discord-activity-badge) |

#### Preferences

| Parameters  | Description + Result |
| :-----------: | :----------------: |
`str` `PREFERRED_ACTIVITY_TO_DISPLAY` *Options*: *[CUSTOM_ACTIVITY, GAME_ACTIVITY, **RICH_PRESENCE**, STREAM_ACTIVITY, UNSPECIFIED_ACTIVITY]* | Renders a particular activity as a prioritized activity. If the preferred activity does not exist, it will render any activity by default. **There will be no demo since it only picks what activity should be displayed.**
`bool` `SHIFT_STATE_ACTIVITY_COLORS` *Defaults to*: **False** | Interchange state and activity colors. This is useful only if you want to retain your state color position even though `APPEND_STATE_ON_SUBJECT` is true. [![Example #8](https://badgen.net/badge/Currently%20Streaming/Visual%20Studio%20Code/green?icon=discord&labelColor=purple)](https://github.com/CodexLink/discord-activity-badge)
`str (char)` `STATUS_CONTEXT_SEPERATOR` *Defaults to*: **`,`** | The character/s that seperates the context of every status elements. Keep note that, once you declared a value on this parameter, it will automatically adds space from both ends to ensure that the content displays properly. If otherwise, the script will do the spacing on its own. [![Example #8](https://badgen.net/badge/Currently%20Playing/Visual%20Studio%20Code%20%7C%20Idling%20In%20Workspace%20%7C%207%20hours%20elapsed./green?icon=discord&labelColor=yellow)](https://github.com/CodexLink/discord-activity-badge)

**You got some ideas or did I miss something out? Please generate an issue or PR (if you have declared it on your own), and we will talk about it.**

> Support for other activities like **Spotify** may be evaluated later.
> For more information on how the script renders the badge based on preferences, please check...

#### Development Parameters

When developing, there are other fields that shouldn't be used in the first place. Though they are helpful if you are planning to contribute or replicate the project.

| Parameters    | Type        | Default     | Description |
| -----------   | ----------- | ----------- | ----------- |
| `IS_DRY_RUN`  | `bool` | `False` | Runs the usual process but it doesn't commit changes. |

## Beyond Examples: Usage

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
- https://stackoverflow.com/questions/41351346/python-asyncio-task-list-generation-without-executing-the-method (Helped me understand more of the use of as_completed.)
- https://stackoverflow.com/a/49710946/5353223 (After knowing the O of Time for `match()` vs `search()`)
- https://stackoverflow.com/questions/3603502/prevent-creating-new-attributes-outside-init
- https://material.io/design/color/the-color-system.html#tools-for-picking-colors
- https://www.epochconvert.com/
- https://stackoverflow.com/a/18472142/5353223
- https://stackoverflow.com/a/624939/5353223
- https://stackoverflow.com/a/41766306/5353223
- https://stackoverflow.com/a/11743262/5353223
- https://stackoverflow.com/questions/9437726/how-to-get-the-value-of-a-variable-given-its-name-in-a-string
- https://stackoverflow.com/a/18470628/5353223
- https://stackoverflow.com/a/51191130/5353223
- https://stackoverflow.com/a/65359924/5353223
- https://stackoverflow.com/questions/33128325/how-to-set-class-attribute-with-await-in-init.
- https://stackoverflow.com/questions/9575409/calling-parent-class-init-with-multiple-inheritance-whats-the-right-way/55583282#55583282
- https://blog.baeke.info/2021/04/09/building-a-github-action-with-docker/
- https://dev.to/dtinth/caching-docker-builds-in-github-actions-which-approach-is-the-fastest-a-research-18ei
- https://github.com/dtinth/github-actions-docker-layer-caching-poc
- https://sodocumentation.net/regex/topic/9852/substitutions-with-regular-expressions
- https://stackoverflow.com/questions/14007545/python-regex-instantly-replace-groups
- https://stackoverflow.com/questions/15340582/python-extract-pattern-matches
- https://stackoverflow.com/a/606199/5353223
- https://stackoverflow.com/a/27529806/5353223
- https://stackoverflow.com/a/22636121/5353223

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
