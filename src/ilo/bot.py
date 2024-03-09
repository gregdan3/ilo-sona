import logging
import traceback
import uuid

import discord
from discord.ext import commands

from ilo.db import ChallengeDB

LOG = logging.getLogger()


class Ilo(discord.Bot):
    def __init__(self, database_file: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = ChallengeDB(database_file=database_file)

        # Loading every cog in the cogs folder
        cogs = ["translation"]

        for cog in cogs:
            self.load_extensions(f"ilo.cogs.{cog}")

    async def on_ready(self):
        LOG.info("Logged in!")

    async def on_application_command_error(
        self, ctx: discord.ApplicationContext, error
    ):
        if isinstance(error, commands.PrivateMessageOnly):
            await ctx.respond(
                "This command can only be used in a DM with the bot.", ephemeral=True
            )

        # Lets us know if it's an invoke error with an error ID.
        if isinstance(error, discord.ApplicationCommandInvokeError):
            error_id = uuid.uuid4()

            LOG.exception(
                f"Exception from {ctx.command.qualified_name}!\n"
                f"{''.join(traceback.format_exception(type(error), error, error.__traceback__))}"
                f"Error ID: {error_id}"
            )

            await ctx.respond(
                f"Exception `{error.args}` from {ctx.command.qualified_name}!\n"
                f"Error ID: `{error_id}`\n"
                "Please send the error ID to `@gregdan3` for debugging."
            )
