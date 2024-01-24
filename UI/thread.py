from PyQt5.QtCore import QThread, pyqtSignal
import requests
import re
import json
import math
import time
import random
from service.service import *

class WorkThread(QThread):
    # 使用信号和UI主线程通讯，参数是发送信号时附带参数的数据类型，可以是str、int、list等
    querySignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(WorkThread, self).__init__(parent)
        # 是否爬取
        self.IsCrawl = True

    def run(self):
        self.scorenotification()
        return
    
    def rsa_no_padding(self,src, modulus, exponent):
        m = int(modulus, 16)
        e = int(exponent, 16)
        t = bytes(src, 'ascii')
        # 字符串转换为bytes
        input_nr = int.from_bytes(t, byteorder='big')
        # 将字节转化成int型数字，如果没有标明进制，看做ascii码值
        crypt_nr = pow(input_nr, e, m)
        # 计算x的y次方，如果z在存在，则再对结果进行取模，其结果等效于pow(x,y) %z
        length = math.ceil(m.bit_length() / 8)
        # 取模数的比特长度(二进制长度)，除以8将比特转为字节
        crypt_data = crypt_nr.to_bytes(length, byteorder='big')
        # 将密文转换为bytes存储(8字节)，返回hex(16字节)
        return crypt_data.hex()

    def updatescore(self,xuenian=None):
        session = requests.session()

        # 打开网站
        res = session.get('https://zjuam.zju.edu.cn/cas/login?service=http://zdbk.zju.edu.cn/jwglxt/xtgl/login_ssologin.html')
        # 获取execution的值以用于登录
        execution = re.findall(r'<input type="hidden" name="execution" value="(.*?)" />', res.text)[0]
        # 获取RSA公钥
        res = session.get('https://zjuam.zju.edu.cn/cas/v2/getPubKey')
        modulus = res.json()['modulus']
        exponent = res.json()['exponent']

        with open('database.json', 'r', encoding="utf-8") as f:
            userdata = json.load(f)
        username = userdata['username']
        password = userdata['password']
        url = userdata.get('url', 'https://oapi.dingtalk.com/robot/send?access_token=')

        rsapwd = self.rsa_no_padding(password, modulus, exponent)

        data = {
            'username': username,
            'password': rsapwd,
            'execution': execution,
            '_eventId': 'submit'
        }
        # 登录
        res = session.post('https://zjuam.zju.edu.cn/cas/login?service=http://zdbk.zju.edu.cn/jwglxt/xtgl/login_ssologin.html', data)
        data["doType"] = "zjsy"
        res = session.post('http://zdbk.zju.edu.cn/jwglxt/xtgl/index_cxLeafGnmkdm.html?gnmkdm=index&su=3220100059', data)
        gnmkdm = ""
        for project in res.json()["result"]:
            if project["gnmkmc"] == "成绩查询":
                gnmkdm = project["gnmkdm"]

        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Redmi K30 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36',
        }

        res = session.post(url=f'http://zdbk.zju.edu.cn/jwglxt/cxdy/xscjcx_cxXscjIndex.html?doType=query&gnmkdm={gnmkdm}&su={username}', data={
            'xn': xuenian,
            'xq': None,
            'zscjl': None,
            'zscjr': None,
            '_search': 'false',
            'nd': str(int(time.time() * 1000)),
            'queryModel.showCount': 5000,
            'queryModel.currentPage': 1,
            'queryModel.sortName': 'xkkh',
            'queryModel.sortOrder': 'asc',
            'time': 0,
        }, headers=headers)

        new_score = res.json()['items']
        
        user = User()
        userscore = user.CrawlerQuery()
        userscore = { item[0]: item[1:] for item in userscore}

        #对比以更新
        for lesson in new_score:
            id = lesson['xkkh']
            name = lesson['kcmc']
            score = lesson['cj']
            credit = lesson['xf']
            gp = lesson['jd']
            year_semester = re.search('(\d{4}-\d{4})-(\d)',id)
            year = year_semester.group(1)
            if year_semester.group(2) == '1':
                semester = '秋冬'
            elif year_semester.group(2) == '2':
                semester = '春夏'
            else:
                semester = '未知'
            if id == '选课课号':
                continue
            if userscore.get(id) != None:
                continue
            
            # 写入数据库
            if user.AddScore(id,year,semester,name,credit,score,gp):
                print('导入发生错误')

            #钉钉推送消息
            try:
                requests.post(url=url, json={
                    "msgtype": "markdown",
                    "markdown" : {
                        "title": "考试成绩通知",
                        "text": """
    ### 考试成绩通知\n
    - **选课课号**\t%s\n
    - **课程名称**\t%s\n
    - **成绩**\t%s\n
    - **学分**\t%s\n
    - **绩点**\t%s """ % (id, name, score, credit, gp)
                    }
                })
            except requests.exceptions.MissingSchema:
                print('The DingTalk Webhook URL is invalid. Please use -d [DingWebhook] to reset it first.')
            
            print('考试成绩通知\n选课课号\t%s\n课程名称\t%s\n成绩\t%s\n学分\t%s\n绩点\t%s' % (id, name, score, credit, gp))
            print()

    def scorenotification(self, xuenian=None):
        try:
            with open("counter.txt", "r", encoding="utf-8") as f:
                times = int(f.read())
        except:
            times = 0
        while True:
            if self.IsCrawl:
                times += 1 
                sign = str(time.strftime("%m-%d %H:%M:%S", time.localtime())) + f" 第 {times} 次运行, "
                print(time.strftime("%m-%d %H:%M:%S", time.localtime()), f"第 {times} 次运行", end='，')
                try:
                    self.updatescore(xuenian)
                    sign += "没有新绩点"
                    print("没有新绩点")
                except Exception as e:
                    sign += str(e)
                    print(str(e))
                finally:
                    self.querySignal.emit(sign)
                    with open("counter.txt", "w", encoding="utf-8") as f:
                        f.write(str(times))
                    time.sleep(random.randint(40, 80))
            else:
                break