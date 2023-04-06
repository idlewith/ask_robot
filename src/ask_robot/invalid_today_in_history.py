import datetime
import json

import requests

from local import (
    gen_today_file_name,
    is_today_file_exist,
    read_local_file,
    write_local_file,
)


def get_month_day(param):
    if not param:
        return ""

    month, day = param.split("/")
    month = str(int(month))
    day = str(int(day))
    return f"{month}月{day}日"


def format_data(data: dict) -> str:
    """
    join each title by `\\n`

    Args:
        data: json data

    Returns:
        formatted text
    """
    events = []
    month_day_str = get_month_day(data.get("day", ""))
    for i in data.get("data", []):
        year = i.get("year", datetime.datetime.now().year)
        title = i.get("title", "")
        events.append(f"{year}, {title}")

    return "\n".join(
        ["历史上的今天", f"不同年份的{month_day_str}发生的事件: \n", "\n\n".join(events)]
    )


def get_data() -> dict:
    """
    data source, use requests get data

    Returns:
        python dict from api
    """
    url = "https://query.asilu.com/today/list/"

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'query.asilu.com',
        'If-Modified-Since': 'Mon, 20 Mar 2023 15:37:52 GMT',
        'If-None-Match': 'Ja d41d8cd98f00b204e9800998ecf8427e-20170627',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers).text
    response = json.loads(response)
    return response


def get_today_in_history():
    file_today = gen_today_file_name("today_in_history-%s.json")
    today_file_exist = is_today_file_exist(file_today)

    if today_file_exist:
        print("local file exist, get data from local file: %s" % file_today)
        data = read_local_file(file_today)
    else:
        print("local file not exist, get data from api")
        data = get_data()
        print(data)
        write_local_file(file_today, data)

    data = format_data(data)
    return data


if __name__ == "__main__":
    r = get_today_in_history()
    print(r)
