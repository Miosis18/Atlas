import discord
import pytz
import datetime as dt
from utilities.management.database.database_management import get_session
from utilities.models.database_models import Members, Bans

session = get_session()


class NewMember:
    @staticmethod
    async def add_new_member_to_db(user: discord.Member) -> None:
        new_member_entry = Members(
            user_id=user.id,
            username=f"{user.display_name}#{user.discriminator}",
            date_joined=dt.datetime.now(pytz.utc).date().strftime("%d-%m-%Y")
        )
        session.add(new_member_entry)
        session.commit()
