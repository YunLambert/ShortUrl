# ShortUrl
A web application to make url short using Aliyun.

## 完成程度

- [X] 输入长链接，可以生成短链接
- [X] 访问短链接，跳转到长链接
- [X] 支持访问计数
- [X] 支持自定义短链，可以指定字符串作为短链的key
- [X] 数据库表设计和对外的HTTP接口
- [X] 支持配置功能，自定义长度、前缀
- [X] 测试代码的编写

## 具体设计

真实可运行的短网址服务网站yunlambert.top(网站备案没有完成，无法直接通过域名访问，**可以直接访问服务器[47.106.239.198](47.106.239.198)**)

### 压缩算法
1.将长网址 md5 生成 32 位签名串,分为 4 段, 每段 8 个字节
2.对这四段循环处理, 取 8 个字节, 将他看成 16 进制串与 0x3fffffff(30位1) 与操作, 即超过 30 位的忽略处理(使用e，所以不做处理)
3.这 30 位分成 6 段, 每 5 位的数字作为字母表的索引取得特定字符, 依次进行获得 6 位字符串（增加一个e组成6位串，减小冲突）
4.总的 md5 串可以获得 4 个 6 位串,取里面的任意一个就可作为这个长 url 的短 url 地址

### 服务框架

基于python的flask web框架进行设计

使用Nginx进行服务器部署

数据库使用MySQL,~~ttserver~~

### 界面设计

![image.png](https://upload-images.jianshu.io/upload_images/7154520-b2c6f8178a47bf19.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

基于BootStrap进行前端界面的编写。

### 数据库表设计

![image.png](https://upload-images.jianshu.io/upload_images/7154520-df1b980ed0f77b2f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

id 序列标号

longurl 长链接

shorturl  短链接

IsSelf  是否为自定义的短链接

inserDate  插入日期

count 访问计数

### 测试

利用python的unittest进行单元测试，测试了以下几种情况:

- 传入新长url 返回 新短url
- 传入已有的长url 返回 已有的短url
- 传入不存在的长url 返回 报错信息(url不可达)
- 传入短url 返回 报错信息(已经为短url)
- 访问短url 可以 访问相应的长url

Thanks for using ShortUrl !

