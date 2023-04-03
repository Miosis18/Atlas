import discord
import os
import yaml
import pytz
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

    @staticmethod
    async def calculate_duration(duration: str):
        total_duration = 0
        unban_date = "Never"
        human_readable_duration = ""

        if duration:
            duration_factors = {'s': ('Second', 1), 'm': ('Minute', 60), 'h': ('Hour', 3600), 'd': ('Day', 86400),
                                'w': ('Week', 604800),  'mo': ('Month', 2592000), 'y': ('Year', 31536000)}

            duration_list = duration.split()

            for dur_str in duration_list:
                dur_format = dur_str[-1] if dur_str[-2:] != 'mo' else 'mo'
                if dur_format in duration_factors:
                    dur_value = dur_str[:-1]
                    if dur_value.isnumeric():
                        total_duration += int(dur_value) * duration_factors[dur_format][1]

                        # append the human-readable duration label
                        if human_readable_duration:
                            human_readable_duration += ", "
                        if int(dur_value) == 1:
                            human_readable_duration += f"1 {duration_factors[dur_format][0]}"
                        else:
                            human_readable_duration += f"{dur_value} {duration_factors[dur_format][0]}s"
                    else:
                        raise ValueError("Invalid duration, example: 1d or 1d 12h")
                else:
                    raise ValueError("Invalid duration, example: 1d or 1d 12h")

            ban_duration = dt.timedelta(seconds=total_duration)
            unban_date = (dt.datetime.now(pytz.utc) + ban_duration)

        return total_duration, unban_date, human_readable_duration

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

        total_duration, unban_date, human_readable_duration = await self.calculate_duration(duration)

        member_in_database = session.query(Members).filter(Members.user_id == str(user.id)).first()

        if not member_in_database:
            new_member_entry = Members(
                user_id=user.id,
                username=f"{user.display_name}#{user.discriminator}",
                date_joined=dt.datetime.now(pytz.utc).date().strftime("%d-%m-%Y")
            )
            session.add(new_member_entry)
            session.commit()
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
