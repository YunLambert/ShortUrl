from flask import Flask, render_template, request, redirect, url_for
import requests
from shorturl import hashlib
import model
import json
import re

app = Flask(__name__)
app.config["SECRET_KEY"] = "12345678"


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        data = {}
        short_url = request.form['url']
        # print(short_url)
        response = requests.get(short_url)
        if response.status_code == 302:
            print("redirect!")
            _data = {
                "long_url": short_url,
                "result": short_url + "is already a short url!"
            }
            data = _data
        elif response.status_code == 200:
            res, temp = model.db_query_longurl(short_url)
            if res != 0:  # 数据库中已经有对应长链接的短链接，直接返回即可
                _data = {
                    "long_url": short_url,
                    "result": temp
                }
                data = _data
            else:  # 数据库中没有对应长链接，生成短连接，并判断短链接是否被占用
                url2 = hashlib.get_short_url(short_url)
                res2, g = model.db_query_shorturl(url2)
                if res2 != 0:  # 短链接被占用，需要生成新的
                    url_t = ""
                    for i in range(0, 3):  # 去MD5的4个字段值分别尝试
                        if res2 == 0:
                            break
                        # url_t = "yunlambert.top/" + hashlib.get_hash_key(short_url)[i]
                        url_t = "http://47.106.239.198/" + hashlib.get_hash_key(short_url)[i]
                        res2, g = model.db_query_shorturl(url_t)
                    while (res2 != 0):  # 如果MD5的4个字段值都不满足的话，更换url进行操作
                        url_t = hashlib.get_short_url(url2)
                        res2, g = model.db_query_shorturl(url_t)
                    _data = {
                        "long_url": url2,
                        "result": url_t
                    }
                    data = _data
                else:  # 短链接没有被占用
                    _data = {
                        "long_url": short_url,
                        "result": url2
                    }
                    model.db_add(short_url, url2, 0)
                    data = _data
        else:
            _data = {
                "long_url": short_url,
                "result": "The long url you given is unreachable, please click here to check the origin url."
            }
            data = _data
        return render_template('result0.html', data=data)
    return render_template("index.html")


@app.route('/customization', methods=['POST', 'GET'])
def custom():
    if request.method == 'GET':
        return render_template('Customization.html')
    if request.method == 'POST':
        data = {}
        if 'url1' in request.form and 'url2' in request.form:
            url1 = request.form['url1']
            url2 = request.form['url2']
            if url1 != None and url2 != None:
                # 数据库判断是否已经存在
                res, temp = model.db_query_longurl(url1)
                if (res != 0):
                    _data = {
                        "long_url": url1,
                        "result": "该网址已有短链接:" + temp
                    }
                    data = _data
                else:
                    _data = {
                        "long_url": url1,
                        "result": url2
                    }
                    model.db_add(url1, url2, 1)
                    data = _data
        elif 'radios' in request.form and 'selectlength' in request.form:
            custom_url = request.form["custom_url"]
            radios = request.form["radios"]
            select = request.form["selectlength"]
            s = hashlib.get_short_url_custom(custom_url, int(select), radios)

            res, temp = model.db_query_longurl(custom)
            if (res != 0):
                _data = {
                    "long_url": custom,
                    "result": "该网址已有短链接:" + temp
                }
                data = _data
            else:
                _data = {
                    "long_url": custom_url,
                    "result": s
                }
                model.db_add(custom_url, s, 1)
                data = _data
        else:
            return render_template("Customization.html")
        return render_template('result.html', data=data)


@app.route('/api', methods=['GET'])
def api():
    return render_template("analysis.html")


@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')


@app.route('/<name>')
def match_short_url(name):
    # shorturl = "yunlambert.top/" + name
    shorturl="http://47.106.239.198/"+name
    res, g = model.db_query_shorturl(shorturl)
    if res != 0:
        return redirect(g)
    else:
        print("no")
        return render_template('404.html'), 404


