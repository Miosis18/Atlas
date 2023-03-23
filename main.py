import asyncio
import os
import colorama
import discord
import yaml
from colorama import Fore
from discord.ext import commands

# Load bot configuration from YAML file
with open("./configs/config.yml") as config_file:
    CONFIG = yaml.load(config_file, Loader=yaml.FullLoader)


# Function to load all cogs from a given directory
async def load_cogs(bot, cogs_dir):
    for cog in os.listdir(cogs_dir):
        if (cog.lower()).endswith(".py"):
            await bot.load_extension(f"{cogs_dir.replace('/', '.')[2:]}.{cog[:-3]}")


# Create a subclass of commands.Bot to customize its behavior
class Atlas(commands.Bot):
    def __init__(self):
        # Call the parent constructor with a custom command prefix and enabled intents
        super().__init__(command_prefix="-", intents=discord.Intents.all())

    # This function is called after the bot is fully initialized but before it starts running
    async def setup_hook(self) -> None:
        await load_cogs(self, "./addons/commands")
        await load_cogs(self, "./addons/tasks")
        # Load cogs from four different directories
        await load_cogs(self, "./cogs/commands/general")
        await load_cogs(self, "./cogs/events")
        await load_cogs(self, "./cogs/tasks")
        await load_cogs(self, "./utilities/management/syncing")


# This function is called when the bot finishes logging in and is ready to start accepting commands
async def on_ready() -> None:
    # Wait 10 seconds before printing anything to the console
    await asyncio.sleep(10)
    # Print a fancy banner to the console with various bot information
    print(f"""
    {"―" * 100}
    {Fore.GREEN}{CONFIG['BotName']} v{CONFIG['Version']} is now Online! 
    {Fore.WHITE}({Fore.LIGHTBLACK_EX}{CONFIG['LicenseKey']}{Fore.WHITE})
    {Fore.RESET}Join our discord server for support, {Fore.BLUE}https://discord.gg/tKqBfUkyds
    {Fore.RESET}• By using this bot you agree to all terms located here, {Fore.YELLOW}ElliotAR.net/tos
    {Fore.RESET}• Addons for the bot can be found here, {Fore.YELLOW}ElliotAR.net/store
    {Fore.RESET}
    {"―" * 100}
""")


# Entry point of the program
def main() -> None:
    # Initialize the colorama module to enable colored console output
    colorama.init(autoreset=True)
    # Print a message to the console to indicate that the bot is starting up
    print(f"{Fore.YELLOW}Starting Bot, this may take a while...")
    # Create an instance of the Bot class and run the bot with the token from the config file
    bot = Atlas()
    # bot.run(CONFIG["BotToken"], log_handler=None)
    bot.run(os.environ['BOT_TOKEN'])


# Only run the main function if this script is being executed directly (not imported)
if __name__ == "__main__":
    main()
