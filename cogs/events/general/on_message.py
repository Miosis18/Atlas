import json
import os
from discord.ext import commands


class NewMessage(commands.Cog):
    def __init__(self, bot):
        self.Bot = bot

    # Cog Ready Terminal Message

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[EVENT] {os.path.basename(__file__)} loaded.")

    @commands.Cog.listener()
    async def on_message(self, message):

        if not message.author.bot:

            with open("./data/json/general_data.json") as file:
                data = json.load(file)

                data["total_messages_since_up"] += 1

            with open("./data/json/general_data.json", "w+") as file:
                json.dump(data, file, indent=4)


async def setup(bot):
    await bot.add_cog(NewMessage(bot))
