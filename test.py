import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import re
import numpy as np
from pykospacing import Spacing

model = tf.keras.models.load_model('sms_model (1).h5')
print(model)
tokenizer = Tokenizer()

new_sentence = "안녕하세요 씨발 계속 바뀌네"

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

print("전처리 완료된 문자 >>"+new_sentence)

encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
pad_new = pad_sequences(encoded, maxlen = 268) # 패딩
score = float(model.predict(pad_new))*100 # 예측

print(score)