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


class DogFact(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.Bot = bot

    # Cog Ready Terminal Message

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COMMAND] {os.path.basename(__file__)} loaded.")

    # DogFact command

    @app_commands.command(name="dogfact", description="Get random advice")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def dog_fact(self, interaction: discord.Interaction) -> None:

        request = requests.get(url="https://dog-api.kinduff.com/api/facts").json()

        dog_fact_embed = discord.Embed(title=f"**Facts about dogs** :dog:",
                                       description=request["facts"][0],
                                       color=int(CONFIG["EmbedColors"].replace("#", ""), 16),
                                       timestamp=dt.datetime.now())
        dog_fact_embed.set_footer(text=f"{CONFIG['BotName']} - Command issued by {interaction.user.name}#"
                                       f"{interaction.user.discriminator}", icon_url=self.Bot.user.display_avatar)

        await interaction.response.send_message(embed=dog_fact_embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(DogFact(bot))
