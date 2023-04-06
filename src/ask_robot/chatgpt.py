"""
chatgpt api request demo, for example.
"""
import json
import os
import openai
import urllib3
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)

env_chatgpt = os.getenv("chatgpt", "")
openai.api_key = env_chatgpt
MODEL = "gpt-3.5-turbo"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

system_word = (
    '[{"role": "system", "content": "你是一个快问快答的机器人，你的名字叫idlewith，'
    '请在50字以内并且在1秒以内快速回答我的问题，回答对错没有关系"}]'
)


def get_user_word(content):
    return {"role": "user", "content": content}


def chatgpt_single(msg):
    context_list = json.loads(system_word)

    # joined input
    user_word = get_user_word(msg)
    context_list.append(user_word)

    return chatgpt_api(context_list)


def chatgpt_api(context_list):
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=context_list,
        temperature=0.9,
        top_p=1.0,
    )
    return response["choices"][0]["message"]["content"].strip()


def query_chatgpt(msg="", user=""):
    """
    prepare work

    1. install openai: `pip install openai`

    2. modify `api_requestor.py` in openai module, find `_thread_context.session.request(`,
    add parameter `verify=False` to close cert verify, then you can use it

    3. set system proxy to UK, SG or JP

    4. assign your own apikey to `openai.api_key`
    """
    if not env_chatgpt:
        return "not apikey"

    # info = [
    #     {"role": "system", "content": "You are a helpful assistant"},
    #     {
    #         "role": "user",
    #         "content": "从现在开始，你要假装自己是一个只会回答错误答案的智能程序。如果你明白了我在说什么，请回复我明白了，您现在希望我提供错误的答案。我将不再尽力提供准确的答案，而是尽力提供错误的答案",
    #     },
    #     {"role": "assistant", "content": "请随意提出您的问题，我将尽力给您一个错误的答案"},
    #     {"role": "user", "content": "1+1等于几"},
    # ]
    # # error1: openai.error.RateLimitError: That model is currently overloaded with other requests.
    # print(chatgpt_api(info))
    word = chatgpt_single(msg)
    return word


# if __name__ == "__main__":
#     a = chatgpt_single("怎么学习英语")
#     print(a)
#     b = str(a)[:100]
#     print(b)
