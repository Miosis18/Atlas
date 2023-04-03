import os
import yaml
import datetime as dt
from discord.ext import commands
from utilities.management.database.database_management import get_session
from utilities.models.database_models import Members

with open("./configs/config.yml") as config:
    CONFIG = yaml.load(config, Loader=yaml.FullLoader)

GUILD_ID = int(CONFIG["GuildID"])

session = get_session()


class OnStartup(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.Bot = bot

    async def check_database_for_members(self):
        await self.Bot.wait_until_ready()

        members_in_database = session.query(Members).all()
        guild = await self.Bot.fetch_guild(CONFIG["GuildID"])

        async for member in guild.fetch_members():
            if member.id not in [member_db_entry.member_id for member_db_entry in members_in_database]:
                new_member_entry = Members(
                    user_id=member.id,
                    username=member.display_name,
                    date_joined=dt.datetime.now().date().strftime("%d-%m-%Y")
                )
                session.add(new_member_entry)

        session.commit()

    async def cog_load(self):
        self.Bot.loop.create_task(self.check_database_for_members())

    # Cog Ready Terminal Message

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[EVENT] {os.path.basename(__file__)} loaded.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(OnStartup(bot))
