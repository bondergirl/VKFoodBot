import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import StrictStr, SecretStr

load_dotenv()


class SiteSettings(BaseSettings):
    api_key: SecretStr = os.getenv("SITE_API", None)
    vk_token: SecretStr = os.getenv("VK_TOKEN", None)
    host_api: StrictStr = os.getenv("HOST_API", None)


class BotSettings(BaseSettings):
    bot_token: SecretStr = os.getenv("BOT_TOKEN", None)
