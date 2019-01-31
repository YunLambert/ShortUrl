import math
from shorturl.config import config


def x_to_ten(number):
    res = 0
    length = len(number)
    for i in range(length):
        res += config.code_map.index(number[i]) * pow(62, length - i - 1)
    return res


def ten_to_x(number):
    if number == 0:
        return 0
    rest = int(number)
    res = []
    while rest != 0:
        shang, mod = divmod(rest, 62)
        res.insert(0, config.number_map[mod])
        rest = shang
    return ''.join(res)


print(ten_to_x('10'))
