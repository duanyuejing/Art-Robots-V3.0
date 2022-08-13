import streamlit as st
import pandas as pd
import requests
import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tts.v20190823 import tts_client, models
import base64
import uuid
import api

# st.markdown(
#     f"""
#     <style>
#     .stApp {{
#     background-image: url('http://pic.bizhi360.com/bpic/84/10584.jpg');
#     background-size: cover
#     }}
#     </style>
#     """,
#     unsafe_allow_html=True)


st.title('语音文学机器人')

# 定义的可选数据
df1 = pd.DataFrame({
    'person_name': ['智逍遥', '智瑜', '智聆', '智美', '智云', '智莉',
                    '智言', '智娜', '智琪', '智芸', '智华', '智燕',
                    '智丹', '智辉', '智宁', '智萌', '智甜', '智蓉',
                    '智靖', '智彤', '智刚', '智瑞', '智虹', '智萱',
                    '智皓', '智薇', '智希', '智梅', '智洁', '智凯',
                    '智柯', '智奎', '智芳', '智蓓', '智莲', '智依',
                    '智川']})

person_jieshi = {'智逍遥': '阅读男声', '智瑜': '情感女声', '智聆': '通用女声',
                 '智美': '客服女声', '智云': '通用男声', '智莉': '通用女声',
                 '智言': '助手女声', '智娜': '客服女声', '智琪': '客服女声',
                 '智芸': '知性女声', '智华': '通用男声', '智燕': '新闻女声',
                 '智丹': '新闻女声', '智辉': '新闻男声', '智宁': '新闻男声',
                 '智萌': '男童声', '智甜': '女童声', '智蓉': '情感女声',
                 '智靖': '情感男声', '智彤': '粤语女声', '智刚': '新闻男声',
                 '智瑞': '新闻男声', '智虹': '新闻女声', '智萱': '聊天女声',
                 '智皓': '聊天男声', '智薇': '聊天女声', '智希': '通用女声',
                 '智梅': '通用女声', '智洁': '通用女声', '智凯': '通用男声',
                 '智柯': '通用男声', '智奎': '通用男声', '智芳': '通用女声',
                 '智蓓': '客服女声', '智莲': '通用女声', '智依': '通用女声',
                 '智川': '四川女声'}

preson_set_property = {'智逍遥': '100510000', '智瑜': '101001', '智聆': '101002',
                       '智美': '101003', '智云': '101004', '智莉': '101005', '智言': '101006',
                       '智娜': '101007', '智琪': '101008', '智芸': '101009', '智华': '101010',
                       '智燕': '101011', '智丹': '101012', '智辉': '101013', '智宁': '101014',
                       '智萌': '101015', '智甜': '101016', '智蓉': '101017', '智靖': '101018',
                       '智彤': '101019', '智刚': '101020', '智瑞': '101021', '智虹': '101022',
                       '智萱': '101023', '智皓': '101024', '智薇': '101025', '智希': '101026',
                       '智梅': '101027', '智洁': '101028', '智凯': '101029', '智柯': '101030',
                       '智奎': '101031', '智芳': '101032', '智蓓': '101033', '智莲': '101034',
                       '智依': '101035', '智川': '101040'}



# 选择要生成的类型
style_n = 0
style = st.radio("请选择您想要的类型", ('诗', '词', '对联'))
if style == '诗':
    style_n = 1
elif style == '词':
    style_n = 2
else:
    style_n = 3


# 一个api写两个函数，一个是请求一个是调用


def cipost(word):
    url = "http://119.3.249.76:8080/gen/ci"
    parm = {"text": word}
    res = requests.post(url, json.dumps(parm))
    # return res.text
    if json.loads(res.text)['code'] == 200:
        return json.loads(res.text)['result']
    else:
        return '出错'


def shipost(word):
    parm = {"text": word}
    couplet_url = "http://119.3.249.76:8080/gen/poem"
    couplet_res = requests.post(couplet_url, json.dumps(parm))
    # return couplet_res.text
    if json.loads(couplet_res.text)['code'] == 200:
        return json.loads(couplet_res.text)['result']
    else:
        return '出错'


def duilianpost(word):
    parm = {"text": word}
    couplet_url = "http://119.3.249.76:8080/gen/couplet"
    couplet_res = requests.post(couplet_url, json.dumps(parm))
    # return couplet_res.text
    if json.loads(couplet_res.text)['code'] == 200:
        # for i in json.loads(couplet_res.text)['result']:
        #     s = s.join(i)
        s = json.loads(couplet_res.text)['result'][0] + ',' + json.loads(couplet_res.text)['result'][1]
        return s
    else:
        return '出错'


title = st.text_input('请输入开头————例如：春')
if st.button('生成文本'):
    with open('word.txt', 'w') as f:
        if style_n == 1:
            # print(shipost(title))
            f.write(shipost(title))
        elif style_n == 2:
            # print(cipost(title))
            f.write(cipost(title))
        elif style_n == 3:
            # print(duilianpost(title))
            f.write(duilianpost(title))
        f.close()
with open('word.txt', 'r') as f:
    st.write(f.read())
    f.close()


with open('word.txt', 'r') as f:
    s = f.read()
    st.write()
    f.close()
option = st.selectbox(
    '请选择使用的人物音色：',
    df1['person_name'])
jieshi = person_jieshi[option]
st.write('您选的人物特点: ', jieshi)
preaon_property = preson_set_property[option]


# 生成语音的SDK


if st.button('生成语音'):
    with open('word.txt', 'r') as f:
        s = f.read()
    api.tencent_cloud_com(preaon_property,s)
    audio_file = open('E:testten.mp3', 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg')

