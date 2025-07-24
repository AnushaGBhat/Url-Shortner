from flask import Flask, request, jsonify, send_from_directory, redirect
import random
import string

app = Flask(__name__, static_folder='static')

url_store = {}

class ShortURL:
    def __init__(self, original_url, short_code):
        self.original_url = original_url
        self.short_code = short_code

@app.route("/")
def home():
    return send_from_directory('static', 'index.html')

@app.route("/shorten", methods=["POST"])
def shorten():
    data = request.get_json()
    original_url = data.get("url")

    if not original_url:
        return jsonify({"error": "URL is required"}), 400

    short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    url_store[short_code] = ShortURL(original_url, short_code)

    return jsonify({"short_url": request.host_url + short_code})

@app.route("/<short_code>")
def redirect_to_url(short_code):
    url_data = url_store.get(short_code)
    if url_data:
        return redirect(url_data.original_url)  # ✅ HTTP 302
    return "URL not found", 404

if __name__ == "__main__":
    app.run(debug=True)
