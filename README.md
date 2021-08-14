<div align="center">
<h1> Discord Activity Badge <code>(Initial Release)🌇</code></h1>
  
  
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

<h4>A containerized action that bridges the Discord User's Activity and their Status State to a Representable Badge for their Special Repository (Github Profile) and soon, for open-sourced Discord Bots.</h4>
<h4><b>Powered by Docker and Python + AsyncIO + discord.py + aiohttp.</b></h4>

[![Container Tester](https://github.com/CodexLink/discord-activity-badge/actions/workflows/docker_test.yml/badge.svg)](https://github.com/CodexLink/discord-activity-badge/actions/workflows/docker_test.yml)
[![Containerization | Discord Activity Badge](https://github.com/CodexLink/discord-activity-badge/actions/workflows/docker_deploy.yml/badge.svg)](https://github.com/CodexLink/discord-activity-badge/actions/workflows/docker_deploy.yml)
[![LGTM Alerts](https://badgen.net/lgtm/alerts/g/CodexLink/discord-activity-badge/python?icon=lgtm&label=LGTM%20Alerts)](https://lgtm.com/projects/g/CodexLink/discord-activity-badge)

[![Codacy Code Quality Grade](https://badgen.net/codacy/grade/42fcd1c143464a288522e236f929b1a8/latest?icon=codacy&label=Codacy%20Code%20Quality)](https://app.codacy.com/gh/CodexLink/discord-activity-badge/dashboard)
[![CodeFactor Code Quality Grade](https://img.shields.io/codefactor/grade/github/CodexLink/discord-activity-badge/latest?label=CodeFactor%20Code%20Quality&logo=codefactor)](https://www.codefactor.io/repository/github/codexlink/discord-activity-badge)
[![LGTM Code Quality](https://badgen.net/lgtm/grade/g/CodexLink/discord-activity-badge/python?icon=lgtm&label=LGTM%20Code%20Quality)](https://lgtm.com/projects/g/CodexLink/discord-activity-badge)
[![LGTM Calculated Line of Code](https://badgen.net/lgtm/lines/g/CodexLink/discord-activity-badge/python?icon=lgtm&label=Code%20Lines%20%28Python%29)](https://lgtm.com/projects/g/CodexLink/discord-activity-badge)

[![Open in Visual Studio Code](https://open.vscode.dev/badges/open-in-vscode.svg)](https://open.vscode.dev/CodexLink/discord-activity-badge/)
[![Repository License](https://img.shields.io/badge/Repo%20License-Apache%20License%202.0-blueviolet)](https://github.com/CodexLink/discord-activity-badge/blob/main/LICENSE)

</div>

## Why?

**Because why not?** If you ever wanted to show your status with context aside from your Github Status, or wanting to go beyond styling your README by adding some extra toppings, or wanting to let some birds (strangers) know what you are doing at some point in time, then this action workflow might be for you!

## What it can do and what does it contain?

* Containerized with Docker and Cached with Buildx (in Github Actions)
* Contains Discord Client Handler
* Contains Custom Async Rewrite based on PyGithub
* It can run locally and Remote with Github Actions (ONLY)
* Python Code Annotated and Typed, Implemented under Async
* String Manipulation and Logic for Badge Construction
* Customizable Badge Output and others
* With Dependency Management, Poetry
* Utility functions that can be reusable, and etc.

## Steps

The following contains the steps needed to make this action work properly. Keep in mind that this is quite hectic but easy, the steps were alot because this is the cheapest way to do this thing.

* Creating a Bot and obtaining its Token in Discord Developers
* Inviting the Bot to a Guild
* Preparing the Workflow
* Repository Secrets
* Workflow Dispatch

### Creating a Bot and obtaining its Token in Discord Developers

Ever since I don't provide anything such as the Bot that I use for reading my activities, you have to make it on your own. You can go to [Discord Developers](https://discord.com/developers/) and start ahead by creating a new application.

<div align="center">
  
[![Image 1](https://github.com/CodexLink/discord-activity-badge/blob/latest/img/1.png)](https://github.com/CodexLink/discord-activity-badge/)

</div>
  
Once you have created a new application, you have to go to the sidebar or menu and go to the **Bot settings**, and add a bot. And then, copy the token and store it somewhere temporarily as we are going to use it later on in the next two steps.

[![Image 2](https://github.com/CodexLink/discord-activity-badge/blob/latest/img/2.gif)](https://github.com/CodexLink/discord-activity-badge/)

As a side note, you have to enable the presence and server members intent **on the same settings (Bot settings)** to allow your bot to read your presence context and the members' states and other kinds of stuff about them.

[![Image 3](https://github.com/CodexLink/discord-activity-badge/blob/latest/img/3.png)](https://github.com/CodexLink/discord-activity-badge/)

*Don't forget to save before proceeding to the next step!!!*

### Inviting the Bot to a Guild

***Inviting the bot and having them in the guild is the only way to read User's Presence and their State, as per the limitation of Discord API.***

Keep in mind that, you can either **create your own guild** or have someone else let the bot join on their guild **as long as you are there**.

To invite, you have to go to the **OAuth2** settings and check the **OAuth2 URL Generator**. Look for **Bot** scope and check it, you will be given a generated link.

[![Image 4, GIF](https://github.com/CodexLink/discord-activity-badge/blob/latest/img/4.gif)](https://github.com/CodexLink/discord-activity-badge/)

Once you have the link, you just have to paste it into the browser and open it.

[![Image 5, GIF](https://github.com/CodexLink/discord-activity-badge/blob/latest/img/5.gif)](https://github.com/CodexLink/discord-activity-badge/)

<div align="center">

[![Image 6](https://github.com/CodexLink/discord-activity-badge/blob/latest/img/6.png)](https://github.com/CodexLink/discord-activity-badge/)

</div>
  
And there you have it! Once you have done this part, the only thing left is to have a workflow in your repository.

### Preparing the Workflow

Paste the following `YAML` on your (profile) repository under the directory `.github/workflows` and commit it.

``` yaml
name: Discord Rich Presence Activity Badge

on:
  schedule:                 # Scheduling with Github Actions is inconsistent.
    - cron: "5 0-23 * * *" # Construct your Cronjob Schedule at https://crontab.guru/.

  workflow_dispatch:        # Enables you to dispatch the workflow at your click.

jobs:
  BadgeUpdater:
    name: Static Badge Updater
    runs-on: ubuntu-latest

    steps:
      - name: Update README Discord Badge to Latest Upstream
        uses: CodexLink/discord-activity-badge@cutting-edge # Choose your own version by picking a tag or a branch name.
        with: # Go to your Repository Secrets and fill those up!
          DISCORD_USER_ID: ${{ secrets.DISCORD_USER_ID }}
          DISCORD_BOT_TOKEN: ${{ secrets.DISCORD_BOT_TOKEN }}

```

> This workflow will run once it has been dispatched (manually) or is scheduled to run for every **5 minutes per 0 to 23 hours** to check for the user's status.

### Repository Secrets

To be able to provide your information, you have to go to your repository > Settings > Secrets > New Repository.

[![Image 7](https://github.com/CodexLink/discord-activity-badge/blob/latest/img/7.png)](https://github.com/CodexLink/discord-activity-badge/)

In the end, you should have these two repository secrets. The token is from the one that we obtained in the Discord Developers Section, and the one is from you yourself in the Discord Client.

**DISCORD_USER_ID** can be obtained by the following.

[![Image 8, GIF](https://github.com/CodexLink/discord-activity-badge/blob/latest/img/8.gif)](https://github.com/CodexLink/discord-activity-badge/)

### Workflow Dispatch

When you finished all the steps, the last thing to do was to manually push it to see changes.

[![Image 9](https://github.com/CodexLink/discord-activity-badge/blob/latest/img/9.png)](https://github.com/CodexLink/discord-activity-badge/)

### Post-Step, Moving the Badge

If you did the run for the first time, the badge will tend to append on the top of your README, you can adjust it to somewhere else and the badge will be replaced by the script, no matter where it is.

<div align="center">

[![Image 10 (A)](https://github.com/CodexLink/discord-activity-badge/blob/latest/img/A.png)](https://github.com/CodexLink/discord-activity-badge/)

</div>

And that's done! For further customizations, please read the other sub-sections below.

## Workflow Parameters

The following sub-sections contain a set of possible inputs that you can integrate with this workflow.

### Required (In-Need-of-Evaluation) Parameters

These inputs are required in order to run the Docker Container.

 Inputs   | Type + Defaults   | Description
 -------- | :---------------: | --------------------------------------
`BADGE_IDENTIFIER_NAME` | `str`: (Script) Discord Activity Badge | The name of the badge (in markdown form) that will be utilized to replace the badge state side's contents. If the identifier does not exist, it will proceed to create a new one and append it on the top of your README. **You must arrange it right after.**
`COMMIT_MESSAGE` | `str`: Discord Activity Badge Updated as of `datetime.datetime.now().strftime("%m/%d/%y — %I:%M:%S %p")` ***See constants.py | The commit message that will be invoked in the commit context when there's are some changes to push.
`DISCORD_BOT_TOKEN` | `str` (**Required**) | The token of your bot from Discord's Developer Page. Note that, you have to use your own bot! Go check [Discord Developers](https://discord.com/developers/).
`DISCORD_USER_ID` | `int` (**Required**) | An integer ID used to identify you in Discord.
`PROFILE_REPOSITORY` | `str`: `GITHUB_ACTOR/GITHUB_ACTOR` | The repository from where the commits will be pushed. Fill this up when you are indirectly deploying the script under a different repository.
`URL_TO_REDIRECT_ON_CLICK` | `str`: `PROFILE_REPOSITORY` value. | The URL to point when the badge has been clicked.
`WORKFLOW_TOKEN` | `str` (**Required**) | The token of the Github Workflow Instance used to authenticate commits deployed by the script. Fill this up if you want to test locally so that you aren't going to be rate limited. **Using user-generated token can give 5000 API requests**!

> Parameters that are `required` have to be explicitly stated in the workflow. Otherwise, it will lead to an error.
> Regardless of the `types`, it will be resolved by the script, this is just an indicator that those will be explicitly converted to what has been told here.

### Optional Parameters

These inputs are optional and have the capability to override the display of the badge and the commit message. Allowing extensibility and customization that allows you to render multiple ways of designing your badge.

#### Colors and Intentions

If you wanna change how things should be delivered (context) and how they should look like (color), then this set of parameters will help you modify the way how it looks. Keep in mind that the labels `[n]` in the parameters is a number, and is corresponding to a set of choices. Please check the options under the table.

| Parameters    | Description + Result |
| :-----------: | :------------------: |
`str` `[1]_STRING` *Note*: **Each state (as options) is almost the same context from output to choices.** | Overrides `Discord Activity` (Subject String) **and** User State with the state of `Playing`, `Watching`, and `Listening` with ***custom strings***; this avoids making the status longer and balanced. If this is a `CustomActivity`, it will append User's State **[Online, Idle, DND, Offline]** instead. </br></br> [![Demo #1](https://badgen.net/badge/Currently%20Playing/Visual%20Studio%20Code/green?icon=discord)](https://github.com/CodexLink/discord-activity-badge/)
`str` `[2]_STATUS_STRING` *Note*: **Please check fallback_values in elements/constants.py** | Overrides the status output in ***online / idle / dnd / offline*** states. </br></br> [![Demo #2](https://badgen.net/badge/Discord%20Activity/Current%20Away-From-Keyboard/yellow?icon=discord)](https://github.com/CodexLink/discord-activity-badge)
`str` `[1]_COLOR` *Note*:***HEX RGB only*** | Renders status badge color whenever there's a certain activity. Which renders the user's state color in the subject, if a certain activity has color specified. Leaving these settings by default (None) will result to render the user's state color. **See example of `APPEND_STATE_ON_SUBJECT`**. That should ignore `SHIFT_STATE_ACTIVITY_COLOR` if that is the case. </br></br> [![Demo #3](https://badgen.net/badge/Currently%20Streaming/Visual%20Studio%20Code/purple?icon=discord&labelColor=green)](https://github.com/CodexLink/discord-activity-badge)
`str` `[2]_STATUS_COLOR` *Note*: ***HEX RGB only*** | Overrides the status color when the user is in ***online / idle / dnd / offline*** states. </br></br> [![Demo #3](https://badgen.net/badge/Discord%20Activity/Currently%20Offline/D103FA?icon=discord)](https://github.com/CodexLink/discord-activity-badge)
`str` `STATIC_SUBJECT_STRING` *Defaults to*: **None** | Statically declare a certain string to display on the subject. If declared, ***[]_ACTIVITY_STRING and []_STATUS_STRING*** will be ignored. </br></br> [![Demo #4](https://badgen.net/badge/Discord%20Activity/Playing%20Honkai%20Impact%203/green?icon=discord)](https://github.com/CodexLink/discord-activity-badge)

> 1. Options: ***CUSTOM_ACTIVITY***, ***GAME_ACTIVITY***, ***RICH_PRESENCE***, ***STREAM_ACTIVITY***, and ***SPOTIFY_ACTIVITY***.
> 2. Options: ***ONLINE***, ***IDLE***, ***DND***, and ***OFFLINE***.

*I separated the options along with the parameter to avoid confusion while reading it.*

#### Context

Whenever you want to change the context of the badge, you can use this set of parameters for extending the context or shorten it.

| Parameters    | Description + Result (If there's any)
| :-----------: | :------------------:
`str` `PREFERRED_PRESENCE_CONTEXT` *Options*: *[***DETAILS***, STATE, CONTEXT_DISABLED]* | Overrides additional information to append in the badge. So far, only `DETAILS` and `STATE` are allowed to be appended since it shows the other context of the application.
`str` `TIME_DISPLAY_OUTPUT` *Options*: *[TIME_DISABLED, HOURS, **HOURS_MINUTE**, MINUTES, SECONDS]* | Appends time (based on preference) after the application name or the detail of the activity when `APPEND_PRESENCE_CONTEXT` is **True**. </br></br> [![Demo #6](https://badgen.net/badge/Currently%20Playing/Visual%20Studio%20Code,%206%20hours%20Elapsed./green?icon=discord)](https://github.com/CodexLink/discord-activity-badge)
`str` `TIME_DISPLAY_ELAPSED_OVERRIDE_STRING` *Defaults to*: **elapsed.** | Overrides the string appended whenever the time is displayed for elapsed. This is effective only when SHOW_TIME_DURATION is **True**. </br></br> [![Demo #7](https://badgen.net/badge/Currently%20Playing/Visual%20Studio%20Code,%206%20hours%20and%20counting./green?icon=discord)](https://github.com/CodexLink/discord-activity-badge)
`str` `TIME_DISPLAY_REMAINING_OVERRIDE_STRING` *Defaults to*: **remaining.** | Overrides the string appended whenever the time is displayed for remaining. This is effective only when `TIME_TO_DISPLAY` is **True**. </br></br> [![Demo #8](https://badgen.net/badge/Currently%20Playing/Visual%20Studio%20Code,%206%20hours%209%20minutes%20to%20finish./green?icon=discord)](https://github.com/CodexLink/discord-activity-badge)
`bool` `TIME_DISPLAY_SHORTHAND` *Defaults to*: **False** | Displays the time with **hours** and **minutes** shorthanded to **h** and **m**. </br></br> [![Demo #9](https://badgen.net/badge/Currently%20Playing/Visual%20Studio%20Code,%206%20h./green?icon=discord)](https://github.com/CodexLink/discord-activity-badge)

#### Preferences

| Parameters  | Description + Result
| :-----------: | :----------------:
`str` `PREFERRED_ACTIVITY_TO_DISPLAY` *Options*: *[CUSTOM_ACTIVITY, GAME_ACTIVITY, **RICH_PRESENCE**, STREAM_ACTIVITY, SPOTIFY_ACTIVITY]* | Renders a particular activity as a prioritized activity. If the preferred activity does not exist, it will render any activity by default. **There will be no demo since it only picks what activity should be displayed.**
`bool` `SHIFT_STATE_ACTIVITY_COLORS` *Defaults to*: **False** | Interchange state and activity colors. This is useful only if you want to retain your state color position even though `APPEND_STATE_ON_SUBJECT` is true. [![Demo #11](https://badgen.net/badge/Currently%20Streaming/Visual%20Studio%20Code/green?icon=discord&labelColor=purple)](https://github.com/CodexLink/discord-activity-badge)
`str (char)` `SPOTIFY_INCLUDE_ALBUM_PLAYLIST_NAME` *Defaults to*: **False** | Displays the album or the playlist from where the song is being played. **Enabling this will keep the badge long enough to capture one whole line of the README!** [![Demo #12](https://badgen.net/badge/Listening%20to/Spotify%2C%20Otsukimi%20PARTY%20HARD%20feat.%20%E3%81%AA%E3%81%AA%E3%81%B2%E3%82%89%20by%20t%2Bpazolite%3B%20Nanahira%20%28KAKATTEKOYEAH%21%21%21%21%29%20%7C%200%3A02%3A48%20of%200%3A04%3A09?color=61d800&labelColor=1db954&icon=discord)](https://github.com/CodexLink/CodexLink)
`str (char)` `STATUS_CONTEXT_SEPERATOR` *Defaults to*: **`,`** | The character/s that separates the context of every status elements. Keep note that, once you declared a value on this parameter, it will automatically add space from both ends to ensure that the content displays properly. If otherwise, the script will do the spacing on its own. [![Demo #13](https://badgen.net/badge/Currently%20Playing/Visual%20Studio%20Code%20%7C%20Idling%20In%20Workspace%20%7C%207%20hours%20elapsed./green?icon=discord&labelColor=yellow)](https://github.com/CodexLink/discord-activity-badge)

**You got some ideas or did I miss something out? Please generate an issue or PR (if you have declared it on your own), and we will talk about it.**

> For more information on how the script renders the badge based on preferences, please check the **badge.py**.

#### Development Parameters

When developing, there are other fields that shouldn't be used in the first place. Though they are helpful if you are planning to contribute or replicate the project.

| Parameters    | Type        | Default     | Description
| -----------   | ----------- | ----------- | -----------
| `IS_DRY_RUN`  | `bool` | `False` | Runs the usual process but it doesn't commit changes.

> The list does seem to contain only one parameter. Worry not, there will be more parameters to be introduced in the future!

## Credits

Here contains a list of resources that I have used in any form that contributed to the development of this repository.

### Used Libraries and Technologies

* [argparse](https://docs.python.org/3/library/argparse.html) — Parser for command-line options, arguments and sub-commands.
* [ast](https://docs.python.org/3/library/argparse.html) — Parser for command-line options, arguments and sub-commands.
* [aiohttp](https://github.com/aio-libs/aiohttp) — Asynchronous HTTP client/server framework for asyncio and Python.
* [asyncio](https://docs.python.org/3/library/asyncio.html) — is a library to write concurrent code using the async/await syntax (Asynchronous I/O).
* [Badgen.net](https://badgen.net) — Fast badge generating service.
* [base64](https://docs.python.org/3/library/base64.html) — Base16, Base32, Base64, Base85 Data Encodings.
* [black](https://github.com/psf/black) — The uncompromising Python code formatter.
* [Discord.py](https://github.com/Rapptz/discord.py) — An API wrapper for Discord written in Python.
* [Docker](https://www.docker.com/) — Empowering App Development for Developers
* [datetime](https://docs.python.org/3/library/datetime.html) — Basic date and time types.
* [discord.py-stubs](https://github.com/bryanforbes/discord.py-stubs) — Literally Discord.py Stubs for `typing` library.
* [enum](https://docs.python.org/3/library/enum.html) — Support for enumerations.
* [flake8](https://github.com/PyCQA/flake8) — flake8 is a python tool that glues together pycodestyle, pyflakes, mccabe, and third-party plugins to check the style and quality of some python code.
* [logging](https://docs.python.org/3/library/logging.html) — Logging facility for Python.
* [mypy](https://github.com/python/mypy) — Optional static typing for Python 3 and 2 (PEP 484).
* [urllib3](https://github.com/urllib3/urllib3) — Python HTTP library with thread-safe connection pooling, file post support, user friendly, and more.
* [os](https://docs.python.org/3/library/os.html) — Miscellaneous operating system interfaces.
* [Poetry](https://github.com/python-poetry/poetry) — Python dependency management and packaging made easy.
* [Python](https://www.python.org/) — an interpreted high-level general-purpose programming language.
* [Pythex](https://pythex.org/) — FIrst regular expression checker that I have used.
* [python-dotenv](https://github.com/theskumar/python-dotenv) — Get and set values in your .env file in local and production servers. 🎉
* [Regex101](https://regex101.com/) — One of the second regular expression checkers.
* [re](https://docs.python.org/3/library/re.html) — Regular expression operations.
* [sys](https://docs.python.org/3/library/sys.html) — System-specific parameters and functions.
* [time](https://docs.python.org/3/library/time.html) — Time access and conversions.
* [typing](https://docs.python.org/3/library/typing.html) — Support for type hints.
* [urllib](https://docs.python.org/3/library/urllib.html#module-urllib) — URL handling modules.
* [Visual Studio Code](https://code.visualstudio.com/) — Code editing. Redefined.

### Special Thanks

The following were the ones who inspired me and gave me confidence for making this pet project possible.

* [jacobtomlinson/python-container-action](https://github.com/jacobtomlinson/python-container-action) — A template for creating GitHub Actions in Python.
* [athul/waka-readme](https://github.com/athul/waka-readme) — Wakatime Weekly Metrics on your Profile Readme.
* <https://dev.to/dtinth/caching-docker-builds-in-github-actions-which-approach-is-the-fastest-a-research-18ei>
* <https://github.com/dtinth/github-actions-docker-layer-caching-poc> -> <https://github.com/sagikazarmark/github-actions-docker-layer-caching-poc>

### Other Resources

Keep in mind that most of these resources have been used for references and were not used for copy-pasting code! Also, it's worth noting that the **links may be unsorted**.

#### Articles or Guides

* <https://blog.baeke.info/2021/04/09/building-a-github-action-with-docker/>
* <https://pythonspeed.com/articles/base-image-python-docker-images/>
* <https://sodocumentation.net/regex/topic/9852/substitutions-with-regular-expressions>

#### Questions (Unsorted)

Some of the questions here were snipped. They will redirect you to the answer.

* <https://stackoverflow.com/questions/36342899/asyncio-ensure-future-vs-baseeventloop-create-task-vs-simple-coroutine>
* <https://stackoverflow.com/questions/66381035/docker-buildx-error-rpc-error-code-unknown-desc-server-message-insuffici>
* <https://stackoverflow.com/a/41766306/5353223>
* <https://stackoverflow.com/questions/41351346/python-asyncio-task-list-generation-without-executing-the-method>
* <https://stackoverflow.com/a/49710946/5353223>
* <https://stackoverflow.com/questions/3603502/prevent-creating-new-attributes-outside-init>
* <https://stackoverflow.com/a/18472142/5353223>
* <https://stackoverflow.com/a/624939/5353223>
* <https://stackoverflow.com/a/41766306/5353223>
* <https://stackoverflow.com/a/11743262/5353223>
* <https://stackoverflow.com/questions/9437726/how-to-get-the-value-of-a-variable-given-its-name-in-a-string>
* <https://stackoverflow.com/a/18470628/5353223>
* <https://stackoverflow.com/a/51191130/5353223>
* <https://stackoverflow.com/a/65359924/5353223>
* <https://stackoverflow.com/questions/33128325/how-to-set-class-attribute-with-await-in-init.
* <https://stackoverflow.com/questions/9575409/calling-parent-class-init-with-multiple-inheritance-whats-the-right-way/55583282>
* <https://stackoverflow.com/questions/14007545/python-regex-instantly-replace-groups>
* <https://stackoverflow.com/questions/15340582/python-extract-pattern-matches>
* <https://stackoverflow.com/a/606199/5353223>
* <https://stackoverflow.com/a/27529806/5353223>
* <https://stackoverflow.com/a/22636121/5353223>
* <https://stackoverflow.com/a/5096669/5353223>

#### Sites

* <https://crontab.guru/>
* <https://www.epochconvert.com/>
* <https://material.io/design/color/the-color-system.html#tools-for-picking-colors>
* <https://regex101.com/>

**I would like to thank those who asked and those who answered a particular question (for Questions), and to the repository and articles that describe the problem, which leads me to a certain direction, resulting in solving it.**

## License

```text
  Copyright 2021 Janrey "CodexLink" Licas

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0
```

You may see the [LICENSE.md](https://github.com/CodexLink/discord-rich-presence-activity-badge/blob/main/LICENSE) file for more information.
