import json
from pprint import pprint

import requests


def query(word: str) -> str:
    """
    query word meaning from api

    Args:
        word: word need be translated

    Returns:
        chinese meaning for words.
    """
    url = "https://dict.youdao.com/jsonapi?q=%s" % word

    response: str = requests.get(url).text
    words: dict = json.loads(response)

    try:
        trans = (
            words.get("web_trans", {}).get("web-translation", [])[0].get("trans", [])
        )
        chinese_list = []
        for tran in trans:
            value = tran.get("value", "")
            chinese_list.append(value)
        chinese = ", ".join(chinese_list)
    except IndexError:
        # Please input english word, for example: "translation hello"
        chinese: str = '请输入英文, 例如 "翻译 hello"'
    return chinese


def translate(words):
    if len(words.split()) == 2:
        word = words.split()[1]
        chinese = query(word)
        return chinese
    else:
        # Please input "translation hello"
        return '请输入 "翻译 hello"'


if __name__ == "__main__":
    r = translate("translate hello")
    pprint(r)
