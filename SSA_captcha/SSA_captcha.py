import random
import threading
import time
from datetime import date, timedelta
import re
import requests
import base64
import json
import captchaCv


class CX:
    def __init__(self, phonenums, password, roomid, seatnums):
        self.acc = phonenums
        self.pwd = password
        self.roomid = roomid
        self.seatnums = seatnums
        self.day = (date.today() + timedelta(days=+1)).strftime("%Y-%m-%d")
        self.captcha = None
        self.token = None
        self.pageToken = None
        self.captcha_is = False
        self.session = requests.session()
        # self.session.headers = headers.get_headers()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Mobile Safari/537.36',
            'sec-ch-ua-platform': '"Android"',
            'Referer': 'https://office.chaoxing.com/',
            'Cookie': 'lv=0; fid=1893; _uid=84846687; UID=84846687; vc=2FB1531C4C43D61E837FB017C42B4CA9; vc2=8DE12D07E58159946DDD2DABE9F67A82; xxtenc=c358301df6659bd0e856d7c4de7cee26; KI4SO_SERVER_EC=RERFSWdRQWdsckNwckxwM2pXeFFSY2c4Zmk5aUp5Yzc1clB5V0lGdXVwdzdqVGNTTnlYU01hU3ox%0AenEwWC8yQ0NPdGdxMXhwZmNPcApyTHAzald4UVJUSGN3NUFtdnAvSm1XQjFQUGdHT1NYclJ1a0ZW%0AMy9nZ01FRXdUUWt5Q3dmLzMrakxEN3p0Tmcvek9kZ3N5UTlGTEhPCnhCdXZPbTAvemhndEQ3SHc5%0AcVYxK09nUmVXWVFqNUFJSHAralBJd0xicUpvK002clN1UldwYTROaXU3VnpTUzczQWVka0xZWVVu%0ANlMKalRXWlcxaFNOUzQzNHFzc21RSk9sdWlwRktIdFRZL0lWMHFnWWt4V0w0TlRmUzFkZUt4Sys3%0AT1I2bk5BQWs2VzZLa1VvZTF2ZUpINQp5QnhselVTVnU1MENyRXJTT3owWGNDZG1nakcyQm1yZWp0%0AWUJlcFZ4T0lQYm8zUk9DR1owSEcyRmIxd1B1SzErUmh4ZXpwMlRTVzBoCjlDQityOHJ4OTlNVEJt%0AUFNoZUJVZkpXVDdQNEFvQnFjT3RlVDQ4S3lNUTNEMHgzZ3JqNzJoODB3VDlXT0tJYzMvb3hWP2Fw%0AcElkPTEma2V5SWQ9MQ%3D%3D; _tid=68003656; sso_puid=84846687; fidsCount=2; _industry=5; uf=b2d2c93beefa90dc45ff49c468aa2f6e9a97e931fce3b272224255f355a068bad0b56241f0c12881b2c105a408201731c49d67c0c30ca5047c5a963e85f11099ba9e882ab47197adce71fc6e59483dd37a48b563e48d11a12a6795f211124b0a32c5bb373fdb1132; _d=1654592676740; vc3=Ov0uLYcZVL66DPvmc93weDKyeEUbr%2BtyMnC5O7k%2FzUlSY%2BVGK9WYNDJXnN57yDmHkiA1oY1djotVYaRbd%2BD77r%2Fn2mGUqgyKiRVng4ijHptDEE%2FyRa39tsHvbLpgILT9GGU5w8XJfplmBjRhJwOlArxtsvyxsHE7jY9Uv6NGQUw%3D26a6b68c5fff2ab0f9ab722e4eccf8cc; DSSTASH_LOG=C_38-UN_190-US_84846687-T_1654592676742; wfwIncode=dk47183; wfwfid=126163; spaceFid=126163; source=num99; wfwEnc=DB4B2D66753282D316834FCE5224C534; JSESSIONID=21C470682FCC4B1AA8D1714BD043AA72.reserve_web_124; route=3b84754f32aaf54a995f7d41f1a28848; oa_uid=84846687; oa_name=%E9%82%93%E6%99%96%E5%BD%AC; oa_deptid=126163; oa_enc=8ab4a296db4957c46b3c88d6e687242b'
        }
        #self.login()

    def login(self):
        c_url = 'https://passport2.chaoxing.com/mlogin?' \
                'loginType=1&' \
                'newversion=true&fid=&' \
                'refer=http%3A%2F%2Foffice.chaoxing.com%2Ffront%2Fthird%2Fapps%2Fseat%2Findex'
        self.session.get(c_url).cookies.get_dict()
        data = {
            'fid': '-1',
            'uname': self.acc,
            'password': base64.b64encode(self.pwd.encode()).decode(),
            'refer': 'http%3A%2F%2Foffice.chaoxing.com%2Ffront%2Fthird%2Fapps%2Fseat%2Findex',
            't': 'true'
        }
        self.session.post('https://passport2.chaoxing.com/fanyalogin', data=data)
        s_url = 'https://office.chaoxing.com/front/third/apps/seat/index'
        self.session.get(s_url)

    def get_token(self):
        response = self.session.get(url=f'https://office.chaoxing.com/front/apps/seat/list')
        self.pageToken = re.compile(r"&pageToken=' \+ '(.*)' \+ '&").findall(response.text)[0]
        response = self.session.get(url='https://office.chaoxing.com/front/apps/seat/select?'
                                        f'id={self.roomid}&'
                                        f'day={self.day}&'
                                        'backLevel=2&'
                                        f'pageToken={self.pageToken}')
        self.token = re.compile("token: '(.*)'").findall(response.text)[0]

    def submit(self, start, end):
        """
        预约方法
        @param start: 开始时间
        @param end: 结束时间
        """
        res = None
        if not self.captcha_is:
            self.get_token()
            res = self.session.get(url='https://office.chaoxing.com/data/apps/seat/submit?'
                                            f'roomId={self.roomid}&'
                                            f'startTime={start}&'  # %3A
                                            f'endTime={end}&'
                                            f'day={self.day}&'
                                            f'seatNum={self.seatnums}&'
                                            f'captcha=0&'
                                            f'token={self.token}')
            try:
                if res.json()['msg'] == '验证失败，请重新验证':
                    self.captcha_is = True
                    self.get_token()
                    while True:
                        self.captcha = self.get_captcha()
                        if self.captcha:
                            break
                    res = self.session.get(url='https://office.chaoxing.com/data/apps/seat/submit?'
                                                    f'roomId={self.roomid}&'
                                                    f'startTime={start}&'  # %3A
                                                    f'endTime={end}&'
                                                    f'day={self.day}&'
                                                    f'seatNum={self.seatnums}&'
                                                    f'captcha={self.captcha}&'
                                                    f'token={self.token}')
            except:
                pass
        else:
            self.get_token()
            while True:
                self.captcha = self.get_captcha()
                if self.captcha:
                    break
            res = self.session.get(url='https://office.chaoxing.com/data/apps/seat/submit?'
                                            f'roomId={self.roomid}&'
                                            f'startTime={start}&'  # %3A
                                            f'endTime={end}&'
                                            f'day={self.day}&'
                                            f'seatNum={self.seatnums}&'
                                            f'captcha={self.captcha}&'
                                            f'token={self.token}')
        print(self.acc, res.json())

    def get_captcha(self):
        """
        处理滑块验证码
        @return: 百分之七十五的准确率预约captcha值
        """
        jq = 'jQuery' + randomNum(16) + '_' + str(time.time() * 1000)[:13]
        t = int(str(time.time() * 1000)[:13])
        res = self.session.get('https://captcha.chaoxing.com/captcha/get/verification/image?'
                               f'callback=jQuery{randomNum(16)}_{str(time.time() * 1000)[:13]}&'
                               'captchaId=42sxgHoTPTKbt0uZxPJ7ssOvtXr3ZgZ1&type=slide&version=1.1.6'
                               f'&_={str(t)}').text
        result = res.split('(')[1].split(')')[0]
        res = json.loads(result)
        token_captcha = res['token']
        shadeImage = res['imageVerificationVo']['shadeImage']  # 'data:image/png;base64,' +
        cutoutImage = res['imageVerificationVo']['cutoutImage']
        textClickArr = captchaCv.main(base64.b64decode(cutoutImage), base64.b64decode(shadeImage))[1]
        textClickArr = '[{"x":' + str(textClickArr) + '}]'
        params = (
            ('callback', jq),
            ('captchaId', '42sxgHoTPTKbt0uZxPJ7ssOvtXr3ZgZ1'),
            ('type', 'slide'),
            ('token', token_captcha),
            ('textClickArr', textClickArr),
            ('coordinate',
             '[]'),
            ('runEnv', '10'),
            ('version', '1.1.6'),
            ('_', str(t + 1)),
        )
        res = self.session.get(url='https://captcha.chaoxing.com/captcha/check/verification/result', params=params).text
        res = res.split('(')[1].split(')')[0]
        res = json.loads(res)
        if res["result"]:
            return json.loads(res['extraData'])["validate"]
        return False


