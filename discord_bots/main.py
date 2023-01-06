from datetime import datetime, timezone

from discord import Colour, Embed, Member, Message, Reaction
from discord.abc import User
from discord.ext.commands import CommandError, Context, UserInputError

from .bot import bot
from discord_bots.config import API_KEY, COMMAND_PREFIX, CONFIG_VALID, CHANNEL_ID, SEED_ADMIN_IDS
from .models import CustomCommand, Player, QueuePlayer, QueueWaitlistPlayer, Session
from .tasks import (
    add_player_task,
    afk_timer_task,
    map_rotation_task,
    queue_waitlist_task,
    vote_passed_waitlist_task,
)

add_player_task.start()
afk_timer_task.start()
map_rotation_task.start()
queue_waitlist_task.start()
vote_passed_waitlist_task.start()

session = Session()
for seed_admin_id in SEED_ADMIN_IDS:
    # There always has to be at least one initial admin to add others!
    player = session.query(Player).filter(Player.id == seed_admin_id).first()
    if player:
        player.is_admin = True
        session.commit()
session.close()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")


@bot.event
async def on_command_error(ctx: Context, error: CommandError):
    if isinstance(error, UserInputError):
        if ctx.command.usage:
            await ctx.channel.send(
                embed=Embed(
                    description=f"Usage: {COMMAND_PREFIX}{ctx.command.name} {ctx.command.usage}",
                    colour=Colour.red(),
                )
            )
        else:
            await ctx.channel.send(
                embed=Embed(
                    description=f"Usage: {COMMAND_PREFIX}{ctx.command.name} {ctx.command.signature}",
                    colour=Colour.red(),
                )
            )
    else:
        if ctx.command:
            print("[on_command_error]:", error, ", command:", ctx.command.name)
        else:
            print("[on_command_error]:", error)


@bot.event
async def on_message(message: Message):
    if message.channel.id == CHANNEL_ID:
        session = Session()
        player: Player | None = (
            session.query(Player).filter(Player.id == message.author.id).first()
        )
        if player:
            player.last_activity_at = datetime.now(timezone.utc)
            if player.name != message.author.display_name:
                player.name = message.author.display_name
        else:
            session.add(
                Player(
                    id=message.author.id,
                    name=message.author.display_name,
                    last_activity_at=datetime.now(timezone.utc),
                )
            )
        session.commit()
        session.close()
        await bot.process_commands(message)

        # Custom commands below
        if not message.content.startswith(COMMAND_PREFIX):
            return

        bot_commands = {command.name for command in bot.commands}
        command_name = message.content.split(" ")[0][1:]
        session = Session()
        if command_name not in bot_commands:
            custom_command: CustomCommand | None = (
                session.query(CustomCommand)
                .filter(CustomCommand.name == command_name)
                .first()
            )
            if custom_command:
                await message.channel.send(content=custom_command.output)
        session.close()


@bot.event
async def on_reaction_add(reaction: Reaction, user: User | Member):
    session = Session()
    player: Player | None = session.query(Player).filter(Player.id == user.id).first()
    if player:
        player.last_activity_at = datetime.now(timezone.utc)
        session.commit()
    else:
        session.add(
            Player(
                id=reaction.message.author.id,
                name=reaction.message.author.display_name,
                last_activity_at=datetime.now(timezone.utc),
            )
        )
    session.close()


@bot.event
async def on_join(member: Member):
    session = Session()
    player = session.query(Player).filter(Player.id == member.id).first()
    if player:
        player.name = member.name
        session.commit()
    else:
        session.add(Player(id=member.id, name=member.name))
        session.commit()
    session.close()


@bot.event
async def on_leave(member: Member):
    session = Session()
    session.query(QueuePlayer).filter(QueuePlayer.player_id == member.id).delete()
    session.query(QueueWaitlistPlayer).filter(
        QueueWaitlistPlayer.player_id == member.id
    ).delete()
    session.commit()


def main():
    if CONFIG_VALID:
        bot.run(API_KEY)
    else:
        print("You must provide a valid config!")


if __name__ == "__main__":
    main()