# 开放测试接口
@app.route('/apitest',methods=['POST'])
def api_test():
    data = {}
    if 'url' in request.form:
        short_url = request.form['url']
        # print(short_url)
        response = requests.get(short_url)
        if response.status_code == 302:
            _data = {
                "long_url": short_url,
                "result": short_url + "is already a short url!"
            }
            data = _data
        elif response.status_code == 200:
            res, temp = model.db_query_longurl(short_url)
            if res != 0:  # 数据库中已经有对应长链接的短链接，直接返回即可
                _data = {
                    "long_url": short_url,
                    "result": temp
                }
                data = _data
            else:  # 数据库中没有对应长链接，生成短连接，并判断短链接是否被占用
                url2 = hashlib.get_short_url(short_url)
                res2, g = model.db_query_shorturl(url2)
                if res2 != 0:  # 短链接被占用，需要生成新的
                    url_t = ""
                    for i in range(0, 3):  # 去MD5的4个字段值分别尝试
                        if res2 == 0:
                            break
                        # url_t = "yunlambert.top/" + hashlib.get_hash_key(short_url)[i]
                        url_t="http://47.106.239.198/"+hashlib.get_hash_key(short_url)[i]
                        res2, g = model.db_query_shorturl(url_t)
                    while (res2 != 0):  # 如果MD5的4个字段值都不满足的话，更换url进行操作
                        url_t = hashlib.get_short_url(url2)
                        res2, g = model.db_query_shorturl(url_t)
                    _data = {
                        "long_url": url2,
                        "result": url_t
                    }
                    data = _data
                else:  # 短链接没有被占用
                    _data = {
                        "long_url": short_url,
                        "result": url2
                    }
                    model.db_add(short_url, url2, 0)
                    data = _data
        else:
            _data = {
                "long_url": short_url,
                "result": "The long url you given is unreachable, please click here to check the origin url."
            }
            data = _data
    elif 'url1' in request.form and 'url2' in request.form:
        url1 = request.form['url1']
        url2 = request.form['url2']
        if url1 != None and url2 != None:
            # 数据库判断是否已经存在
            res, temp = model.db_query_longurl(url1)
            if (res != 0):
                _data = {
                    "long_url": url1,
                    "result": "该网址已有短链接:" + temp
                }
                data = _data
            else:
                _data = {
                    "long_url": url1,
                    "result": url2
                }
                model.db_add(url1, url2, 1)
                data = _data
    elif 'radios' in request.form and 'selectlength' in request.form:
        custom_url = request.form["custom_url"]
        radios = request.form["radios"]
        select = request.form["selectlength"]
        s = hashlib.get_short_url_custom(custom_url, int(select), radios)

        res, temp = model.db_query_longurl(custom)
        if (res != 0):
            _data = {
                "long_url": custom,
                "result": "该网址已有短链接:" + temp
            }
            data = _data
        else:
            _data = {
                "long_url": custom_url,
                "result": s
            }
            model.db_add(custom_url, s, 1)
            data = _data
    return json.dumps(data)


@app.route('/api?<name>')
def api_json_custom(name):
    m = name.split("&&")
    data = {}
    if m.size() == 1:
        short_url = re.match(r'url=(.*)', name)
        print(short_url)
        response = requests.get(short_url)
        if response.status_code == 302:
            _data = {
                "long_url": short_url,
                "result": short_url + "is already a short url!"
            }
            data = _data
        elif response.status_code == 200:
            res, temp = model.db_query_longurl(short_url)
            if res != 0:  # 数据库中已经有对应长链接的短链接，直接返回即可
                _data = {
                    "long_url": short_url,
                    "result": temp
                }
                data = _data
            else:  # 数据库中没有对应长链接，生成短连接，并判断短链接是否被占用
                url2 = hashlib.get_short_url(short_url)
                res2, g = model.db_query_shorturl(url2)
                if res2 != 0:  # 短链接被占用，需要生成新的
                    url_t = ""
                    for i in range(0, 3):  # 去MD5的4个字段值分别尝试
                        if res2 == 0:
                            break
                        # url_t = "yunlambert.top/" + hashlib.get_hash_key(short_url)[i]
                        url_t = "http://47.106.239.198/" + hashlib.get_hash_key(short_url)[i]
                        res2, g = model.db_query_shorturl(url_t)
                    while (res2 != 0):  # 如果MD5的4个字段值都不满足的话，更换url进行操作
                        url_t = hashlib.get_short_url(url2)
                        res2, g = model.db_query_shorturl(url_t)
                    _data = {
                        "long_url": url2,
                        "result": url_t
                    }
                    data = _data
                else:  # 短链接没有被占用
                    _data = {
                        "long_url": short_url,
                        "result": url2
                    }
                    model.db_add(short_url, url2, 0)
                    data = _data
        else:
            _data = {
                "long_url": short_url,
                "result": "The long url you given is unreachable, please click here to check the origin url."
            }
            data = _data
    if m.size() == 2:
        url1 = re.match(r"url1=(.*)", m[0])
        url2 = re.match(r"url2=(.*)", m[1])
        res, temp = model.db_query_longurl(url1)
        if (res != 0):
            _data = {
                "long_url": url1,
                "result": "该网址已有短链接:" + temp
            }
            data = _data
        else:
            res2, g = model.db_query_shorturl(url2)
            if res2 != 0:
                _data = {
                    "long_url": url1,
                    "result": "该短链接已被占用:" + g
                }
                data = _data
            else:
                _data = {
                    "long_url": url1,
                    "result": url2
                }
                model.db_add(url1, url2, 1)
                data = _data

    if m.size() == 3:
        custom_url = re.match(r"url=(.*)", m[0])
        radios = re.match(r"domain=(.*)", m[1])
        select = re.match(r"length=(.*)", m[2])

        s = hashlib.get_short_url_custom(custom_url, int(select), radios)

        res, temp = model.db_query_longurl(custom_url)
        if (res != 0):
            _data = {
                "long_url": custom_url,
                "result": "该网址已有短链接:" + temp
            }
            data = _data
        else:
            res2, g = model.db_query_shorturl(s)
            if res2 != 0:
                _data = {
                    "long_url": custom_url,
                    "result": "该短链接已被占用:" + g
                }
                data = _data
            else:
                _data = {
                    "long_url": custom_url,
                    "result": s
                }
                model.db_add(custom_url, s, 1)
                data = _data
    return json.dumps(data)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, port=8892)
