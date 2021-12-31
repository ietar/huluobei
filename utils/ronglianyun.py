# -*- coding: utf-8 -*-
import requests
import hashlib
import time
import base64
import json

from ronglian_sms_sdk import SmsSDK

Settings = {
    'base_url': 'https://app.cloopen.com:8883',
    'account_sid': '8a216da86ab0b4d2016ac006273b0db5',
    'auth_token': 'af911dc1ac5e45cd82116965af250473',
    'app_id': '8a216da86ab0b4d2016ac006278c0dbb',
}


class SmsSdk:
    """
    容联云发送短信类 sdk
    """
    def __init__(self, setting: dict):
        self.account_sid = setting.get('account_sid')
        self.auth_token = setting.get('auth_token')
        self.app_id = setting.get('app_id')

        self.instance = SmsSDK(accId=self.account_sid,
                               accToken=self.auth_token,
                               appId=self.app_id)

    def send_msg(self, code, expire_minute):
        a = self.instance.sendMessage(tid='1', mobile='15901016143', datas=(code, expire_minute))
        return a


class Sms:
    """
    容联云发送短信类 自制
    """
    def __init__(self, setting: dict):
        self.base_url = setting.get('base_url')
        self.account_sid = setting.get('account_sid')
        self.auth_token = setting.get('auth_token')
        self.app_id = setting.get('app_id')

    def send_msg(self, to: str, template_id: int, datas=None, data=None, sub_append=None, req_id=None) -> dict:
        """

        :param to: String	必选	短信接收端手机号码集合，用英文逗号分开，每批发送的手机号数量不得超过200个
        :param template_id: String	必选	模板Id，官网控制台模板列表获取。测试模板id是1。测试模板的内容是：【云通讯】您使用的是云通讯短信模板，您的验证码是{1}，请于{2}分钟内正确输入
        :param datas: Array	可选	内容数据外层数组节点
        :param data: String 可选 内容数据，用于替换模板中{序号}，模板如果没有变量，此参数可不传，多个变量，使用数组的数据格式
        :param sub_append: String	可选	扩展码，四位数字 0~9999
        :param req_id: String	可选	第三方自定义消息id，最大支持32位，同账号下同一自然天内不允许重复。
        :return:{'statusCode': '000000', 'templateSMS': {'smsMessageSid': '9538240018844833a22beb19c5aeb701', 'dateCreated': '20211112165259'}}
        """
        sms_url = f'/2013-12-26/Accounts/{self.account_sid}/SMS/TemplateSMS'
        ts = time.strftime('%Y%m%d%H%M%S', time.localtime())
        sign_str = self.account_sid + self.auth_token + ts
        sign = hashlib.md5(sign_str.encode()).hexdigest().upper()
        auth = base64.b64encode(f'{self.account_sid}:{ts}'.encode())
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'charset': 'utf-8',
            'Authorization': auth,
        }
        params = {
            'sig': sign
        }
        post_data = {
            'to': to,
            'appId': self.app_id,
            'templateId': str(template_id),
        }
        if datas:
            post_data['datas'] = datas
        if data:
            post_data['data'] = data
        if sub_append:
            post_data['subAppend'] = sub_append
        if req_id:
            post_data['reqId'] = req_id

        r = requests.post(url=self.base_url+sms_url, headers=headers, params=params, data=json.dumps(post_data))
        return r.json()

    def send_msg1(self, to: str, code: str, expire_minute: int) -> dict:
        """

        :param to: str 必选	短信接收端手机号码集合，用英文逗号分开，每批发送的手机号数量不得超过200个
        :param code: str 必选 发送的验证码
        :param expire_minute: int 必选 验证码过期时间(分钟)
        :return:{'statusCode': '000000', 'templateSMS': {'smsMessageSid': '9538240018844833a22beb19c5aeb701', 'dateCreated': '20211112165259'}}
        """
        return self.send_msg(to=to, template_id=1, datas=[code, expire_minute])


sms = Sms(setting=Settings)


if __name__ == '__main__':

    print(sms.send_msg1(to='15901016143', code='nop', expire_minute=3))

    # sms2 = SmsSdk(Settings)
    # print(sms2.send_msg(code='kksk', expire_minute=3))






