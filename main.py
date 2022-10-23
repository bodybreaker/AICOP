from urllib import response
from flask import Flask,jsonify,request
import requests
import json
from io import StringIO
from html.parser import HTMLParser
from werkzeug.serving import WSGIRequestHandler
WSGIRequestHandler.protocol_version = "HTTP/1.1"

import os
import tensorflow as tf
from tensorflow import keras



app = Flask(__name__)



# ai모델 읽기
new_model = tf.keras.models.load_model('sms_model.h5')
# 모델 구조를 출력합니다
# app.logger.info("모델 로드 완료")



#경찰청 사기의심 전화*계좌번호 조회
URL_COP="https://net-durumi.cyber.go.kr/countFraud.do?fieldType=H&accessType=3&_=1662989169142&keyword="

@app.route("/")
def health_check():
    return "alive"

@app.post("/sms")
def receive_sms():
    number = request.form["number"]
    content = request.form["content"]

    app.logger.info("got sms")

    app.logger.info("[수신번호] >> "+number)
    app.logger.info("[문자내용] >> "+content)

    copResult = check_cop(number=number)

    result={"isSuccess":True,"copResult":copResult}

    return jsonify(result)

# 경찰청 사이버수사대 체크
def check_cop(number):
    app.logger.info("경찰청 사이버수사대 체크 >> "+number)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'Host':'net-durumi.cyber.go.kr',
        'Referer':'https://cyberbureau.police.go.kr/'
    }
    response = requests.get(URL_COP+number,headers=headers)
    app.logger.info("응답코드 >> "+str(response.status_code))

    resText = response.text
    resText = resText.replace("data(","")
    resText = resText.replace(")","")
    resText = json.loads(resText)
    app.logger.info("응답전문 >> "+str(resText))

    s = MLStripper()
    s.feed(resText['message'])
    return s.get_data()

# HTML 제거 클래스
class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()  


if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True,port=6789)