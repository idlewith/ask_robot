import json
import os

import requests


def request_download(img_url, img_save_path):
    r = requests.get(img_url)
    with open(img_save_path, 'wb') as f:
        f.write(r.content)


def get_access_token(appid, secret):
    '''获取access_token,100分钟刷新一次'''

    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(appid,
                                                                                                           secret)
    r = requests.get(url)
    parse_json = json.loads(r.content.decode())
    print(parse_json)

    token = parse_json['access_token']

    return token


def img_upload(mediaType, name):

    app_id = os.getenv('app_id', '')
    secret = os.getenv('secret', '')
    token = get_access_token(app_id, secret)
    url = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s" % (token, mediaType)
    img_path = '/root/code/tmp/b.png'
    request_download('https://idlepig.coding.net/p/image/d/image/git/raw/master/1654018765795.png', img_path)
    files = {'media': open('{}'.format(img_path), 'rb')}
    r = requests.post(url, files=files)
    parse_json = json.loads(r.content.decode())
    print(parse_json)

    return parse_json['media_id']


a = img_upload('image', '0.png')
print(a)
