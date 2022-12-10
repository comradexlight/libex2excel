import re
from typing import Union


def get_user_id_part(raw_url: str) -> Union[str, None]:
    user_id_part = re.search("usr(\\d)*", raw_url)
    if user_id_part:
        return user_id_part.group()
    return None


def get_url() -> str:
    user_id_part = None
    while user_id_part is None:
        raw_url = input("Please type the page address of the libex user whose"\
                "catalog you want to retrieve.\nYour link should match the"\
                "template https://www.libex.ru/ppl/usr******/\n")
        user_id_part = get_user_id_part(raw_url)
    return "https://www.libex.ru/ppl/" + user_id_part + "/"
