import json

import requests

from utils.basic import (
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
    for i in data.get("result", []):
        date = i.get("date", "").split("年")[0] + "年"
        title = i.get("title", "")
        events.append(", ".join([date, title]))

    return "\n".join(["历史上的今天", f"不同年份的{month_day_str}发生的事件: \n", "\n\n".join(events)])


def get_data() -> dict:
    """
    data source, use requests get data

    Returns:
        python dict from api
    """
    url = "https://api.oick.cn/lishi/api.php"
    response = requests.get(url).text
    response = json.loads(response)
    return response


def today_in_history():

    file_today = gen_today_file_name("today_in_history-%s.json")
    today_file_exist = is_today_file_exist(file_today)

    if today_file_exist:
        print("local file exist, get data from local file: %s" % file_today)
        data = read_local_file(file_today)
    else:
        print("local file not exist, get data from api")
        data = get_data()
        write_local_file(file_today, data)

    data = format_data(data)
    return data


if __name__ == "__main__":
    r = today_in_history()
    print(r)
