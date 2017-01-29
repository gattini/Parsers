# -*- coding: utf-8 -*-
import time, datetime, requests, json

from_date_and_time = "2017-01-29 13:01"  # от какой даты и времени
to_date_and_time = "2017-01-29 16:14"  # до какой даты и времени

class News():
    url = ""
    title = ""
    second_title = ''
    description = ""
    body = ""
    published_at = 0


def encodeTime(string):
    return int(
        time.mktime(
            datetime.datetime.strptime(
                string, "%Y-%m-%d %H:%M").timetuple()
        )
    )


def decodeTime(number):
    return (
        datetime.datetime.fromtimestamp(
            int(number)
        ).strftime('%Y-%m-%d %H:%M:%S')
    )


def getFromUrl(url):
    r = requests.get(url, auth=('usrname', 'password'), verify=False, stream=True)
    r.raw.decode_content = True
    return r.raw.data


def parseCollection(raw_json):
    j_data = json.loads(raw_json)
    return j_data['collection']


def getResponse(page):
    result = []
    chrono = ["news"]  # TODO cards & poligon => "cards", "articles", "shapito", "polygon"
    for c in chrono:
        url = "https://meduza.io/api/v3/search?chrono={}&page={}&per_page=50&locale=ru".format(c, page)
        raw_json = getFromUrl(url)
        collection = parseCollection(raw_json)
        result.extend(collection)
    return result


def getNews(linkTail):
    news = News()
    news.url = "https://meduza.io/api/v3/" + linkTail
    raw_json = getFromUrl(news.url)
    j_data = json.loads(raw_json)

    news.title = j_data['root']['title']
    news.body = j_data['root']['content']['body']
    news.published_at = j_data['root']['published_at']

    if ('second_title' in j_data['root'].keys()):
        news.second_title = j_data['root']['second_title']

    if ('description' in j_data['root'].keys()):
        news.description = j_data['root']['description']

    return news


DIGEST = []

proceed  = True
i = 0
while (proceed):
    collection = getResponse(i)
    i += 1
    for c in collection:
        news = getNews(c)
        if (news.published_at < encodeTime(from_date_and_time)):
            proceed = False
            break
        if (news.published_at < encodeTime(to_date_and_time)):
            #TODO проверка регулярных выражений тут
            DIGEST.append(news)
