from django.shortcuts import render
import json
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

import keras
# from tensorflow import keras
from keras.preprocessing.sequence import pad_sequences
import pickle

# Загрузка конфигурационного файла
config = json.load(open('newral/config.json'))

# Общие данные по двум категориям сетей
max_len = config['max_len']
with open(config['tokenizer'], 'rb') as handle:
    tokenizer = pickle.load(handle)

# Данные по сети с категориальным обучением
model_categorical = keras.models.load_model(config['model_categorical'])
model_categorical_save_path = config['model_categorical_save_path']
model_categorical.load_weights(model_categorical_save_path)

# Данные по сети с бинарным обучением
model_binary = keras.models.load_model(config['model_binary'])
model_binary_save_path = config['model_binary_save_path']
model_binary.load_weights(model_binary_save_path)



class ReviewView(APIView):
    def get(self, request):
        return render(request, 'app/index.html')

    def post(self, request):
        text = request.data['data']
        sequence = tokenizer.texts_to_sequences([text])
        data = pad_sequences(sequence, maxlen=max_len)
        
        result_categorical = list(model_categorical.predict(data)[0])
        grade_result_categorical = result_categorical.index(max(result_categorical)) + 1
        
        result_binary = list(model_binary.predict(data)[0])
        grade_result_binary = round(10 * result_binary[0])
        
        return Response({
            "Grade_categorical": grade_result_categorical,
            "Tonality_categorical": "Negative"\
                 if result_categorical.index(max(result_categorical)) < 5\
                      else "Positive",
            
            "Grade_binary": 1 if grade_result_binary < 1 else grade_result_binary,
            "Tonality_binary": "Negative"\
                 if result_binary[0] < 0.5\
                      else "Positive"
            })