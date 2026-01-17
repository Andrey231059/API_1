from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    news = None
    joke = None

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'news':
            news = get_news()
        elif action == 'joke':
            joke = get_random_joke()

    return render_template("index.html", news=news, joke=joke)


def get_news():
    api_key = "7cf5f77d04544b0fb44c72dfb788fc47"
    url = f"https://newsapi.org/v2/everything?q=новости&language=ru&sortBy=publishedAt&apiKey={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        return data.get('articles', [])
    except:
        return []



# def get_random_joke():
#     try:
#         response = requests.get("https://v2.jokeapi.dev/joke/Any?lang=en&type=single")
#         if response.status_code == 200:
#             data = response.json()
#             if data.get('type') == 'single':
#                 return data['joke']
#             else:
#                 # На случай, если вернётся двухчастная шутка (редко при type=single)
#                 return f"{data['setup']} — {data['delivery']}"
#     except Exception as e:
#         print("Ошибка при получении шутки:", e)
#     return None

def get_random_joke():
    try:
        # 1. Получаем шутку на английском
        joke_resp = requests.get(
            "https://v2.jokeapi.dev/joke/Any?lang=en&type=single",
            timeout=5
        )
        if joke_resp.status_code != 200:
            return {"en": "No joke available.", "ru": "Шутка недоступна."}

        data = joke_resp.json()
        if data.get("error"):
            return {"en": "Joke API returned an error.", "ru": "Ошибка сервиса шуток."}

        english_joke = data.get("joke", "Why don't scientists trust atoms? Because they make up everything!")

        # 2. Переводим на русский через LibreTranslate
        try:
            translate_resp = requests.post(
                "https://libretranslate.com/translate",
                json={
                    "q": english_joke,
                    "source": "en",
                    "target": "ru",
                    "format": "text"
                },
                headers={"Content-Type": "application/json"},
                timeout=5
            )

            if translate_resp.status_code == 200:
                translated = translate_resp.json().get("translatedText", "")
                if translated.strip():  # если перевод не пустой
                    russian_joke = translated
                else:
                    russian_joke = "Не удалось перевести (пустой ответ)."
            else:
                russian_joke = f"Ошибка сервера перевода ({translate_resp.status_code})"
        except Exception as e:
            russian_joke = f"Перевод невозможен: {str(e)}"

        return {"en": english_joke, "ru": russian_joke}

    except Exception as e:
        print("Ошибка при получении или переводе шутки:", e)
        return {
            "en": "Failed to fetch joke.",
            "ru": "Не удалось получить шутку."
        }


if __name__ == '__main__':
    app.run(debug=True)
