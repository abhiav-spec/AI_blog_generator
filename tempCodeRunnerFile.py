from flask import Flask, render_template, request, jsonify
import requests
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Load API Keys from environment
HF_API_KEY = os.getenv("HF_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

# Check if keys are loaded (optional debug)
if not HF_API_KEY or not PEXELS_API_KEY:
    raise ValueError("API keys are missing. Check your .env file.")

# API URLs and headers
HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
HF_HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}
PEXELS_HEADERS = {"Authorization": PEXELS_API_KEY}


def query_huggingface(prompt):
    try:
        response = requests.post(HF_API_URL, headers=HF_HEADERS, json={"inputs": prompt})
        if response.status_code != 200:
            return f"API Error: {response.status_code} - {response.text}"
        data = response.json()
        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]
        elif isinstance(data, dict) and "generated_text" in data:
            return data["generated_text"]
        elif "error" in data:
            return f"API Error: {data['error']}"
        else:
            return "Error: Unexpected API response format."
    except Exception as e:
        return f"Exception: {str(e)}"


def fetch_image_url(query):
    try:
        res = requests.get(
            f"https://api.pexels.com/v1/search?query={query}&per_page=1",
            headers=PEXELS_HEADERS
        )
        if res.status_code == 200:
            data = res.json()
            if data['photos']:
                return data['photos'][0]['src']['large']
    except Exception as e:
        print("Image Fetch Error:", e)
    return "https://via.placeholder.com/800x400.png?text=Image+Not+Found"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt', 'tiger')
    blog = query_huggingface(f"Write a detailed blog post about: {prompt}")
    image_url = fetch_image_url(prompt)
    return jsonify({'blog': blog, 'image_url': image_url})


if __name__ == '__main__':
    app.run(debug=True)
