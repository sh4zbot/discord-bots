from twitchAPI.twitch import Twitch

from discord_bots.config import TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET

twitch = None
if TWITCH_CLIENT_ID and TWITCH_CLIENT_SECRET:
    twitch = Twitch(app_id=TWITCH_CLIENT_ID, app_secret=TWITCH_CLIENT_SECRET)
