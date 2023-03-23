import discord
import os
from discord.ext import commands
from discord.ext.commands import Greedy, Context
from typing import Optional, Literal


class Syncing(commands.Cog):
    def __init__(self, bot):
        self.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[ADMIN] {os.path.basename(__file__)} loaded.")

    @commands.command()
    @commands.guild_only()
    async def sync(self, ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) \
            -> None:
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


async def setup(bot):
    await bot.add_cog(Syncing(bot))
