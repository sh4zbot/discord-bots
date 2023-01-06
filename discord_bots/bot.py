# This file exists to avoid a circular reference

import discord
from discord.ext import commands

from discord_bots.config import COMMAND_PREFIX

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
    case_insensitive=True,
    command_prefix=COMMAND_PREFIX,
    help_command=commands.DefaultHelpCommand(verify_checks=False, dm_help=True),
    intents=intents,
)
