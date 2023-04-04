import discord
import os
import yaml
import pytz
import datetime as dt
from discord import app_commands
from discord.ext import commands
from utilities.management.database.database_management import get_session
from utilities.models.database_models import Members, UnBans

with open("./configs/config.yml") as config:
    CONFIG = yaml.load(config, Loader=yaml.FullLoader)

GUILD_ID = int(CONFIG["GuildID"])

session = get_session()


class UnBan(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.Bot = bot

    # Cog Ready Terminal Message

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COMMAND] {os.path.basename(__file__)} loaded.")

    # Unban command

    @app_commands.command(name="unban", description="Get random advice")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.default_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user: discord.User, reason: str) -> None:

        try:
            await interaction.guild.unban(user, reason=reason)
            await interaction.response.send_message(f"{user.name} has been unbanned.")
        except discord.errors.NotFound:
            await interaction.response.send_message("That user is not banned.")
            return

        member_in_database = session.query(Members).filter(Members.user_id == str(user.id)).first()

        if member_in_database:
            new_unban = UnBans(
                member_id=member_in_database.member_id,
                reason=reason if reason else 'N/A',
                date_of_unban=dt.datetime.now(pytz.utc).date().strftime("%d-%m-%Y")
            )
            session.add(new_unban)
            session.commit()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UnBan(bot))
