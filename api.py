from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tts.v20190823 import tts_client, models
import base64
import json
import uuid


def tencent_cloud_com(voicetype,voicetext):
    try:
        cred = credential.Credential("xxxxxx", "xxxxxx")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "tts.tencentcloudapi.com"
        voicetype = voicetype # 播音声音类型
        voicetext = voicetext
        # if voicetype == '':
        #     print('你选择的声音类型是空，默认将设置为0')
        #     voicetype = '0'
        # else:
        #     print('你选的声音类型是：', voicetype)

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tts_client.TtsClient(cred, "ap-beijing", clientProfile)
        uuid_str = uuid.uuid1()
        # print(uuid_str)

        req = models.TextToVoiceRequest()
        params = '{"Text":"' + voicetext + '","SessionId":"' + str(
            uuid_str) + '","ModelType":1,"VoiceType":' + voicetype + '}'
        req.from_json_string(params)

        resp = client.TextToVoice(req)
        jsonres = resp.to_json_string()
        # print(type(resp.to_json_string()))

        strss = json.loads(jsonres)
        voice_base64 = strss['Audio']
        file_name = 'E:testten.mp3'

        # print('保存路径为：', file_name)
        resultdata = base64.b64decode(voice_base64)  # 转换成base64编码
        file = open(file_name, "wb")  # 保存为mp3文件
        file.write(resultdata)
        file.close()

    except TencentCloudSDKException as err:
        print(err)
