import discord
import json
import os
import datetime as dt
from discord.ext import commands


class MessageDelete(commands.Cog):
    def __init__(self, bot):
        self.Bot = bot

    # Cog Ready Terminal Message

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[EVENT] {os.path.basename(__file__)} loaded.")

    @commands.Cog.listener()
    async def on_message_delete(self, message):

        message_deleter_logs = [log async for log in message.guild.audit_logs(
            limit=1, action=discord.AuditLogAction.message_delete)]

        message_deleted_author = message_deleter_logs[0].target
        valid_time_check = (dt.datetime.utcnow() - (message_deleter_logs[0].created_at.replace(tzinfo=None))).seconds

        if (message.author.id != message_deleted_author.id) or (valid_time_check > 5):

            with open("./data/json/general_data.json") as file:
                data = json.load(file)

                data["last_deleted_message"]["member_id"] = message.author.id
                data["last_deleted_message"]["message_content"] = message.content

            with open("./data/json/general_data.json", "w+") as file:
                json.dump(data, file, indent=4)


async def setup(bot):
    await bot.add_cog(MessageDelete(bot))
