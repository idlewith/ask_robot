# encoding: utf-8
from datetime import datetime

import bs4
import requests
from bs4 import BeautifulSoup

from utils.basic import (
    gen_today_file_name,
    is_today_file_exist,
    read_local_file,
    write_local_file,
)
from utils import logger


def get_month_day():
    month = datetime.now().month
    day = datetime.now().day
    return f"{month}月{day}日"


def get_article_text(uri_id):
    url_60s = "https://zhuanlan.zhihu.com/p/%s" % uri_id
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36"
    }

    response = requests.get(url_60s, headers=headers)
    response = response.text
    return response


def extract_content(text):
    soup: BeautifulSoup = BeautifulSoup(text, features="html.parser")
    div_content: bs4.element.Tag = soup.find("div", {"class": "Post-RichTextContainer"})

    text_list = []
    for p in div_content.find_all("p"):
        text_p = p.get_text().strip()
        if (
            text_p
            and "微语" not in text_p
            and "每天60秒读懂世界" not in text_p
            and "农历" not in text_p
        ):
            text_list.append(p.get_text().strip())

    result = "\n\n".join(text_list)
    return result


def is_today(title):
    day = title.split("，")[0]
    month = day.split("月")[0]
    day = day.split("月")[1].split("日")[0]

    now_month = str(datetime.now().month)
    now_day = str(datetime.now().day)

    if now_month == month and now_day == day:
        return True
    else:
        return False


def get_article_id(uri):
    id_str = uri.split("/")[-1].strip()
    return id_str


def get_menu_text():
    url_60s_index = "https://www.zhihu.com/people/mt36501"

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36"
    }

    response = requests.get(url_60s_index, headers=headers)
    response = response.text
    return response


def parse_menu(text):
    soup: BeautifulSoup = BeautifulSoup(text, features="html.parser")
    h2_titles: bs4.element.Tag = soup.find("h2", {"class": "ContentItem-title"})

    today = is_today(h2_titles.get_text())
    if not today:
        return ""

    uri_id = get_article_id(h2_titles.find("a").get("href"))
    return uri_id


def _get_news_60s():
    text = get_menu_text()
    uri_id = parse_menu(text)
    if not uri_id:
        return ""

    text_article = get_article_text(uri_id)
    result = extract_content(text_article)
    if not result:
        return ""

    return get_month_day() + "\n\n" + result


def cut_limit_whole_line(data):
    data_list = data.split("\n\n")
    limit_list = []
    for row in data_list:
        if row.endswith("；"):
            row = row[:-1]

        limit_str = "\n\n".join(limit_list)
        if len(limit_str) > 600:
            limit_str = "\n\n".join(limit_list[:-1])
            return limit_str
        else:
            limit_list.append(row)

    return data


def get_news_60s():
    data = _get_news_60s()
    data = cut_limit_whole_line(data)
    return data


if __name__ == "__main__":
    r = get_news_60s()
    print(r)
    print(len(r))
    print(type(r))
