import discord
import os
import yaml
import datetime as dt
from discord import app_commands
from discord.ext import commands

with open("./configs/config.yml") as config:
    CONFIG = yaml.load(config, Loader=yaml.FullLoader)

GUILD_ID = int(CONFIG["GuildID"])


class Avatar(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.Bot = bot

    # Cog Ready Terminal Message

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COMMAND] {os.path.basename(__file__)} loaded.")

    # Avatar command

    @app_commands.command(name="avatar", description="Get random advice")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def avatar(self, interaction: discord.Interaction, user: discord.Member = None) -> None:

        target_user = interaction.user

        if user:
            target_user = user

        avatar_embed = discord.Embed(title=f"{target_user.name}#{target_user.discriminator}",
                                     description=f"[Click here for the full image.]({target_user.avatar.url})",
                                     color=int(CONFIG["EmbedColors"].replace("#", ""), 16),
                                     timestamp=dt.datetime.now())
        avatar_embed.set_image(url=target_user.avatar.url)
        avatar_embed.set_footer(text=f"{CONFIG['BotName']} - Command issued by {interaction.user.name}#"
                                     f"{interaction.user.discriminator}", icon_url=self.Bot.user.display_avatar)

        await interaction.response.send_message(embed=avatar_embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Avatar(bot))
