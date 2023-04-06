# -*- coding: utf-8 -*-
"""
voice message
b'<xml><ToUserName><![CDATA[gh_52f70b25a9b5]]></ToUserName>\n<FromUserName><![CDATA[oJo_v06K5xUTXXGoKSCpBVHrHKmM]]></FromUserName>\n<CreateTime>1646914232</CreateTime>\n<MsgType><![CDATA[voice]]></MsgType>\n<MediaId><![CDATA[-bRr-dLVIZvuqjP4J3xaQJcwwnfKrAJon9CidqIP9vc53AfIXgA7r0YTSfDaPyaZ]]></MediaId>\n<Format><![CDATA[amr]]></Format>\n<MsgId>23578144969699076</MsgId>\n<Recognition><![CDATA[]]></Recognition>\n</xml>'

image message
b'<xml><ToUserName><![CDATA[gh_52f70b25a9b5]]></ToUserName>\n<FromUserName><![CDATA[oJo_v06K5xUTXXGoKSCpBVHrHKmM]]></FromUserName>\n<CreateTime>1646914714</CreateTime>\n<MsgType><![CDATA[image]]></MsgType>\n<PicUrl><![CDATA[http://mmbiz.qpic.cn/mmbiz_jpg/4q4d8FsN3E15G6wPSiaqdib9bMVu6ia1W6HF9iaAiau2omq9NBRpo76vPOhUIbmiarhPxq9sTqgkIyQWsFCrxWk2KXQg/0]]></PicUrl>\n<MsgId>23578149529141267</MsgId>\n<MediaId><![CDATA[MR-2EQSUZZmzWvLXfoOK5YDYqSv3Ua5P_M5trcw2tcpURGddrQmqldk-5ClyddBL]]></MediaId>\n</xml>'
http://mmbiz.qpic.cn/mmbiz_jpg/4q4d8FsN3E15G6wPSiaqdib9bMVu6ia1W6HF9iaAiau2omq9NBRpo76vPOhUIbmiarhPxq9sTqgkIyQWsFCrxWk2KXQg/0


"""

import os
import sys

import xmltodict
from flask import Flask, request, abort
from wechatpy import parse_message, create_reply
from wechatpy.exceptions import (
    InvalidSignatureException,
    InvalidAppIdException,
)
from wechatpy.utils import check_signature, to_text

from log import logger
from .local.first_message import send_first_message
# from .utils.basic import get_real_name
import func_config

# here to set your custom token, e.g.: abcde
TOKEN = os.getenv("token", "")
AES_KEY = os.getenv("aes_key", "")
APPID = os.getenv("app_id", "")
KEYWORD_TODO = "todo"
KEYWORD_TEXT = "text"
KEYWORD_VOICE = "voice"
KEYWORD_CHINESE = ["记录", "展示"]

app = Flask(__name__)


@app.route("/")
def index():
    return "index"
    # host = request.url_root
    # return render_template("index.html", host=host)


@app.route("/wx", methods=["GET", "POST"])
def wechat():
    logger.info("request: " + str(request))
    signature = request.args.get("signature", "")
    timestamp = request.args.get("timestamp", "")
    nonce = request.args.get("nonce", "")
    encrypt_type = request.args.get("encrypt_type", "raw")
    msg_signature = request.args.get("msg_signature", "")

    try:
        check_signature(TOKEN, signature, timestamp, nonce)
        logger.info("token: " + TOKEN)
    except InvalidSignatureException:
        abort(403)

    if request.method == "GET":
        echo_str = request.args.get("echostr", "")
        return echo_str

    # POST request
    elif encrypt_type == "raw":
        # plaintext mode
        logger.info("request.data")
        logger.info("request.data type: " + str(type(request.data)))
        logger.info("request.data content: " + str(request.data))

        from_user_name, message, message_type, msg = extract_field_from_request_data()

        # if someone subscribes, send init message
        subscribe = is_subscribe(message, message_type)
        if subscribe:
            reply = create_reply(send_first_message(), msg)
            return reply.render()

        if msg.type == "text":
            reply = reply_text_msg(msg, from_user_name)
            # username = get_real_name(from_user_name)
            username = ''
            msg_strip = str(msg).strip()
            for keyword_chinese in KEYWORD_CHINESE:
                if keyword_chinese in msg_strip:
                    log_msg = "---".join(
                        [KEYWORD_TODO, KEYWORD_TEXT, username, msg_strip]
                    )
                    logger.info(log_msg)

            log_msg = "---".join([username, msg_strip])
            logger.info(log_msg)

        elif msg.type == "voice":
            message = xmltodict.parse(to_text(request.data))["xml"]
            recognition = message["Recognition"]
            msg_strip = str(recognition).strip()
            # username = get_real_name(from_user_name)
            username = ''
            logger.info("Recognition: " + msg_strip)

            for keyword_chinese in KEYWORD_CHINESE:
                if keyword_chinese in msg_strip:
                    log_msg = "---".join(
                        [KEYWORD_TODO, KEYWORD_VOICE, username, msg_strip]
                    )
                    logger.info(log_msg)

            log_msg = "---".join([username, msg_strip])
            logger.info(log_msg)

            reply = reply_voice_msg(msg, from_user_name, str(recognition))
        else:
            reply = create_reply("Sorry, can not handle this for now.", msg)
        return reply.render()
        # return reply
    else:
        # encryption mode
        from wechatpy.crypto import WeChatCrypto

        crypto = WeChatCrypto(TOKEN, AES_KEY, APPID)
        try:
            msg = crypto.decrypt_message(request.data, msg_signature, timestamp, nonce)
        except (InvalidSignatureException, InvalidAppIdException):
            abort(403)
        else:
            msg = parse_message(msg)
            if msg.type == "text":
                reply = create_reply(msg.content, msg)
            else:
                reply = create_reply("Sorry, can not handle this for now", msg)
            return crypto.encrypt_message(reply.render(), nonce, timestamp)


