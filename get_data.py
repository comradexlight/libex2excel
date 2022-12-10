import requests
import re
from enum import Enum
from time import sleep
from typing import Iterable, List
from bs4 import BeautifulSoup
from dataclasses import dataclass

import config


class Condition(str, Enum):
    new = "новое"
    like_new = "как новое"
    excellent = "отличное"
    good = "хорошее"
    acceptable = "приемлемое"
    poor = "плохое"
    digital_book = "цифровая книга"


@dataclass(slots=True, frozen=True)
class Book:
    author: str
    title: str
    book_series: str
    year_of_publication: str
    publishing: str
    condition: Condition


def get_data_from_libex(url: str) -> List[Book]:
    page_number = 0
    books_list = []
    next_page_is_exist = True
    while next_page_is_exist:
        response = requests.get(
                url,
                params={"pg": page_number},
                cookies=config.cookies,
                headers=config.headers
                )
        soup = BeautifulSoup(response.text, "lxml")
        items = soup.find_all(
                "div",
                attrs={"style": "border-bottom:1px solid #330066;"\
                        "padding:0.35em 0em 0.35em 0em;"}
                )
        for item in items:
            book = _parse_raw_book_data(item)
            books_list.append(book)
        print("Current page is", page_number)
        page_number += 1
        sleep(0.4)
        if len(items) < 12:
            next_page_is_exist = False

    print("Book data received")
    return books_list


def _parse_raw_book_data(raw_book_data) -> Book:
    book_data = raw_book_data.find_all("td")
    return Book(
        author=_parse_author(book_data),
        title=_parse_title(book_data),
        book_series=_parse_book_series(book_data),
        year_of_publication=_parse_year_of_publication(book_data),
        publishing=_parse_publishing(book_data),
        condition=_parse_condition(raw_book_data)
        )


def _parse_author(book_data) -> str:
    return book_data[0].text.strip()


def _parse_title(book_data) -> str:
    return book_data[1].text.strip()


def _parse_book_series(book_data) -> str:
    if re.search(
            "(Серия: )([a-zA-Zа-яА-Я\\s]*)",
            book_data[2].text
            ) is not None:
        return re.search(
                "(Серия: )([a-zA-Zа-яА-Я\\s]*)",
                book_data[2].text).group().split("Серия: ")[1]
    return ""


def _parse_publishing(book_data) -> str:
    return re.search("(Изд-во: )([a-zA-Zа-яА-Я\\s\\-:.]*)",
                     book_data[2].text).group().strip().split("Изд-во: ")[1]


def _parse_year_of_publication(book_data) -> str:
    return re.search("\\d{4}(-\\d{4})?", book_data[2].text).group()


def _parse_condition(raw_book_data) -> Condition:
    condition = raw_book_data.find("img", attrs={"style": "vertical-align:"\
            "middle;"})["title"].split("состояние: ")[1]
    return Condition(condition)
