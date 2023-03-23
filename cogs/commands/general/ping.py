import discord
import os
import yaml
import datetime as dt
from discord import app_commands
from discord.ext import commands

with open("./configs/config.yml") as config:
    CONFIG = yaml.load(config, Loader=yaml.FullLoader)

GUILD_ID = int(CONFIG["GuildID"])


class EightBall(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.Bot = bot

    # Cog Ready Terminal Message

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COMMAND] {os.path.basename(__file__)} loaded.")

    # Ping command

    @app_commands.command(name="ping", description="Check the bots latency")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def ping(self, interaction: discord.Interaction) -> None:

        ping_embed = discord.Embed(title="[:ping_pong:] Pinged",
                                   color=int(CONFIG["EmbedColors"].replace("#", ""), 16),
                                   timestamp=dt.datetime.utcnow())
        ping_embed.add_field(name="Pong!", value="The bot has successfully pinged the server :globe_with_meridians:, "
                                                 "you can see the statistics below:"
                                                 "\n\nThese statistics depend on your connection to discord and the "
                                                 "servers response times.")
        ping_embed.add_field(name="Latency - :bar_chart:", value=f"`{round(self.Bot.latency * 1000)}ms`",
                             inline=False)
        ping_embed.set_footer(text=f"{CONFIG['BotName']} - Command issued by {interaction.user.name}#"
                                   f"{interaction.user.discriminator}", icon_url=self.Bot.user.display_avatar)

        await interaction.response.send_message(embed=ping_embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(EightBall(bot))
