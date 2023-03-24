import discord
import os
import yaml
import requests
import datetime as dt
from discord import app_commands
from discord.ext import commands

with open("./configs/config.yml") as config:
    CONFIG = yaml.load(config, Loader=yaml.FullLoader)

GUILD_ID = int(CONFIG["GuildID"])


class CatFact(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.Bot = bot

    # Cog Ready Terminal Message

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COMMAND] {os.path.basename(__file__)} loaded.")

    # CatFact command

    @app_commands.command(name="catfact", description="Get random advice")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def cat_fact(self, interaction: discord.Interaction) -> None:

        request = requests.get(url="https://meowfacts.herokuapp.com/").json()

        cat_fact_embed = discord.Embed(title=f"**Facts about cats** :cat:",
                                       description=request["data"][0],
                                       color=int(CONFIG["EmbedColors"].replace("#", ""), 16),
                                       timestamp=dt.datetime.now())
        cat_fact_embed.set_footer(text=f"{CONFIG['BotName']} - Command issued by {interaction.user.name}#"
                                       f"{interaction.user.discriminator}", icon_url=self.Bot.user.display_avatar)

        await interaction.response.send_message(embed=cat_fact_embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CatFact(bot))
