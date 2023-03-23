import discord
import yaml
import os
from discord.ext import commands
from datetime import datetime as dt


with open("./configs/config.yml") as config:
    CONFIG = yaml.load(config, Loader=yaml.FullLoader)


class Joins(commands.Cog):
    def __init__(self, bot):
        self.Bot = bot

    # Cog Ready Terminal Message

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[EVENT] {os.path.basename(__file__)} loaded.")

    # Member Join Event ( Welcome DM, Welcome Message, Database Add )

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if CONFIG["EnableWelcomeMessages"] is True:
            welcome_embed = discord.Embed(title="[:ping_pong:] Member Has Joined",
                                          color=int(CONFIG["EmbedColors"].replace("#", ""), 16),
                                          timestamp=dt.utcnow())
            welcome_embed.add_field(name="Example",
                                    value="Welcome message here")
            welcome_embed.set_thumbnail(url=member.avatar.url)
            welcome_embed.set_footer(text=f"{CONFIG['BotName']} - Command issued by Console",
                                     icon_url=self.Bot.user.display_avatar)

            welcome_channel = self.Bot.get_channel(int(CONFIG["WelcomeChannel"]))
            await welcome_channel.send(embed=welcome_embed)


async def setup(bot):
    await bot.add_cog(Joins(bot))
