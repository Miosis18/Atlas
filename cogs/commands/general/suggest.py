import discord
import os
import yaml
import datetime as dt
from discord import app_commands, ui
from discord.ext import commands
from utilities.management.database.database_management import get_session
from utilities.models.database_models import Suggestions

with open("./configs/config.yml") as config:
    CONFIG = yaml.load(config, Loader=yaml.FullLoader)

GUILD_ID = int(CONFIG["GuildID"])

# Create a database session
session = get_session()


class SuggestionsButtons(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Upvote", style=discord.ButtonStyle.secondary, emoji="\U00002b06")
    async def upvote(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(label="Downvote", style=discord.ButtonStyle.secondary, emoji="\U00002b07")
    async def down_vote(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(label="Reset Vote", style=discord.ButtonStyle.secondary, emoji="\U0001f5d1")
    async def reset(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.primary, emoji="\U00002705",
                       disabled=not (CONFIG["SuggestionSettings"]["EnableAcceptDenySystem"]))
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(label="Reject", style=discord.ButtonStyle.primary, emoji="\U0000274c",
                       disabled=not (CONFIG["SuggestionSettings"]["EnableAcceptDenySystem"]))
    async def reject(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass


class Suggest(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.Bot = bot

    # Cog Ready Terminal Message

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[COMMAND] {os.path.basename(__file__)} loaded.")

    # Suggest command

    @app_commands.command(name="suggest", description="Get random advice")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def suggest(self, interaction: discord.Interaction, suggestion: str) -> None:

        if CONFIG["SuggestionSettings"]["Enabled"] is True:

            suggestions_channel = await self.Bot.fetch_channel(CONFIG["SuggestionSettings"]["ChannelID"])

            last_suggestion = session.query(Suggestions).order_by(Suggestions.suggestion_id.desc()).first()
            last_suggestion_id = 0 if last_suggestion is None else last_suggestion.suggestion_id

            suggestion_embed = discord.Embed(title=f":bulb: New Suggestion (#{last_suggestion_id + 1})",
                                             color=int(CONFIG["SuggestionStatusesEmbedColors"]["Pending"].replace(
                                                 "#", ""), 16),
                                             timestamp=dt.datetime.utcnow())
            suggestion_embed.set_footer(icon_url=interaction.user.display_avatar.url,
                                        text=f"{interaction.user.name}#{interaction.user.discriminator}")

            suggestion_message = await suggestions_channel.send(embed=suggestion_embed, view=SuggestionsButtons())
            await interaction.response.send_message("Your suggestion has been posted", ephemeral=True)

            new_suggestion = Suggestions(
                message_id=suggestion_message.id,
                author_id=interaction.user.id,
                content=suggestion,
                up_votes=0,
                down_votes=0,
                status="Pending"
            )

            session.add(new_suggestion)
            session.commit()

        else:
            await interaction.response.send_message("Sorry, the suggestion system has been disabled.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Suggest(bot))
