import os
import openai
import flask
from flask import Flask, request, jsonify

# Print versions of the libraries
print(f"OpenAI version: {openai.__version__}")
print(f"Flask version: {flask.__version__}")

app = Flask(__name__)

# Set the OpenAI API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Make sure OPENAI_API_KEY environment variable is set.")
openai.api_key = api_key

# Define the function to generate posts
def generate_post(topic):
    prompt_post = f"Напишите подробный пост для блога на тему: {topic}."
    response_post = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt_post}],
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )
    post_content = response_post.choices[0].message["content"].strip()
    return post_content

# Define the extended function to generate posts with titles and meta descriptions
def generate_post_extended(topic):
    prompt_title = f"Придумайте привлекательный заголовок для поста на тему: {topic}."
    prompt_meta = f"Создайте мета-описание для поста на тему: {topic}."
    prompt_post = f"Напишите подробный и увлекательный пост для блога на тему {topic}, используя при этом короткие абзацы, подзаголовки, примеры и ключевые слова для лучшего восприятия и SEO-оптимизации."

    # Generate the title
    response_title = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt_title}],
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    title = response_title.choices[0].message["content"].strip()

    # Generate the meta description
    response_meta = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt_meta}],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    meta_description = response_meta.choices[0].message["content"].strip()

    # Generate the post
    response_post = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt_post}],
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.7,
    )
    post_content = response_post.choices[0].message["content"].strip()

    # Return the result
    return {
        "title": title,
        "meta_description": meta_description,
        "post_content": post_content,
    }

@app.route('/generate_post', methods=['GET'])
def generate_post_endpoint():
    topic = request.args.get('topic')
    if topic:
        try:
            post = generate_post_extended(topic)
            return jsonify(post)
        except Exception as e:
            return jsonify({"error": f"Failed to generate post: {str(e)}"}), 500
    else:
        return jsonify({"error": "No topic provided"}), 400

# This line is no longer needed:
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8000)))



