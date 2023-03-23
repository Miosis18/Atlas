import discord
import os
import yaml
import upsidedown
import datetime as dt
from discord import app_commands
from discord.ext import commands

with open("./configs/config.yml") as config:
    CONFIG = yaml.load(config, Loader=yaml.FullLoader)

GUILD_ID = int(CONFIG["GuildID"])


class FlipText(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.Bot = bot

    # Cog Ready Terminal Message

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COMMAND] {os.path.basename(__file__)} loaded.")

    # FlipText command

    @app_commands.command(name="fliptext", description="Get random advice")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def flip_text(self, interaction: discord.Interaction, text: str) -> None:

        flipped_text_embed = discord.Embed(description=upsidedown.transform(text),
                                           color=int(CONFIG["EmbedColors"].replace("#", ""), 16),
                                           timestamp=dt.datetime.now())
        flipped_text_embed.set_footer(text=f"{CONFIG['BotName']} - Command issued by {interaction.user.name}#"
                                           f"{interaction.user.discriminator}", icon_url=self.Bot.user.display_avatar)

        await interaction.response.send_message(embed=flipped_text_embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(FlipText(bot))
