# -*- coding: utf-8 -*-
import requests
from lxml import html

API_URL = "http://pl.wikiquote.org/w/api.php"


def openSearch(titles):
    """

    :param titles:
    :return:
    """
    result = requests.get(API_URL, params={
        "format": "json",
        "action": "opensearch",
        "namespace": 0,
        "suggest": "",
        "search": titles,
    })

    if result.status_code == 200:
        try:
            result_response = result.json()[1]
        except:
            result_repsonse = "Parsing error"
    else:
        result_response = ""

    return {
        "response": result_response,
        "status": result.status_code,
    }


def getRandomQuote(title):
    return ""


def getQuotesForSection(page_id, section):
    result = requests.get(API_URL, params={
        "format": "json",
        "action": "parse",
        "noimages": "",
        "pageid": page_id,
        "section": section,
    })

    result_response = ""

    if result.status_code == 200:
        quotes_text = ""
        quotes_array = []
        try:
            result_json = result.json()
            quotes_text = result_json['parse']['text']["*"]
        except:
            result_repsonse = "Parsing error"

        quotes_html = html.fromstring(quotes_text)
        quote_objects = quotes_html.xpath('//li/text()')

        ignored = ["Autor: ", "\n", ", ", u"Zobacz też: ", ]

        for obj in quote_objects:
            if obj not in ignored:
                quotes_array += [obj, ]
        result_response = quotes_array
    else:
        result_response = ""

    return {
        "response": result_response,
        "status": result.status_code,
    }


def getSectionsForPage(page_id):
    result = requests.get(API_URL, params={
        "format": "json",
        "action": "parse",
        "prop": "sections",
        "pageid": page_id
    })

    result_response = ""

    if result.status_code == 200:
        try:
            result_json = result.json()
            sections = result_json['parse']['sections']
            section_array = []
            for section in sections:
                _2number = section['number'].split(".")
                if len(_2number) > 1 and _2number == 1:
                    section_array += [section['index'], ]

            if len(section_array) == 0:
                section_array = ["1", ]

            result_response = section_array
        except:
            result_repsonse = "Parsing error"

    return {
        "response": result_response,
        "status": result.status_code,
    }


def queryTitles(titles):
    result = requests.get(API_URL, params={
        "format": "json",
        "action": "query",
        "redirects": "",
        "titles": titles
    })
    if result.status_code == 200:
        try:
            result_json = result.json()
            pages = result_json['query']['pages']
            result_response = ""
            for page in pages.keys():
                result_response = page
                break
        except:
            result_repsonse = "Parsing error"
    else:
        result_response = ""

    return {
        "response": result_response,
        "status": result.status_code,
    }
