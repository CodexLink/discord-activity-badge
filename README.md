<h1 align="center">Discord Rich Presence to Github Profile Badge</h1>
<h4 align="center">A Dockerized Github Workflow utilizing Discord.py for Rich Presence Display, Powered by Python.</h4>

<div align="center">

![Codacy Grade](https://img.shields.io/codacy/grade/d2da8866a48145be8c330a9056b35743?label=Codacy%20Grade&logo=codacy)
[![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/CodexLink/dquerybotboilerplate?label=CodeFactor%20Grade&logo=codefactor)](https://www.codefactor.io/repository/github/codexlink/dquerybotboilerplate)
[![Repository License](https://img.shields.io/badge/Repo%20License-MIT-blueviolet)](https://github.com/CodexLink/discord-rich-presence-activity-badge/blob/main/LICENSE)
</div>

## Welcome

To be constructed.

## Usage

The usage of this workflow action is similarly the same to other actions. You need to instantiate the name of this repo with `uses` in `step` along `with` required parameters.

### Workflow

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

These inputs are required in order to run the Docker Container or the action workflow that you referred, which is this repo.

| Inputs                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `WORKFLOW_INSTANCE_TOKEN` | An auto-generated token for authentication use in order to make changes to the user's profile `README.md`.    |
| `DISCORD_USERNAME`  | The user's discord username. `Required` as a target for the status lookup.    |
| `DISCORD_USERNAME_TAG` | The user's discord unique tag. `Required` as there are other instance were you have a same username to other users.   |

#### Optional Inputs

These inputs are optional and has the capability to override the display of the badge and the commit message.

| Inputs                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `` | To be constructed.    |
| ``   | To be constructed.    |

## Examples

With multiple variety of output of this workflow, here's an example of occurences along with Parameters given and the Result.

| Parameters                                             | Result                                        |
|------------------------------------------------------|-----------------------------------------------|
| `` | To be constructed.    |
| ``   | To be constructed.    |

## Credits

* [Discord.py](https://github.com/Rapptz/discord.py) — An API wrapper for Discord written in Python.
* [PEP 8 Guidelines Tl;DR Version](https://realpython.com/python-pep8/#naming-conventions) — Huge thanks to [Jasmine Finer](https://github.com/jasminefiner) (who made the article) for TL;DR or compressed version of PEP 8 Guidelines.
* [Shields.io](https://shields.io/) — Concise, consistent, and legible badges in SVG and raster format.

## License

This project is licensed under the **MIT License** by [Janrey Licas](https://github.com/CodexLink) - see the [LICENSE.md](https://github.com/CodexLink/discord-rich-presence-activity-badge/blob/main/LICENSE) file for more information.