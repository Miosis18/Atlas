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
            await interaction.response.send_message("You do not have permission to ban this person", ephemeral=True)
            return

        total_duration, unban_date, human_readable_duration = await Punishments().calculate_duration(duration)

        member_in_database = session.query(Members).filter(Members.user_id == str(user.id)).first()

        if not member_in_database:
            await NewMember().add_new_member_to_db(user)
            member_in_database = session.query(Members).filter(Members.user_id == str(user.id)).first()

        try:
            ban_msg = "User banned"
            duration_str = "Permanent"
            date_of_unban = unban_date
            if duration:
                ban_msg = "User temp banned"
                duration_str = human_readable_duration
                date_of_unban = unban_date.date().strftime("%d-%m-%Y")

            await interaction.response.send_message(ban_msg)
            new_ban = Bans(
                member_id=member_in_database.member_id,
                duration=duration_str,
                reason=reason if reason else 'N/A',
                date_banned=dt.datetime.now(pytz.utc).date().strftime("%d-%m-%Y"),
                date_of_unban=date_of_unban,
                unban_timestamp=0 if not duration else (str(unban_date.timestamp()).replace(".", ""))
            )
            session.add(new_ban)
            try:
                await user.send(f"You have been {ban_msg.lower()}")
            except discord.errors.HTTPException:
                pass
            session.commit()
        except discord.errors.Forbidden:
            await interaction.response.send_message("I do not have permission to ban this person", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ban(bot))
