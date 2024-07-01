import os
import openai
from flask import Flask, request, jsonify

# Печать версий библиотек
print(f"OpenAI version: {openai.__version__}")
print(f"Flask version: {Flask.__version__}")

app = Flask(__name__)

# Установка API-ключа OpenAI из переменной окружения
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Make sure OPENAI_API_KEY environment variable is set.")
openai.api_key = api_key

# Определение функции генерации постов
def generate_post(topic):
    prompt_post = f"Напишите подробный пост для блога на тему: {topic}."
    response_post = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt_post}],
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )
    post_content = response_post.choices[0].message["content"].strip()
    return post_content

# Переопределение функции генерации постов с заголовками и мета-описаниями
def generate_post_extended(topic):
    prompt_title = f"Придумайте привлекательный заголовок для поста на тему: {topic}."
    prompt_meta = f"Создайте мета-описание для поста на тему: {topic}."
    prompt_post = f"Напишите подробный и увлекательный пост для блога на тему {topic}, используя при этом короткие абзацы, подзаголовки, примеры и ключевые слова для лучшего восприятия и SEO-оптимизации."

    # Генерация заголовка
    response_title = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt_title}],
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    title = response_title.choices[0].message["content"].strip()

    # Генерация мета-описания
    response_meta = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt_meta}],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    meta_description = response_meta.choices[0].message["content"].strip()

    # Генерация поста
    response_post = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt_post}],
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.7,
    )
    post_content = response_post.choices[0].message["content"].strip()

    # Возврат результата
    return {
        "title": title,
        "meta_description": meta_description,
        "post_content": post_content,
    }

@app.route('/generate_post', methods=['GET'])
def generate_post_endpoint():
    topic = request.args.get('topic')
    if topic:
        post = generate_post_extended(topic)
        return jsonify(post)
    else:
        return jsonify({"error": "No topic provided"}), 400

# Эта строка больше не нужна:
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8000)))



