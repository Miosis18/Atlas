import discord
import os
import yaml
import aiohttp
import random
from discord import app_commands
from discord.ext import commands

with open("./configs/config.yml") as config:
    CONFIG = yaml.load(config, Loader=yaml.FullLoader)

GUILD_ID = int(CONFIG["GuildID"])


class Meme(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.Bot = bot

    # Cog Ready Terminal Message

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COMMAND] {os.path.basename(__file__)} loaded.")

    # Meme command

    @app_commands.command(name="meme", description="Get random advice")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def meme(self, interaction: discord.Interaction) -> None:

        subreddits = CONFIG["SubReddits"]

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://www.reddit.com/r/{random.choice(subreddits)}/random/.json") as response:
                data = await response.json()

        chosen_post = data[0]['data']['children'][0]['data']

        meme_embed = discord.Embed(title=chosen_post['title'],
                                   description=f"[View Thread](https://reddit.com{chosen_post['permalink']})",
                                   color=int(CONFIG["EmbedColors"].replace("#", ""), 16))
        meme_embed.set_image(url=chosen_post['url'])
        meme_embed.set_footer(text=f"\U0001F44D {chosen_post['ups']} \U0001F44E {chosen_post['downs']} "
                                   f"\U0001F4AC {chosen_post['num_comments']}")

        await interaction.response.send_message(embed=meme_embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Meme(bot))
