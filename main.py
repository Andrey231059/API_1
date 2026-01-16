#импортируем Flask и библиотеку Request
from flask import Flask, render_template, request
import requests

#импортируем объект класса Flask
app = Flask(__name__)

#формируем путь и методы GET и POST
@app.route('/', methods=['GET', 'POST'])
#создаем функцию с переменной weather, где мы будем сохранять погоду
def index():
   weather = None
   if request.method == 'POST':
       city = request.form['city']
       #прописываем переменную, куда будет сохраняться результат и функцию weather с указанием города, который берем из формы
       weather = get_weather(city)
       #передаем информацию о погоде в index.html
   return render_template("index.html", weather=weather)

#в функции прописываем город, который мы будем вводить в форме
def get_weather(city):
   api_key = "ваш_ключ"
   #адрес, по которомы мы будем отправлять запрос. Не забываем указывать f строку.
   url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
   #для получения результата нам понадобится модуль requests
   response = requests.get(url)
   #прописываем формат возврата результата
   return response.json()

if __name__ == '__main__':
   app.run(debug=True)