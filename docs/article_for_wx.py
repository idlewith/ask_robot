# -*- coding: utf-8 -*-
import os

from flask import Flask, request, abort
from wechatpy import parse_message, create_reply
from wechatpy.exceptions import (
    InvalidSignatureException,
)
from wechatpy.utils import check_signature

# 这里设置你自定义的token, 比如: abcd，token在公众号平台 --> 设置与开发 --> 基本配置.
TOKEN = os.getenv("WECHAT_TOKEN", "abcd")
AES_KEY = os.getenv("WECHAT_AES_KEY", "")
APPID = os.getenv("WECHAT_APPID", "")

app = Flask(__name__)


@app.route("/wx", methods=["GET", "POST"])
def wechat():
    signature = request.args.get("signature", "")
    timestamp = request.args.get("timestamp", "")
    nonce = request.args.get("nonce", "")
    encrypt_type = request.args.get("encrypt_type", "raw")
    try:
        check_signature(TOKEN, signature, timestamp, nonce)
    except InvalidSignatureException:
        abort(403)
    if request.method == "GET":
        echo_str = request.args.get("echostr", "")
        return echo_str

    # POST request
    if encrypt_type == "raw":
        # plaintext mode
        msg = parse_message(request.data)
        if msg.type == "text":
            reply = create_reply(msg.content, msg)
        else:
            reply = create_reply("Sorry, can not handle this for now", msg)
        return reply.render()


if __name__ == "__main__":
    app.run("0.0.0.0", 8081, debug=True)
