# -*- coding: utf-8 -*-
import random
from .wikiquotes import openSearch, queryTitles, getSectionsForPage, \
    getQuotesForSection


# ugh, you should totally get that from wikiquotes
FALLBACK_QUOTES = [
    "Czy nie wygląda to, jakby istnienie było pomyłką, której skutki ujawniają się stopniowo coraz bardziej?",  # noqa
    "Każde pożegnanie ma coś ze śmierci, każde ponowne spotkanie – coś ze zmartwychwstania.",  # noqa
    "Na świecie ma się do wyboru tylko samotność albo pospolitość.",  # noqa
    "Nieustanne starania obliczone na usunięcie cierpienia nie dają nic poza zmianą jego postaci.",  # noqa
    "Prostytutki to ludzkie ofiary złożone na ołtarzu monogamii.",  # noqa
    "Suma cierpień przewyższa u człowieka znacznie sumę rozkoszy.",  # noqa
    "Zimno mi psychicznie.",
]

ALL_TITLES = [
    "śmierć",
    "Artur Schopenhauer",
    "porażka",
    "życie",
    "nieszczęście",
    "niepowodzenie"
]


def get_quote():
    try:
        phrase = ""

        while not phrase:
            # search
            search_results = openSearch(random.choice(ALL_TITLES))

            pages = queryTitles(search_results['response'][0])
            if pages['response'] != "":
                sections = getSectionsForPage(pages['response'])
                quotes = getQuotesForSection(
                    pages['response'], sections['response'][0])

                quotes = quotes['response']
                phrase = random.choice(
                    [x for x in quotes if 4 < len(x) <= 128])
        return phrase
    except KeyError:
        return FALLBACK_QUOTES[random.randint(0, len(FALLBACK_QUOTES) - 1)]
