import discord
import os
import yaml
import json
import random
import datetime as dt
from discord import app_commands
from discord.ext import commands

with open("./configs/config.yml") as config:
    CONFIG = yaml.load(config, Loader=yaml.FullLoader)

GUILD_ID = int(CONFIG["GuildID"])


class DarkJoke(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.Bot = bot

    # Cog Ready Terminal Message

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COMMAND] {os.path.basename(__file__)} loaded.")

    # DarkJoke command

    @app_commands.command(name="darkjoke", description="Get random advice")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def dark_joke(self, interaction: discord.Interaction) -> None:

        with open("./data/json/dark_jokes.json", "r", encoding="UTF-8") as file:
            data = json.load(file)

        dark_joke_embed = discord.Embed(title="**DARK JOKE** :rofl:",
                                        description=random.choice(data["DarkJokes"]),
                                        color=int(CONFIG["EmbedColors"].replace("#", ""), 16),
                                        timestamp=dt.datetime.now())
        dark_joke_embed.set_footer(text=f"{CONFIG['BotName']} - Command issued by {interaction.user.name}#"
                                        f"{interaction.user.discriminator}", icon_url=self.Bot.user.display_avatar)

        await interaction.response.send_message(embed=dark_joke_embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(DarkJoke(bot))
