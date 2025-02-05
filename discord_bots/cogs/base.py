from typing import Type

from discord import Colour
from discord.ext.commands import Cog, Context

from discord_bots.checks import HasName
from discord_bots.utils import send_message


class BaseCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_before_invoke(self, ctx: Context):
        self.message = ctx.message

    async def send_success_message(self, success_message):
        await send_message(
            self.message.channel,
            embed_description=success_message,
            colour=Colour.green(),
        )

    async def send_info_message(self, info_message):
        await send_message(
            self.message.channel,
            embed_description=info_message,
            colour=Colour.blue(),
        )

    async def send_error_message(self, error_message):
        await send_message(
            self.message.channel, embed_description=error_message, colour=Colour.red()
        )

    async def setname(
        self, ctx: Context, class_: Type[HasName], old_name: str, new_name: str
    ):
        session = ctx.session

        entry: class_ | None = (
            session.query(class_).filter(class_.name.ilike(old_name)).first()
        )
        if not entry:
            await self.send_error_message(
                f"Could not find {class_.__name__.lower()} **{old_name}**"
            )
            return

        old_name = entry.name
        entry.name = new_name
        session.commit()
        await self.send_success_message(
            f"{class_.__name__} name updated from **{old_name}** to **{new_name}**"
        )
