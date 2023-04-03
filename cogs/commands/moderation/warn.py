import discord
import os
import yaml
import pytz
import datetime as dt
from discord import app_commands
from discord.ext import commands
from utilities.management.database.database_management import get_session
from utilities.management.database.new_member import NewMember
from utilities.models.database_models import Members, Warns

with open("./configs/config.yml") as config:
    CONFIG = yaml.load(config, Loader=yaml.FullLoader)

GUILD_ID = int(CONFIG["GuildID"])

session = get_session()


class Warn(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.Bot = bot

    # Cog Ready Terminal Message

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COMMAND] {os.path.basename(__file__)} loaded.")

    # Suggest command

    @app_commands.command(name="warn", description="Get random advice")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.default_permissions(moderate_members=True)
    async def warn(self, interaction: discord.Interaction, user: discord.Member, reason: str) -> None:

        if interaction.user.roles[-1].position <= user.roles[-1].position:
            await interaction.response.send_message("You do not have permission to warn this person", ephemeral=True)
            return

        member_in_database = session.query(Members).filter(Members.user_id == str(user.id)).first()

        if not member_in_database:
            await NewMember().add_new_member_to_db(user)
            member_in_database = session.query(Members).filter(Members.user_id == str(user.id)).first()

        await interaction.response.send_message(f"{user.mention} has been warned by {interaction.user.mention}")

        new_warn = Warns(
            member_id=member_in_database.member_id,
            reason=reason if reason else 'N/A',
            date_warned=dt.datetime.now(pytz.utc).date().strftime("%d-%m-%Y")
        )
        session.add(new_warn)
        session.commit()

        try:
            await user.send(f"You have been warned by {interaction.user.name} for {reason if reason else 'N/A'}")
        except discord.errors.HTTPException:
            pass





async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Warn(bot))
