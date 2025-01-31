# SheevBot

This is a bot originally made for /r/PrequelMemes to help with spam prevention.

# Getting started


## Installing packages and renaming files
1. Install the packages in `requirements.txt`.
2. COPY the three files that end in `_EXAMPLE` to remove the `_EXAMPLE` from the filename. Leave the original `_EXAMPLE` files as well or git will get upset.

## Creating user accounts
1. Create a discord bot. [Instructions here](https://discordpy.readthedocs.io/en/stable/discord.html). Put the token in `sheevsecrets.py`. The only perms you need are view channels, send messages, embed links, and attach files.
2. You need a reddit account for the bot. Create the account regularly, log in, go to [this page](https://www.reddit.com/prefs/apps/) and create an app with type "script". Put the the secret and client ID in `sheevsecrets.py`. Also, put your password for the account in `sheevsecrets.py`.
3. Invite the reddit account for the bot to your subreddit as a moderator. The perms it needs are users, flair, posts, comments, and wiki. 

## Discord server
The bot is managed via discord. Your discord server needs a few things:
1. A channel for the bot to dump its logs in. Note it will frequently report having truoble processing certain posts. I am looking into it but it doesn't seem to actually cause an issue. Mute the channel and only look in there if you are trying to diagnose something. The bot will ping you if something critical happens.
2. A channel to log announcements in your subreddit. Every time you sticky a post the bot will post a link to the post in that channel. Note that by default this can take up to an hour to reduce unnecessary calls, since logging announcements is typically not time sensitive.
3. A channel to dump the scoreboard report the bot can generate. This is a report meant to be run (manually) once a month that shows critical mod actions taken by your team during the previous month.

## Test Subreddit
1. Create a test subreddit to test settings and stuff before you go live. Make it the ONLY subreddit in the "subreddits" list in the `bot_config.json` until you are ready to go live. Also, put it in the "test_subreddit" field.

## Configuring the bot
1. The `SheevCloud.py` file will have to be changed to suit your specific storage platform. If you are hosting the bot locally, just replace the entire contents of each function with `pass`.
2. In `bot_config.json`, EVERYTHING needs to be changed except for the two "freqency" variables.
3. For each subreddit you are monitoring (including the test subreddit), create a wiki page called `sheevbot`. Make sure it is hidden/mod-only/unlisted. Take the contents of `sheevbot.wiki`, paste them into the wiki page, then change the values to match your subreddits flairs, desired responses, etc.

# Notes 

* The `SheevCloud.json` file is currently set up for my google cloud storage setup. I didn't make that file more generic/configurable because settup up google cloud was not easy, and I wanted to at least throw some kind of error if you didn't do your due diligence. The edits you have to make to the file if you are using google cloud storage are minimal.
* The things in the `bot_config.json`, being on the machine the bot runs, are only meant to be set up by the admin running the bot.
* The things on the `sheevbot` wiki pages, being on the subreddit itself, are meant to be manageable by any moderator in your subreddit.
* The PRAW module will be CONSTANTLY printing out a warning message about using it in an async environment. There is a bug in PRAW that prevents it from working with this for some reason, and I haven't been able to figure out a workaround, nor can I figure out how to supress the message.
* Any times referenced by the bot in config files are in seconds.