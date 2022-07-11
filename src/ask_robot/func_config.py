from .local.calculate import calc
from .web.news_60s import get_news_60s
from .web.sina_news import get_sina_news
from .web.translate import trans
from .web.today_in_history import get_today_in_history


voice_keyword_func_dict = {
    "新闻": get_news_60s,
    "news": get_news_60s,
    "history": get_today_in_history,
    "历史": get_today_in_history,
}

text_keyword_func_dict = {
    "历史": {"func": get_today_in_history, "param": ""},
    "history": {"func": get_today_in_history, "param": ""},
    "新闻": {"func": get_news_60s, "param": ""},
    "news": {"func": get_news_60s, "param": ""},
    "翻译": {"func": trans, "param": "content"},
    "translate": {"func": trans, "param": "content"},
    "计算": {"func": calc, "param": "content,user"},
    "calc": {"func": calc, "param": "content,user"},
}
