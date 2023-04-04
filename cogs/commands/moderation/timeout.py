import discord
import os
import yaml
import pytz
import datetime as dt
from discord import app_commands
from discord.ext import commands
from utilities.management.generic.punishments import Punishments
from utilities.management.database.database_management import get_session
from utilities.management.database.new_member import NewMember
from utilities.models.database_models import Members, Mutes

with open("./configs/config.yml") as config:
    CONFIG = yaml.load(config, Loader=yaml.FullLoader)

GUILD_ID = int(CONFIG["GuildID"])

session = get_session()


class TimeoutCommand(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.Bot = bot

    # Cog Ready Terminal Message

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COMMAND] {os.path.basename(__file__)} loaded.")

    # Suggest command

    @app_commands.command(name="timeout", description="Get random advice")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.default_permissions(moderate_members=True)
    async def timeout(self, interaction: discord.Interaction, user: discord.Member, duration: str, reason: str) -> None:

        if interaction.user.roles[-1].position <= user.roles[-1].position:
            await interaction.response.send_message("You do not have permission to mute this person", ephemeral=True)
            return

        try:
            total_duration, unmute_date, human_readable_duration = await Punishments().calculate_duration(duration)
        except ValueError:
            await interaction.response.send_message("That is an invalid duration time, usage: 1d or 1d 12hr",
                                                    ephemeral=True)
            return

        member_in_database = session.query(Members).filter(Members.user_id == str(user.id)).first()

        if not member_in_database:
            await NewMember().add_new_member_to_db(user)
            member_in_database = session.query(Members).filter(Members.user_id == str(user.id)).first()

        try:
            await user.timeout(unmute_date, reason=reason)
            await interaction.response.send_message(f"{user.mention} has been timed out by {interaction.user.mention}.")

            new_timeout = Mutes(
                member_id=member_in_database.member_id,
                duration=human_readable_duration,
                reason=reason if reason else 'N/A',
                date_muted=dt.datetime.now(pytz.utc).date().strftime("%d-%m-%Y"),
                date_of_unmute=unmute_date.date().strftime("%d-%m-%Y"),
                unmute_timestamp="N/A",
                mute_type="Timeout"
            )
            session.add(new_timeout)
            session.commit()

        except discord.errors.Forbidden:
            await interaction.response.send_message("I do not have permission to mute this person.", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TimeoutCommand(bot))
