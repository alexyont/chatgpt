import requests
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import logging

_MODEL = "gpt-3.5-turbo"
_API_KEY = "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"

app = Flask(__name__, template_folder='templates')
CORS(app)

dev_logger: logging.Logger = logging.getLogger(name='dev')
dev_logger.setLevel(logging.INFO)

handler: logging.StreamHandler = logging.StreamHandler()
dev_logger.addHandler(handler)

def get_reply(inputStr):
    dev_logger.info("get_reply:"+inputStr) 
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions",
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + _API_KEY
            },
            json = {
                "model":_MODEL,
                "messages":[{"role":"user","content":inputStr}]
            }
        )

        responseDict = response.json()
        dev_logger.info(responseDict)
        reply = ""
        #id=responseDict["id"]
        for message in responseDict["choices"]:
            reply += message["message"]["content"]
            #put_excel(id, inputStr,message["message"]["content"])
    except requests.exceptions.HTTPError as errh:
        dev_logger.error("HTTP Error") 
        dev_logger.error(errh.args[0])  
        reply = "HTTP Error 發生錯誤"
    except Exception as err: 
        dev_logger.error(err)   
        reply = "ERR:"+str(err)

    return reply

@app.route('/reply', methods=['POST'])
def reply():
    try:
        # 從 POST 請求中取得傳遞的 JSON 資料
        data = request.json

        # 檢查是否有 'input_string' 這個 key
        if 'input_string' in data:
            input_string = data['input_string']
            reply = get_reply(input_string)
            return jsonify({'result': reply})
        else:
            return jsonify({'error': 'Missing input_string parameter'}), 400

    except: 
        print("錯誤")
        reply = jsonify({'error': 'Missing input_string parameter'}), 400

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)