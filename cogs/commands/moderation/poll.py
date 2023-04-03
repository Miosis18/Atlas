import discord
import os
import yaml
import datetime as dt
from discord import app_commands
from discord.ext import commands

with open("./configs/config.yml") as config:
    CONFIG = yaml.load(config, Loader=yaml.FullLoader)

GUILD_ID = int(CONFIG["GuildID"])


class Poll(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.Bot = bot

    # Cog Ready Terminal Message

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COMMAND] {os.path.basename(__file__)} loaded.")

    # Poll command

    @app_commands.command(name="poll", description="Get random advice")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def poll(self, interaction: discord.Interaction, question: str) -> None:

        poll_embed = discord.Embed(title="A poll has been started!",
                                   description=question,
                                   color=int(CONFIG["EmbedColors"].replace("#", ""), 16),
                                   timestamp=dt.datetime.utcnow())
        poll_embed.set_footer(text=f"Poll started by: {interaction.user.name}#{interaction.user.discriminator}",
                              icon_url=interaction.user.display_avatar.url)

        await interaction.response.send_message(embed=poll_embed)
        new_poll_message = await interaction.original_response()
        await new_poll_message.add_reaction("\U0001F44D")
        await new_poll_message.add_reaction("\U0001F44E")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Poll(bot))
