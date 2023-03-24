import discord
import os
import yaml
import datetime as dt
from discord import app_commands
from discord.ext import commands

with open("./configs/config.yml") as config:
    CONFIG = yaml.load(config, Loader=yaml.FullLoader)

GUILD_ID = int(CONFIG["GuildID"])


class UserInfo(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.Bot = bot

    # Cog Ready Terminal Message

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COMMAND] {os.path.basename(__file__)} loaded.")

    # UserInfo command

    @app_commands.command(name="userinfo", description="Get random advice")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def user_info(self, interaction: discord.Interaction, user: discord.Member = None) -> None:

        target_user = user or interaction.user

        suffixes = {1: "st", 2: "nd", 3: "rd"}
        day = int(target_user.joined_at.strftime('%d'))
        join_date_suffix = suffixes.get(day if day < 20 or day > 30 else day % 10, "th")
        join_date_string = target_user.joined_at.strftime(
            '%A, %d') + join_date_suffix + target_user.joined_at.strftime(' %B %Y')

        badges = {
            "Active Developer": "active_developer",
            "Bug Hunter": "bug_hunter",
            "Bug Hunter Level Two": "bug_hunter_level_2",
            "Discord Certified Moderator": "discord_certified_moderator",
            "Early Supporter": "early_supporter",
            "Early Verified Bot Developer": "early_verified_bot_developer",
            "HypeSquad Events": "hypesquad",
            "House Of Balance": "hypesquad_balance",
            "House Of Bravery": "hypesquad_bravery",
            "House Of Brilliance": "hypesquad_brilliance",
            "Discord Partner": "partner",
            "Discord Staff": "staff",
            "Verified Bot Developer": "verified_bot_developer"
        }

        member_badges = ""
        for badge, flag in badges.items():
            if getattr(target_user.public_flags, flag):
                member_badges += f"{badge}, "

        member_details_message = (
            f">>> **Nickname:** {'None' if target_user.display_name == target_user.name else target_user.display_name}\n"
            f"**Joined At:** {join_date_string}\n"
            f"**Highest Role:** {target_user.top_role.mention}\n\n")

        user_details_message = (
            f">>> **ID:** {target_user.id}\n"
            f"**Username:** {target_user.name}\n"
            f"**Created At:** {target_user.created_at.date()} "
            f"({(dt.datetime.now().date() - target_user.created_at.date()).days} days)\n"
            f"**Badges:** {'None' if member_badges == '' else member_badges[:-2]}\n"
            f"**Bot Account:** {'Yes' if target_user.bot is True else 'No'}")

        user_statistics_embed = discord.Embed(color=int(CONFIG["EmbedColors"].replace("#", ""), 16),
                                              timestamp=dt.datetime.now())
        user_statistics_embed.set_thumbnail(url=target_user.display_avatar.url)
        user_statistics_embed.set_author(name=f"{target_user.name}#{target_user.discriminator}",
                                         icon_url=target_user.display_avatar.url)
        user_statistics_embed.add_field(name="Member Details:", value=member_details_message, inline=False)
        user_statistics_embed.add_field(name="User Details:", value=user_details_message, inline=False)
        user_statistics_embed.set_footer(text=f"{CONFIG['BotName']} - Command issued by {interaction.user.name}#"
                                              f"{interaction.user.discriminator}",
                                         icon_url=self.Bot.user.display_avatar.url)

        await interaction.response.send_message(embed=user_statistics_embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UserInfo(bot))