def extract_field_from_request_data():
    message = xmltodict.parse(to_text(request.data))["xml"]
    from_user_name = message["FromUserName"]
    logger.info("FromUserName: " + str(from_user_name))

    message_type = message["MsgType"].lower()
    logger.info("MsgType: " + str(message_type))

    msg = parse_message(request.data)
    logger.info("msg")
    logger.info("msg type: " + str(type(msg)))
    logger.info("msg content: " + str(msg))

    return from_user_name, message, message_type, msg


def is_subscribe(message, message_type):
    if message_type == "event" or message_type.startswith("device_"):
        if "Event" in message:
            logger.info("event in message")
            event_type = message["Event"].lower()
        else:
            event_type = ""

        if event_type == "subscribe":
            return True
        else:
            return False


def reply_voice_msg(msg, user, content):
    logger.info("voice mode, in replay message")
    logger.info("voice mode, content type: " + str(type(content)))
    logger.info("voice mode, content: " + str(content))
    result = map_voice_keyword_to_func(content, user)

    reply = create_reply(result, msg)
    return reply


def reply_text_msg(msg, user):
    content: str = msg.content.strip()
    logger.info("text mode, in replay message")
    logger.info("text mode, content type: " + str(type(content)))
    logger.info("text mode, content: " + content)
    result = map_text_keyword_to_func(content, user)

    # todo reply image
    # if "冰墩墩" in content:
    #     image_reply = ImageReply()
    #     image_reply.media_id = (
    #         "CVE-AgGLEVfYepyn0TvydL3F1XLB81xelAgesq7gd6-muClBXq0K2IHbKk8g-6aN"
    #     )
    #     reply = create_reply(image_reply, msg)
    #     logger.info("image: " + str(reply))
    #     return reply

    reply = create_reply(result, msg)
    return reply


def map_voice_keyword_to_func(content, user):
    if not content:
        return " "

    voice_keywords = func_config.voice_keyword_func_dict

    for k, v in voice_keywords.items():
        if k in content.lower():
            result = v()
            logger.info("voice mode, result")
            logger.info("voice mode, result type: " + str(type(result)))
            logger.info("voice mode, result content: " + str(result))
            return str(result)
    return ""


def map_text_keyword_to_func(content, user):
    if not content:
        return ""

    keyword = content.split()[0].replace("。", "")

    keyword_action_dict = func_config.text_keyword_func_dict
    # keyword_action_dict = {
    #     "历史": {"func": today_in_history, "param": ""},
    #     "history": {"func": today_in_history, "param": ""},
    #     # "冰墩墩": {"func": bingdwendwen, "param": ""},
    #     # "泡泡": {"func": bubble, "param": ""},
    #     "新闻": {"func": get_news_60s, "param": ""},
    #     "news": {"func": get_news_60s, "param": ""},
    #     "翻译": {"func": translate, "param": (content,)},
    #     "translate": {"func": translate, "param": (content,)},
    #     "计算": {"func": calc, "param": (content, user)},
    #     "calc": {"func": calc, "param": (content, user)},
    # }
    func = keyword_action_dict.get(keyword, {}).get("func", "")
    param_raw = keyword_action_dict.get(keyword, {}).get("param", "")
    if param_raw == 'content':
        param = (content, )
    elif param_raw == 'content,user':
        param = (content, user)
    else:
        param = ''

    logger.info("text mode, execute function: " + str(func))
    logger.info("text mode, params: " + str(param))

    if not func:
        return ""

    if param:
        result = func(*param)
    else:
        result = func()
    result = str(result)
    logger.info("text mode, result")
    logger.info("text mode, result type: " + str(type(result)))
    logger.info("text mode, result content: " + str(result))
    return result


def main():
    app.run("0.0.0.0", 8081, debug=True)


# if __name__ == '__main__':
#     try:
#         run()
#     except BrokenPipeError as exc:
#         sys.exit(exc.errno)
