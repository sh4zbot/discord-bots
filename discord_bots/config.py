import os
from dotenv import load_dotenv

load_dotenv()
CONFIG_VALID: bool = True


def to_string(key: str, required: bool = False, default: str | None = None) -> str | None:
    value = os.getenv(key)
    if not value and default is not None:
        return default
    elif required and not value:
        global CONFIG_VALID
        CONFIG_VALID = False
        print(f"{key} must be specified correctly, was '{value}'")
        return None
    else:
        return value


def to_int2(key: str, required: bool = False, default: int | None = None) -> int | None:
    value = os.getenv(key)
    try:
        return int(value)
    except:
        if required and default is None:
            global CONFIG_VALID
            CONFIG_VALID = False
            print(f"{key} must be specified correctly, was '{value}'")
        return default


def to_float2(key: str, required: bool = False, default: float | None = None) -> float | None:
    value = os.getenv(key)
    try:
        return float(value)
    except:
        if required and default is None:
            global CONFIG_VALID
            CONFIG_VALID = False
            print(f"{key} must be specified correctly, was '{value}'")
        return default


def to_bool(key: str, required: bool = False, default: bool | None = None) -> bool | None:
    value = os.getenv(key)
    if value is not None and value.lower() == "true":
        return True
    elif value is not None and value.lower() == "false":
        return False
    else:
        if required and default is None:
            global CONFIG_VALID
            CONFIG_VALID = False
            print(f"{key} must be specified correctly, was '{value}'")
        return default


def convert_to_int(value: str) -> int | None:
    try:
        return int(value)
    except:
        return None


# Discord setup
API_KEY: str = to_string(key="DISCORD_API_KEY", required=True)
CHANNEL_ID: int = to_int2(key="CHANNEL_ID", required=True)
TRIBES_VOICE_CATEGORY_CHANNEL_ID: int = to_int2(key="TRIBES_VOICE_CATEGORY_CHANNEL_ID", required=True)
admin_ids = os.getenv("SEED_ADMIN_IDS").split(",") if os.getenv("SEED_ADMIN_IDS") else []
SEED_ADMIN_IDS: list[int] = list(filter(lambda x: x is not None, map(convert_to_int, admin_ids)))
if not len(SEED_ADMIN_IDS):
    print("SEED_ADMIN_IDS must be specified")
    CONFIG_VALID = False

# Database setup
DB_NAME: str = to_string(key="DB_NAME", required=True)
DB_USER_NAME: str = to_string(key="DB_USER_NAME", required=True)
DB_PASSWORD: str = to_string(key="DB_PASSWORD", required=True)

# Functional setup
DEBUG: bool = to_bool(key="DEBUG", default=False)
mock_command_users = os.getenv("MOCK_COMMAND_USERS").split(",") if os.getenv("MOCK_COMMAND_USERS") else []
MOCK_COMMAND_USERS: list[int] = list(filter(lambda x: x is not None, map(convert_to_int, mock_command_users)))
COMMAND_PREFIX: str = to_string(key="COMMAND_PREFIX", default="!")
SHOW_TRUESKILL: bool = to_bool(key="SHOW_TRUESKILL", default=False)
RANDOM_MAP_ROTATION: bool = to_bool(key="RANDOM_MAP_ROTATION", default=False)
AFK_TIME_MINUTES: int = to_int2(key="AFK_TIME_MINUTES", default=45)
MAP_ROTATION_MINUTES: int = to_int2(key="MAP_ROTATION_MINUTES", default=60)
MAP_VOTE_THRESHOLD: int = to_int2(key="MAP_VOTE_THRESHOLD", default=7)
RE_ADD_DELAY_SECONDS: int = to_int2(key="RE_ADD_DELAY", default=30)
DEFAULT_TRUESKILL_MU: float | None = to_float2(key="DEFAULT_TRUESKILL_MU")
DEFAULT_TRUESKILL_SIGMA: float | None = to_float2(key="DEFAULT_TRUESKILL_MU")
DISABLE_PRIVATE_MESSAGES = to_bool(key="DISABLE_PRIVATE_MESSAGES", default=False)
POP_RANDOM_QUEUE = to_bool(key="POP_RANDOM_QUEUE", default=True)

# stats
STATS_DIR: str | None = to_string(key="STATS_DIR")
STATS_HEIGHT: int | None = to_int2(key="STATS_HEIGHT")
STATS_WIDTH: int | None = to_int2(key="STATS_WIDTH")

# Twitch integration
TWITCH_CLIENT_ID: str | None = to_string(key="TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET: str | None = to_string(key="TWITCH_CLIENT_SECRET")
TWITCH_GAME_NAME: str | None = to_string(key="TWITCH_GAME_NAME")
