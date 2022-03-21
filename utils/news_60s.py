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
        if len(limit_str) > 750:
            return "\n\n".join(limit_list[:-1])
        else:
            limit_list.append(row)

    return data


def get_news_60s():
    file_today = gen_today_file_name("news-60s-%s.txt")
    today_file_exist = is_today_file_exist(file_today)

    if today_file_exist:
        logger.logger.info(
            "local file exist, get data from local file: %s" % file_today
        )
        data = read_local_file(file_today)
    else:
        logger.logger.info("local file not exist, get data from api")
        data = _get_news_60s()
        if data:
            write_local_file(file_today, data)

    # data = '3月5日，农历二月初三，星期六！\n\n在这里，每天60秒读懂世界！\n\n1、香港：4日新增确诊52523例，新增死亡136例，大多为65岁以上长者；\n\n2、全国政协委员花亚伟：建议允许年满30周岁以上的未婚女性生育一胎，且享受合法生育的产假、生育保险等一切权利；全国人大代表李君：应全面禁止未成年人玩网络游戏，强制设置人脸识别登陆；\n\n3、两高：制售假劣药以孕产妇、儿童为使用对象将酌情从重处罚；\n\n4、广西一夫妇年龄差30岁在21年间生育15孩，官方：2016年曾调查， 将再次深入核实；\n\n5、"买下半个英国"的李嘉诚家族计划出售其旗下英国配电公司UK Power Networks，估值高达150亿英镑(约1264亿元)，有分析认为，英国脱欧后，部分政客鼓吹将公用事业收归公有，近期俄乌冲突冲击英国经济，可能是其出售资产的原因；\n\n6、外媒：法国总统马克龙当地3日正式宣布竞选连任，最新民调显示马克龙在首轮投票中的支持率为28%排在首位；\n\n7、当地4日，巴基斯坦一清真寺发生自杀式袭击，致56死194伤，警方：2名恐怖分子试图闯入清真寺，与警察交火不久后清真寺内发生爆炸。目前尚无任何组织或个人宣称负责；\n\n8、摩根大通：如俄石油供应持续遭受欧美制裁，国际油价有望飙涨至185美元；外媒：利比亚最大的油田停产，或与该国政局不稳及俄乌冲突有关；欧盟多国考虑恢复煤电，以摆脱对俄天然气的依赖；\n\n9、柬埔寨"血奴"案当事人和3名涉案人员被控煽动歧视罪等多项罪名，已被羁押候审；\n\n10、韩媒：4日上午，韩国核电站附近燃起山火，近4000居民被紧急疏散；\n\n11、北溪-2天然气管道公司：未申请破产，只是关闭了网站；\n\n12、俄方称乌克兰总统已离乌，目前在波兰。乌方随后否认；德总理：暂不考虑乌克兰加入欧盟事宜；\n\n13、印媒：印度东部比哈尔邦一家烟花厂3日晚发生爆炸，造成至少10人死亡多人受伤；\n\n14、普京：俄在乌特别军事行动将全面完成既定任务，没有与拜登对话打算；美国防官员：美俄已建立通信渠道，防止出现误判或军事事件；\n\n15、俄乌第二轮谈判就双方临时停火建立人道主义通道达成一致，并同意召开第三轮谈判，可能在5日或6日举行；乌方：扎波罗热核电站已被俄军控制，机组正常工作；'
    data = cut_limit_whole_line(data)
    return data


if __name__ == "__main__":
    r = get_news_60s()
    print(r)
    print(len(r))
    print(type(r))
