import json
import requests
import datetime
from flask import Flask, request

app = Flask(__name__)

global_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.41',
}


def get_error(error_type, error_code, error_info, receive_id):
    payload_template = {"header": {"template": "red", "title": {"tag": "plain_text", "content": "[MCSManager Bot] {ErrorType}"}}, "elements": [{"tag": "markdown", "content": "**获取失败，请稍后再试。**\n\n错误代码：\n{ErrorCode}\n\n详细信息：\n{ErrorInfo}"}, {"tag": "hr"}, {"tag": "markdown", "content": "<font color='grey'>{NowTime} # MCSManager Bot by [CJYKK](https://CJYKK.top/)</font>", "text_align": "right"}]}
    payload_template["header"]["title"]["content"] = payload_template["header"]["title"]["content"].format(ErrorType=error_type)
    payload_template["elements"][0]["content"] = payload_template["elements"][0]["content"].format(ErrorCode=error_code, ErrorInfo=error_info)
    payload_template["elements"][2]["content"] = payload_template["elements"][2]["content"].format(NowTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    payload = json.dumps({
        "content": json.dumps(payload_template),
        "msg_type": "interactive",
        "receive_id": receive_id
    })
    headers = {
        'Authorization': 'Bearer t-g1046bf7GXY7UU2PTQ5BSL2GPCUANT3LFQWGD47P',
        'Content-Type': 'application/json'
    }
    requests.request("POST", "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id", headers=headers, data=payload)


def mcsm_command_status():
    try:
        req_row = requests.get("http://admin.wsmcs.tusitu123.top:21931/api/service/remote_services_system?apikey=4b07d82ca6384cc9ad0bf756d3067824", headers=global_headers)
        if req_row.status_code != 200:
            get_error("查询错误", req_row.status_code, req_row.reason, "ou_984415ee05d467b2cc7aaf0ee8225df6")
    except requests.ConnectionError as error:
        get_error("连接错误", "[无]", error, "ou_984415ee05d467b2cc7aaf0ee8225df6")
    except BaseException as error:
        get_error("未知错误", "[无]", error, "ou_984415ee05d467b2cc7aaf0ee8225df6")


def decide_mcsm_command(command):
    if command == "status":
        mcsm_command_status()


@app.route('/feishu', methods=['POST'])
def feishu():
    try:
        request_json = request.get_json()
        event_type = request_json['header']['event_type']
        if event_type == 'im.message.receive_v1':
            message_content = json.loads(
                request_json['event']['message']['content'])
            text = message_content.get('text')

            if text.startswith("/mcsm "):
                print(f'Running command: {text[6::]}')
                decide_mcsm_command(text[6::])
            else:
                print(f"Message: {text}")
    except (KeyError, json.JSONDecodeError, BaseException) as e:
        print(f"Error: {e}")

    return ""


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=55998)