def diy_book(starttime, endtime):
    """
    取时间段按两小时切片
    @param starttime: 开始时间
    @param endtime: 结束时间
    @return: 时间列表
    """
    start_h, start_m = starttime.split(':', 1)
    end_h, end_m = endtime.split(':', 1)
    ls_time = []
    start = int(start_h)
    for c in range(int(end_h) - int(start_h)  + 1):
        if (int(end_h) - start) <= 2:
            if (int(end_h) - start) == 2 and start_m == end_m:
                ls_time.append([str(start) + ':' + start_m, str(int(start) + 2) + ':' + start_m])
                break
            if (int(end_h) - start) == 2 and start_m == '30':
                ls_time.append([str(start) + ':' + start_m, str(int(start) + 2) + ':' + end_m])
                break
            if (int(end_h) - start) == 2 and start_m == '00':
                ls_time.append([str(start) + ':' + start_m, str(int(start) + 2) + ':' + start_m])
                start += 2
                continue
            if (int(end_h) - start) == 1:
                ls_time.append([str(start) + ':' + start_m, str(int(start) + 1) + ':' + end_m])
                break
            if int(end_h) == start and start_m == '00':
                ls_time.append([str(start) + ':' + start_m, str(int(start)) + ':' + end_m])
                break
            break
        ls_time.append([str(start) + ':' + start_m, str(int(start) + 2) + ':' + start_m])
        start += 2
    return ls_time


