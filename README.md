# Atlas Discord Bot



`atlas` A discord bot with plenty of features good for any sized community discord server. Atlas is a remade clone of PlexBot which is a relatively expensive alternative.

Contents
========

 * [Why?](#why)
 * [Installation](#installation)
 * [Configuration](#configuration)
 * [Want to contribute?](#want-to-contribute)

### Why?

I saw how many sales that PlexBot was gaining and thought to myself this isnt a hard bot to make and could be done in a relatively short amount of time, if so many people are willing to pay for this then I am willing to make it for free and release it open source.

Not only this but the current PlexBot didnt seem to be maintained, using APIs that no longer worked and thus loss of functionality in commands that utilized those APIs as well as using an outdated version of discord.js

`Atlas` is an upto date clone of PlexBot using the latest version of discord.py coded from the ground up and maintains information about members, suggestions and punishments in a mysql database.

### Installation
---

> **Warning**
> Be careful running this with elevated privileges. Code execution can be achieved with write permissions on the config file.


#### Install From Source

```bash
$ git clone https://www.github.com/miosis18/atlas.git
$ cd atlas
$ pip3 install .
```


### Configuration

Atlas comes with a config file written in yaml that allows the end user to input values and toggle settings as they see fit. Yaml is an easy to use markup language not requiring computer savvy end users. 

To access the config file navigate to `~/.configs/config.yml`

1. Open the file in a text editor that you see fit. `Notepad++ is recommended`
2. Make your changes as you see fit and dont forget to save the file.
3. If an error occurs after you edit the config then either revert your changes and try again OR delete the config entirely and Atlas will generate you a fresh one.

Editing the file in a text editor will give you more control and be faster.



### Want to Contribute?
---

Check out `CONTRIBUTING.md` and the `docs` directory.