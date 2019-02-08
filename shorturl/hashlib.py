import hashlib
from shorturl.config import config
import random

"""
1.将长网址 md5 生成 32 位签名串,分为 4 段, 每段 8 个字节
2.对这四段循环处理, 取 8 个字节, 将他看成 16 进制串与 0x3fffffff(30位1) 与操作, 即超过 30 位的忽略处理(使用e，所以不做处理)
3.这 30 位分成 6 段, 每 5 位的数字作为字母表的索引取得特定字符, 依次进行获得 6 位字符串（增加一个e组成6位串，减小冲突）
4.总的 md5 串可以获得 4 个 6 位串,取里面的任意一个就可作为这个长 url 的短 url 地址
"""


def get_md5(s):
    s = s.encode('utf8')
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()


def get_hash_key(long_url):
    urls = []
    hex = get_md5(long_url)
    for i in range(0, 4):
        n = int(hex[i * 8:(i + 1) * 8], 16)
        v = []
        e = 0
        for j in range(0, 5):
            x = 0x0000003D & n
            e |= ((0x00000002 & n) >> 1) << j  # 把每次循环没有使用的第二个bit保存到e里面
            v.insert(0, config.code_map[x])
            n = n >> 6  # 采取位运算，因为来回转换str和int会损失精度
        e |= n << 5  # v的后5位由x决定，第一位由e来决定
        v.insert(0, config.code_map[e & 0x0000003D])
        urls.append(''.join(v))
    return urls


def get_short_url(s):
    i = random.randint(0, 3)
    # s = "yunlambert.top/" + get_hash_key(s)[i]
    s = "http://47.106.239.198/" + get_hash_key(s)[i]
    return s


def get_short_url_custom(s, n, x):
    t = get_hash_key(s)
    total = t[0] + t[1] + t[2] + t[3]
    s ="http://"+ x + "/" + total[:n]  # n的范围为6-24
    return s

# if __name__ == '__main__':
#     print("https://yun.io/" + get_hash_key('http://pythontab.com')[0])
