import xml.etree.ElementTree as ET
from datetime import datetime

import requests

from .local import (
    gen_today_file_name,
    is_today_file_exist,
    read_local_file,
    write_local_file,
)


sina_news_pattern = r"^(新浪新闻|sina news).*"


def get_xml():
    url_sina = "https://sina-news.vercel.app/rss.xml"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like"
            " Gecko) Chrome/54.0.2840.90 Safari/537.36"
        )
    }

    html_obj = requests.get(url_sina, headers=headers)
    response = html_obj.text
    return response


def get_field(item, field):
    try:
        title = item.find(field).text
        return title
    except AttributeError:
        return ""


def date_str2date(date_str):
    return datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")


def date2date_str(date: datetime):
    weekday = gen_weekday_to_cn(date.strftime("%A"))
    return date.strftime("%m-%d %H:%M") + f"({weekday})"


def gen_weekday_to_cn(weekday):
    en_cn_dict = {
        "Monday": "星期一",
        "Tuesday": "星期二",
        "Wednesday": "星期三",
        "Thursday": "星期四",
        "Friday": "星期五",
        "Saturday": "星期六",
        "Sunday": "星期天",
    }
    return en_cn_dict.get(weekday, "")


def add_href(date_str, link):
    tag_a = f'<a href="{link}" target="_blank">{date_str}</a>'
    return tag_a


def extract(response):
    if not response:
        return ""

    root = ET.fromstring(response)

    items = []
    for item in root.find("channel").findall("item"):
        title = get_field(item, "title").strip()
        link = get_field(item, "link").strip()
        pub_date = get_field(item, "pubDate")
        pub_date = date_str2date(pub_date)
        items.append([pub_date, title, link])
    sorted_items = sorted(items, key=lambda x: x[0], reverse=True)

    n = []
    for item in sorted_items:
        date, title, link = item
        date_str = date2date_str(date)
        date_str = add_href(date_str, link)
        n.append("<br>".join([date_str, title]))
    return "<br><br>".join(n)


def get_sina_news(msg="", user=""):
    file_today = gen_today_file_name("sina-news-60s-%s.txt")
    today_file_exist = is_today_file_exist(file_today)

    if today_file_exist:
        data = read_local_file(file_today)
        data = data.replace("\n", "<br>")
    else:
        data = get_xml()
        data = extract(data)
        if data:
            write_local_file(file_today, data)
    return data


# if __name__ == "__main__":
#     data = get_sina_news()
#     print(data)
