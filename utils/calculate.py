from utils import config
from utils import logger


def format_output(result):
    expr_str = str(result)
    if "." in expr_str:
        suffix = expr_str.split(".")[1]
        if len(suffix) > 2:
            return "%.5f" % result
        else:
            return str(result)
    else:
        return int(result)


def has_permission(user):
    if user in config.calc_permission_list:
        return True
    else:
        return False


def calc(string, user):
    logger.logger.info("calc string: " + str(string))
    logger.logger.info("user: " + str(user))

    if len(string.split()) <= 1:
        return "没有表达式"  # no expression

    # remove permission at the moment, 先移除权限校验，估计要几年后才能添加了
    if has_permission(user):
        return "不在允许请求的范围内"  # not paid

    expression = " ".join(string.split()[1:])
    try:
        eval_expr = eval(expression)
        result = format_output(eval_expr)
        return result
    except (SyntaxError, TypeError):
        return "表达式不正确"  # expression has error


if __name__ == "__main__":
    # result = calc('calculate 469/6%3/8646/3%6')
    r = calc("计算 469/6%3/8646/3%6", "")
    print(r)
