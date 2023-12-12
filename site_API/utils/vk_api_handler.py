import requests
from typing import Dict
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Item:
    name: str
    description: str
    price: str
    currency: str
    photo: str
    owner: str
    link: str


class SiteApiInterface:
    @staticmethod
    def make_item_list(response):
        response_lst = []
        for item in response:
            response_lst.append(Item(name=item["title"],
                                     description=item["description"],
                                     price=str(int(item["price"]["amount"]) // 100),
                                     currency=item["price"]["currency"]["title"],
                                     photo=item["thumb_photo"],
                                     owner="https://vk.com/market" + str(item["owner_id"]),
                                     link="https://vk.com/market?utm_ref=left_menu&w=product" +
                                          str(item["owner_id"]) + "_" + str(item["id"]) + "%2Fquery"
                                     )
                                )
        return response_lst

    @staticmethod
    def get_low(url: str, params: Dict, success=200):
        params["sort_by"] = 2
        params["sort_direction"] = 0
        response = requests.get(
            url=url,
            params=params
        )
        status_code = response.status_code
        if status_code == success:
            response = response.json()["response"]["items"]
            return SiteApiInterface.make_item_list(response)
        return status_code

    @staticmethod
    def get_high(url: str, params: Dict, success=200):
        params["sort_by"] = 2
        params["sort_direction"] = 1
        response = requests.get(
            url=url,
            params=params
        )
        status_code = response.status_code
        if status_code == success:
            response = response.json()["response"]["items"]
            return SiteApiInterface.make_item_list(response)
        return status_code

    @staticmethod
    def get_custom(url: str, params: Dict, success=200):
        params["sort_by"] = 2
        params["sort_direction"] = 1
        response = requests.get(
            url=url,
            params=params
        )
        status_code = response.status_code
        if status_code == success:
            response = response.json()["response"]["items"]
            return SiteApiInterface.make_item_list(response)
        return status_code
