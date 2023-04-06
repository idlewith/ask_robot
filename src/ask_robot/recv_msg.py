import re
from .logger import logger

from .msg_handle import text_handle_list
from .chatgpt import  query_chatgpt

ROBOT_NAME = "idlewith"
api_key_list = []
restrict_times = 20  # upper limit for single person for every day
restrict_word_len = 2500  # limit of input word


def is_help(text):
    # return bool(re.match(r"\?|？|help", text))
    return bool(re.match(r"^[？?]$", text))


def get_help_info(receiver, msg_type=""):
    help_info = []
    help_info.append('输入"?"获取帮助信息')
    num = 0
    for index, rule in enumerate(text_handle_list):
        if rule["whitelist"] and receiver not in rule["whitelist"]:
            continue
        # if rule["type"] != msg_type and rule["type"] != type_all:
        #     continue
        num += 1
        help_info.append(f"{num}: {rule['help']}")

    # help_url = "https://idlewith.com/help"
    # help_info.append(f"\n详情可参考: {help_url}")
    help_info.append("以上信息均来自互联网，仅供参考学习使用。")
    return "\n\n".join(help_info)


def ai_chat(msg):
    """
    AI聊天
    1、出于信息安全等考虑，增加了输入长度限制和敏感词校验
    2、单个人每天的访问会有限制
    3、首次使用会进行提醒
    """
    return "未实现"
    # api_key_info = get_chatgpt_sk(msg.reply_id)
    #
    # if api_key_info:
    #     openai_key = str(api_key_info, "utf-8")
    #     personal_flag = True
    # else:
    #     openai_key = random.choice(api_key_list)
    #     personal_flag = False
    #
    # sensitive_words = word_detected(msg.text)
    # if len(msg.text) > restrict_word_len:
    #     word = f"tips:聊天功能为第三方接口，为避免无意的信息泄漏，输入限制长度为：{restrict_word_len}"
    # elif sensitive_words:
    #     record_sensitive_words(
    #         f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:{msg.sender} {msg.text}{str(sensitive_words)}"
    #     )
    #     word = "tips:包含敏感词汇，请注意！（或误判）"
    # else:
    #     word = chatgpt(msg, openai_key, personal_flag)
    #
    # if word:
    #     send_msg(word, msg.reply_id)


def handle(msg, user):
    receiver = user
    if is_help(msg):
        return get_help_info(receiver)

    for rule in text_handle_list:
        if not re.match(rule["pattern"], msg):
            continue
        if rule["whitelist"] and receiver not in rule["whitelist"]:
            continue
        # if rule["type"] != msg_type and rule["type"] != type_all:
        #     continue
        text = rule["func"](msg, receiver)

        logger.info(f"text mode, execute function: {str(rule['func'])}")
        logger.info(f"text mode, msg: {msg}, user: {user}")

        logger.info(f"text mode, text")
        logger.info(f"text mode, result type: " + str(type(text)))
        logger.info(f"text mode, result content: " + str(text))

        return text

    text = query_chatgpt(msg)
    logger.info("text mode, text")
    logger.info("text mode, result type: " + str(type(text)))
    logger.info("text mode, result content: " + str(text))
    return text
