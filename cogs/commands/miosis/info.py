import discord
import os
import yaml
import datetime as dt
from discord import app_commands
from discord.ext import commands

with open("./configs/config.yml") as config:
    CONFIG = yaml.load(config, Loader=yaml.FullLoader)

GUILD_ID = int(CONFIG["GuildID"])


class Info(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.Bot = bot

    # Cog Ready Terminal Message

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COMMAND] {os.path.basename(__file__)} loaded.")

    # Meme command

    @app_commands.command(name="info", description="Get random advice")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def info(self, interaction: discord.Interaction) -> None:

        info_embed = discord.Embed(title=f"{CONFIG['BotName']} Information",
                                   color=int(CONFIG["EmbedColors"].replace("#", ""), 16),
                                   timestamp=dt.datetime.now())
        info_embed.add_field(name="Version", value=f"`{CONFIG['Version']}`", inline=False)
        info_embed.add_field(name="Creator", value="Miosis#0010", inline=False)
        info_embed.add_field(name="Description", value="This bot is available for free to use or view its source code, "
                                                       "you can view the bot at this link", inline=False)
        info_embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/669987834966441995/cafa057d426c3e6f97ae1646fcf1fba7.png?size=1024")
        info_embed.set_footer(text=f"{CONFIG['BotName']} - Command issued by {interaction.user.name}#"
                                   f"{interaction.user.discriminator}", icon_url=self.Bot.user.display_avatar)

        await interaction.response.send_message(embed=info_embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Info(bot))
