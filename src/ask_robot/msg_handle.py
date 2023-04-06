from .calculate import calc, calculate_pattern
from .news_60s import get_news_60s, news_60s_pattern
from .sina_news import get_sina_news, sina_news_pattern
from .translate import trans, trans_pattern


"""
'pattern': 触发的话术
'func': 执行的函数
'whitelist': 白名单，配置后只有白名单会显示此功能。不配置则对所有人可见
'help': ? 帮助提示
没用到，'type': type_personal 个人功能; type_group 群功能; type_all 都适配
"""
voice_handle_list = [
    {
        "pattern": news_60s_pattern,
        "func": get_news_60s,
        "whitelist": [],
        "help": "获取每日新闻",
    },
]


text_handle_list = [
    {
        "pattern": news_60s_pattern,
        "func": get_news_60s,
        "whitelist": [],
        "help": '"新闻": 获取每日新闻',
    },
    {
        "pattern": calculate_pattern,
        "func": calc,
        "whitelist": [],
        "help": '"翻译 hello": 可以实时获取单词的中文含义，注意hello是可以换成其他单词的',
    },
    {
        "pattern": trans_pattern,
        "func": trans,
        "whitelist": [],
        "help": '"计算 3+2": 可以实时计算你的表达式，同样，表达式也是可以换成其他的表达式的（加减乘除分别对应：+-*/）',
    },
]
