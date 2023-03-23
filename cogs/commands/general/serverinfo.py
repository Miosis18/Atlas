import discord
import os
import yaml
import datetime as dt
from discord import app_commands
from discord.ext import commands

with open("./configs/config.yml") as config:
    CONFIG = yaml.load(config, Loader=yaml.FullLoader)

GUILD_ID = int(CONFIG["GuildID"])


class ServerInfo(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.Bot = bot

    # Cog Ready Terminal Message

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COMMAND] {os.path.basename(__file__)} loaded.")

    # ServerInfo command

    @app_commands.command(name="serverinfo", description="Get random advice")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def server_info(self, interaction: discord.Interaction) -> None:
        notification_level = ((str(interaction.guild.default_notifications).split('.')[1]).replace('_', ' ')).split(' ')

        details_message = (
            f">>> **Name:** {interaction.guild.name}\n"
            f"**ID:** {interaction.guild.id}\n"
            f"**Owner:** {interaction.guild.owner.mention}\n"
            f"**Created At:** {interaction.guild.created_at.date()} "
            f"({(dt.datetime.now().date() - interaction.guild.created_at.date()).days} days)\n"
            f"**Verification:** {str(interaction.guild.verification_level).capitalize()}\n"
            f"**Notifications:** {' '.join([i.capitalize() for i in notification_level])}\n\n")

        statistics_message = (
            f">>> **Members:** {interaction.guild.member_count}\n"
            f"**Roles:** {len(interaction.guild.roles) - 1 if len(interaction.guild.roles) - 1 >= 0 else 0}\n"
            f"**Channels:** {len(interaction.guild.channels) - 1 if len(interaction.guild.channels) - 1 >= 0 else 0}\n"
            f"**Emojis:** {len(interaction.guild.emojis) - 1 if len(interaction.guild.emojis) - 1 >= 0 else 0}\n"
            f"**Stickers:** {len(interaction.guild.stickers) - 1 if len(interaction.guild.stickers) - 1 >= 0 else 0}\n"
            f"**Boosts:** {interaction.guild.premium_subscription_count}")

        server_statistics_embed = discord.Embed(color=int(CONFIG["EmbedColors"].replace("#", ""), 16),
                                                timestamp=dt.datetime.now())
        server_statistics_embed.set_thumbnail(url=interaction.guild.icon.url)
        server_statistics_embed.set_author(name=interaction.guild.name)
        server_statistics_embed.add_field(name="Server Details:", value=details_message, inline=False)
        server_statistics_embed.add_field(name="Server Statistics:", value=statistics_message, inline=False)
        server_statistics_embed.set_footer(text=f"{CONFIG['BotName']} - Command issued by {interaction.user.name}#"
                                                f"{interaction.user.discriminator}",
                                           icon_url=self.Bot.user.display_avatar)

        await interaction.response.send_message(embed=server_statistics_embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ServerInfo(bot))
