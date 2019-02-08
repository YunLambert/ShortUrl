# coding:utf-8
import unittest
import requests

local_url = "http://127.0.0.1:8892/apitest"
test_url = "http://47.106.239.198/apitest"


# 本地测试
def local_send_post(data):
    res = requests.post(url=local_url, data=data)
    print(res.json())
    return res.json()


# 线上(服务器)测试
def send_post(data):
    res = requests.post(url=test_url, data=data)
    print(res.json())
    return res.json()


class TestMethod(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("开始测试....")

    @classmethod
    def tearDownClass(cls):
        print("结束测试....")

    # 每次方法之前执行
    def setUp(self):
        print("-------------->Case")

    # #每次方法之后执行
    # def tearDown(self):
    #     print("--------------------")

    def test_01(self):
        print("Test1:传入新长url 返回 短url:")
        data = {
            'url': "http://yz.uestc.edu.cn/xinwenzhongxin/yaowen/2017/09/29/31.html"  # 新长链接
        }
        res = local_send_post(data)
        print(res)
        # self.assertEqual(res,1000,"测试失败")

    def test_02(self):
        print("Test2:传入已有的长url 返回 已有的短url:")
        data = {
            'url': "https://www.cnblogs.com/gavinyyb/p/6413467.html"   # 已有的长链接
        }
        res=local_send_post(data)
        print(res)
        self.assertEqual(res['result'],"47.106.239.198/VfIazv","测试失败！")

    def test_03(self):
        print("Test3:传入自定义新长url与自定义短url:")
        data = {
            'url1': "https://blog.csdn.net/zhangxiaoxiang/article/details/835879",   # 已有的长链接
            'url2':"http://47.106.239.198/aaaaaaa"
        }
        res=local_send_post(data)
        print(res)

    def test_04(self):
        print("Test4:传入自定义(选项)新长url 返回 短url:")
        data = {
            'custom_url': "https://blog.csdn.net/leixiaohua1020/article/details/46754977",   # 已有的长链接
            'radios':"47.106.239.198",
            'selectlength':"8"
        }
        res=local_send_post(data)
        print(res)

    def test_05(self):
        print("Test5:传入无法访问的长url 返回 无法访问报错信息:")
        data = {
            'url': "https://blog.csdn.net/leixiaohua1020/article/details/4675497",   # 无法访问的长链接
        }
        res=local_send_post(data)
        print(res)

    def test_06(self):
        print("Test6:访问短url 至 相应的长url:")
        res = requests.post(url="http://47.106.239.198/IAeeyv")
        self.assertEqual(res.status_code, 200, "测试失败！")

    def test_07(self):
        print("Test7:传入短url 返回 已经为短链接报错信息:")
        data = {
            'url': "http://47.106.239.198/IAeeyv",
        }
        res = local_send_post(data)
        print(res["result"])


if __name__ == "__main__":
    unittest.main()
