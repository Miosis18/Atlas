import discord
import os
import yaml
import random
import datetime as dt
from discord import app_commands
from discord.ext import commands

with open("./configs/config.yml") as config:
    CONFIG = yaml.load(config, Loader=yaml.FullLoader)

with open("./configs/lang.yml") as lang:
    LANG = yaml.load(lang, Loader=yaml.FullLoader)

GUILD_ID = int(CONFIG["GuildID"])


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.Bot = bot

    # Cog Ready Terminal Message

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COMMAND] {os.path.basename(__file__)} loaded.")

    # EightBall command

    @app_commands.command(name="8ball", description="Ask the bot a question")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def eight_ball(self, interaction: discord.Interaction, question: str) -> None:

        eight_ball_embed = discord.Embed(color=int(CONFIG["EmbedColors"].replace("#", ""), 16),
                                         timestamp=dt.datetime.utcnow())
        eight_ball_embed.add_field(name="Question", value=f"{question.capitalize()}", inline=False)
        eight_ball_embed.add_field(name="Answer", value=f"{random.choice(LANG['EightBallReplies']).capitalize()}",
                                   inline=False)
        eight_ball_embed.set_footer(text=f"{CONFIG['BotName']} - Command issued by {interaction.user.name}#"
                                         f"{interaction.user.discriminator}", icon_url=self.Bot.user.display_avatar)

        await interaction.response.send_message(embed=eight_ball_embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ping(bot))
