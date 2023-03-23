import discord
import os
import yaml
import json
from discord.ext import commands, tasks

with open("./configs/config.yml") as config:
    CONFIG = yaml.load(config, Loader=yaml.FullLoader)

GUILD_ID = int(CONFIG["GuildID"])


class Status(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.status_index = 0

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[TASK] {os.path.basename(__file__)} loaded.")
        if CONFIG["BotActivitySettings"]["Enabled"] is True:
            self.activity_change.start()

    # Bot status change loop

    @tasks.loop(seconds=CONFIG["BotActivitySettings"]["Interval"])
    async def activity_change(self):

        # Change Status Message

        status = CONFIG['BotActivitySettings']['Statuses'][self.status_index]

        if "{total-users}" in status:
            status = status.replace("{total-users}", str(self.bot.get_guild(GUILD_ID).member_count))
        elif "{total-messages}" in status:
            with open("./data/json/general_data.json") as f:
                data = json.load(f)
            status = status.replace("{total-messages}", str(data["total_messages_since_up"]))
        elif "{total-channels}" in status:
            status = status.replace("{total-channels}", str(len(self.bot.get_guild(GUILD_ID).voice_channels) +
                                                            len(self.bot.get_guild(GUILD_ID).text_channels)))

        # Change Activity

        if CONFIG['BotActivitySettings']["Type"].upper() == "WATCHING":
            await self.bot.change_presence(
                activity=discord.Activity(type=discord.ActivityType.watching, name=status))
        elif CONFIG['BotActivitySettings']["Type"].upper() == "PLAYING":
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=status))
        elif CONFIG['BotActivitySettings']["Type"].upper() == "LISTENING":
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status))
        elif CONFIG['BotActivitySettings']["Type"].upper() == "COMPETING":
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=status))

        # Scroll Through Config List

        if self.status_index >= (len(CONFIG['BotActivitySettings']['Statuses']) - 1):
            self.status_index = 0
        else:
            self.status_index += 1


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Status(bot))
