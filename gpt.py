import requests
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

#_MODEL = "gpt-3.5-turbo"
_MODEL = "ft:gpt-3.5-turbo-0613:personal::8MBzgoJJ"
_API_KEY = "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"

app = Flask(__name__, template_folder='templates')
CORS(app)

def put_excel(id, question, answer):
    url = 'https://script.google.com/macros/s/AKfycby2ttK4bJWPWtz6B_re4yzu_gt93VZS1ynHjae_Bq_M8oRqd1r0h0nZM9qZ9kd6e8PMRA/exec'

    params = {
        'name':'工作表1',
        'data':'["'+id+'","'+question+'","'+answer.replace("\n", " ").replace("'", " ").replace('"', ' ')+'","'+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'"]'
    }

    web = requests.get(url=url, params=params)

    return web

def put_training_data():
    try:
        file_path = 'traning_data.txt'  
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        response = requests.post("https://api.openai.com/v1/chat/completions",
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + _API_KEY
            },
            json = {
                "model":_MODEL,
                "messages":[{"role":"system","content":file_content}]
            }
        )

        responseDict = response.json()
        print(responseDict)
    except: 
        print("發生錯誤")

    return reply

def get_reply(inputStr):
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
        print(responseDict)
        reply = ""
        id=responseDict["id"]
        for message in responseDict["choices"]:
            reply += message["message"]["content"]
            put_excel(id, inputStr,message["message"]["content"])
    except: 
        reply = "發生錯誤"

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
    put_training_data()
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)