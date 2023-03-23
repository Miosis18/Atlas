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


class Dog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.Bot = bot

    # Cog Ready Terminal Message

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COMMAND] {os.path.basename(__file__)} loaded.")

    # Dog command

    @app_commands.command(name="dog", description="Get random advice")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def dog(self, interaction: discord.Interaction) -> None:

        appropriate_image = False
        image = "https://i.pinimg.com/564x/7e/c3/5a/7ec35aa21a3212ed7658f7ff9542c9db.jpg"

        while appropriate_image is False:
            request = requests.get(url="https://random.dog/woof.json").json()
            if request["url"][-3:] == "jpg":
                image = request["url"]
                appropriate_image = True

        dog_embed = discord.Embed(title="**Woof Woof** :dog:",
                                  color=int(CONFIG["EmbedColors"].replace("#", ""), 16),
                                  timestamp=dt.datetime.now())
        dog_embed.set_image(url=image)
        dog_embed.set_footer(text=f"{CONFIG['BotName']} - Command issued by {interaction.user.name}#"
                                  f"{interaction.user.discriminator}", icon_url=self.Bot.user.display_avatar)

        await interaction.response.send_message(embed=dog_embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Dog(bot))
