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


def get_quote():
    try:
        phrase = []

        while len(phrase) > 128 or len(phrase) < 4:
            # get title
            all_titles = [u"śmierć", "Artur Schopenhauer",
                          u"życie", u"nieszczęście", "niepowodzenie"]
            title = all_titles[random.randint(0, len(all_titles) - 1)]

            # search
            search_results = openSearch(title)

            pages = queryTitles(search_results['response'][0])
            if pages['response'] != "":
                sections = getSectionsForPage(pages['response'])
                quotes = getQuotesForSection(
                    pages['response'], sections['response'][0])

                quotes = quotes['response']
                phrase = quotes[random.randint(0, len(quotes) - 1)]
        return phrase
    except KeyError:
        return FALLBACK_QUOTES[random.randint(0, len(FALLBACK_QUOTES) - 1)]
