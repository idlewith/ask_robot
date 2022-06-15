def first_message():
    content = (
        "欢迎关注Python脚本，下面是整理的一些Python电子书。\n\n"
        "链接:https://pan.baidu.com/s/1ue8cTKMEEQHTsHMEHHGhWg?pwd=o65q\n"
        "提取码:o65q\n\n"
        "本公众号还提供一些交互式的信息查询关键词，可以获取动态的结果:\n\n"
        '- 回复"历史"或者直接语音说出"历史"两个字，都可以获取历史上的今天发生了什么\n\n'
        '- 回复"冰墩墩"或者直接语音说出"冰墩墩"三个字，都可以获取画冰墩墩的Python代码\n\n'
        '- 回复"翻译 hello"，可以实时获取单词的中文含义，注意hello是可以换成其他单词的\n\n'
        '- 回复"计算 3+2"，可以实时计算你的表达式，同样，表达式也是可以换成其他的表达式的（加减乘除分别对应：+-*/）\n\n'
        '- 回复"新闻"或者直接语音说出"新闻"两个字，都可以获取每日新闻\n\n以上信息均来自互联网，仅供参考学习使用。'
    )
    return content


if __name__ == "__main__":
    a = first_message()
    print(a)
