import discord
import os
import yaml
import json
import datetime as dt
from discord import app_commands
from discord.ext import commands

with open("./configs/config.yml") as config:
    CONFIG = yaml.load(config, Loader=yaml.FullLoader)

GUILD_ID = int(CONFIG["GuildID"])


class Snipe(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.Bot = bot

    # Cog Ready Terminal Message

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COMMAND] {os.path.basename(__file__)} loaded.")

    # Snipe command

    @app_commands.command(name="snipe", description="Get random advice")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def snipe(self, interaction: discord.Interaction) -> None:

        with open("./data/json/general_data.json", "r") as file:
            data = json.load(file)

        if data["last_deleted_message"]["member_id"] and data["last_deleted_message"]["message_content"]:

            try:
                message_author = await interaction.guild.fetch_member(int(data["last_deleted_message"]["member_id"]))

                last_deleted_message_embed = discord.Embed(color=int(CONFIG["EmbedColors"].replace("#", ""), 16),
                                                           timestamp=dt.datetime.now())
                last_deleted_message_embed.add_field(name="Author", value=message_author.mention, inline=False)
                last_deleted_message_embed.add_field(name="Message", value=data["last_deleted_message"]["message_content"],
                                                     inline=False)
                last_deleted_message_embed.set_footer(text=f"{CONFIG['BotName']} - "
                                                           f"Command issued by {interaction.user.name}#"
                                                           f"{interaction.user.discriminator}",
                                                      icon_url=self.Bot.user.display_avatar)

                await interaction.response.send_message(embed=last_deleted_message_embed)

            except discord.errors.HTTPException:
                await interaction.response.send_message("Whoopsie, an error has occurred.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Snipe(bot))