def submit_sub(seatnums, roomid, start, end, acc, pwd):
    """
    预约子方法
    @param seatnums: 座位号
    @param roomid: 房间号
    @param start: 开始时间
    @param end: 结束时间
    @param acc: 账号
    @param pwd: 密码
    """
    sub = CX(acc, pwd, roomid=roomid, seatnums=seatnums)
    for index_a in diy_book(start, end):
        sub.submit(start=index_a[0], end=index_a[1])


def book_seat(list_form):
    """
    多账号多线程预约支持
    @param list_form: 座位号 房间号 开始时间 结束时间 手机号 密码
    """
    ths = []
    for index1 in list_form:
        ths.append(
            threading.Thread(target=submit_sub,
                             args=(index1[0], index1[1], index1[2], index1[3], index1[4], index1[5],))
        )
    for th in ths:
        # print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), 'start_thread')
        th.start()
    for th in ths:
        th.join()


def randomNum(num):
    """
    产生num+4位的随机数
    @param num: 数量
    @return: nums+4位的随机数
    """
    l_nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    nums = '3310'
    for index in range(num):
        nums += str(random.choice(l_nums))
    return nums


if __name__ == '__main__':
    a = time.time()
    lis = [
        ['081', '6101', '9:00', '21:00', '1********', '****']  # 座位号 房间号 开始时间 结束时间 手机号 密码
    ]
    book_seat(lis)  # 立刻预约
    print(time.time() - a)
