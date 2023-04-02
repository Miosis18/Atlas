import discord
import os
import yaml
import datetime as dt
from discord import app_commands
from discord.ext import commands
from utilities.management.database.database_management import get_session
from utilities.models.database_models import Members, Bans

with open("./configs/config.yml") as config:
    CONFIG = yaml.load(config, Loader=yaml.FullLoader)

GUILD_ID = int(CONFIG["GuildID"])

session = get_session()


class Ban(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.Bot = bot

    # Cog Ready Terminal Message

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COMMAND] {os.path.basename(__file__)} loaded.")

    # Ban command

    @app_commands.command(name="ban", description="Get random advice")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.default_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, user: discord.Member, duration: str = None,
                  reason: str = None) -> None:

        if interaction.user.roles[-1].position <= user.roles[-1].position:
            await interaction.response.send_message("You do not have permission to ban this person")
            return

        if duration is not None:
            duration_factors = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400, 'w': 604800, 'mo': 2592000, 'y': 31536000}
            duration_list = duration.split()
            total_duration = 0
            for duration_str in duration_list:
                duration_format = duration_str[-1] if duration_str[-2:] != 'mo' else 'mo'
                if duration_format in duration_factors:
                    duration_value = duration_str[:-1]
                    if duration_value.isnumeric():
                        total_duration += int(duration_value) * duration_factors[duration_format]
                    else:
                        await interaction.response.send_message("Sorry that is an invalid duration, "
                                                                "example is 1d or 1d 12h")
                        return
                else:
                    await interaction.response.send_message("Sorry that is an invalid duration, "
                                                            "example is 1d or 1d 12h")
                    return
            ban_duration = dt.timedelta(seconds=total_duration)
            print(dt.datetime.utcnow() + ban_duration)

        try:
            if duration is not None:
                # await interaction.client.ban(user, reason=f"{reason if reason else 'None Provided'}")
                await interaction.response.send_message("User temp banned")
                try:
                    await user.send("You have been temp banned")
                except discord.errors.HTTPException:
                    pass
            else:
                # await interaction.client.ban(user, reason=f"{reason if reason else 'None Provided'}")
                await interaction.response.send_message("User banned")
                try:
                    await user.send("You have been banned")
                except discord.errors.HTTPException:
                    pass
        except discord.errors.Forbidden:
            await interaction.response.send_message("I do not have permission to ban this person")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ban(bot))
