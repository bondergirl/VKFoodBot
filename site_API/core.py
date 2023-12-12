from settings import SiteSettings
from site_API.utils.vk_api_handler import SiteApiInterface


vk = SiteSettings()

method = "market.searchItems"
version = 5.199
token = vk.vk_token.get_secret_value()

url = f"https://api.vk.com/method/{method}"

params = {"access_token": token, "v": version, "category_id": 10006, "q": " "}

vk_api = SiteApiInterface()

