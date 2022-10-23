from urllib import response
from flask import Flask,jsonify,request
import requests
import json
from io import StringIO
from html.parser import HTMLParser
from werkzeug.serving import WSGIRequestHandler
WSGIRequestHandler.protocol_version = "HTTP/1.1"

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import re
import numpy as np
from pykospacing import Spacing
import pickle5 as pickle

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"




app = Flask(__name__)

# ai모델 읽기
model = tf.keras.models.load_model('sms_model.h5')
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
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

    print(model)

    new_sentence = content

     # URL 제거
    new_sentence = re.sub(r"(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])","",new_sentence)
    new_sentence = re.sub(r'/(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})/gi','',new_sentence)
    
    # web발신 제거
    new_sentence = new_sentence.replace('[Web발신]','')

    # 개행문자 제거
    new_sentence = new_sentence.replace('\n','')
    
    # 한글만 처리
    new_sentence  = re.sub(r"[^ㄱ-ㅣ가-힣\s]", "", new_sentence)

    spacing = Spacing()
    new_sentence = spacing(new_sentence)

    app.logger.info("전처리 완료된 문자 >>"+new_sentence)

    encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
    pad_new = pad_sequences(encoded, maxlen = 273) # 패딩
    score = float(model.predict(pad_new))*100 # 예측

    app.logger.info(score)

    app.logger.info("모델 예측 결과 >>"+str((content)))

    copResult = check_cop(number=number)

    result={"isSuccess":True,"copResult":copResult,"aiResult":round(score,2)}

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