import discord
import os
import yaml
from discord import app_commands
from discord.ext import commands

with open("./configs/config.yml") as config:
    CONFIG = yaml.load(config, Loader=yaml.FullLoader)

GUILD_ID = int(CONFIG["GuildID"])


class AddRole(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.Bot = bot

    # Cog Ready Terminal Message

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COMMAND] {os.path.basename(__file__)} loaded.")

    # Suggest command

    @app_commands.command(name="addrole", description="Get random advice")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.default_permissions(manage_roles=True)
    async def add_role(self, interaction: discord.Interaction, user: discord.Member, role: discord.Role) -> None:

        if role not in user.roles:
            if interaction.user.id != user.id:
                if interaction.user.roles[-1].position >= role.position:
                    try:
                        await user.add_roles(role)
                        await interaction.response.send_message("Role added")
                    except discord.errors.Forbidden:
                        await interaction.response.send_message("I cannot add this role as I do not have a role "
                                                                "high enough to do this.", ephemeral=True)
                else:
                    await interaction.response.send_message("You cannot do this as you do not have permission to "
                                                            "promote someone this high", ephemeral=True)
            else:
                await interaction.response.send_message("You cannot add roles to yourself", ephemeral=True)
        else:
            await interaction.response.send_message("They already have the role", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AddRole(bot))
