import discord
import os
import yaml
import random
import datetime as dt
from discord import app_commands
from discord.ext import commands

with open("./configs/config.yml") as config:
    CONFIG = yaml.load(config, Loader=yaml.FullLoader)

GUILD_ID = int(CONFIG["GuildID"])


class CoinFlip(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.Bot = bot

    # Cog Ready Terminal Message

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COMMAND] {os.path.basename(__file__)} loaded.")

    # CoinFlip command

    @app_commands.command(name="coinflip", description="Get random advice")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def coin_flip(self, interaction: discord.Interaction) -> None:

        coinflip_embed = discord.Embed(title=f"{interaction.user.name}#{interaction.user.discriminator} "
                                             f"has flipped a coin",
                                       description=f"The coin landed on **{random.choice(['Heads', 'Tails'])}**",
                                       color=int(CONFIG["EmbedColors"].replace("#", ""), 16),
                                       timestamp=dt.datetime.now())
        coinflip_embed.set_footer(text=f"{CONFIG['BotName']} - Command issued by {interaction.user.name}#"
                                       f"{interaction.user.discriminator}", icon_url=self.Bot.user.display_avatar)

        await interaction.response.send_message(embed=coinflip_embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CoinFlip(bot))
