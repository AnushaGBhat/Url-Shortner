from flask import Flask, request, jsonify, redirect
import string, random, datetime

app = Flask(__name__)

url_store = {}
clicks = {}

@app.route("/api/health")
def health():
    return jsonify({"status": "ok"}), 200

def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route("/api/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    short_code = generate_short_code()
    while short_code in url_store:
        short_code = generate_short_code()

    url_store[short_code] = {
        "original_url": url,
        "created_at": datetime.datetime.utcnow(),
    }
    clicks[short_code] = 0

    return jsonify({
        "short_code": short_code,
        "short_url": request.host_url + short_code
    })

@app.route("/<short_code>")
def redirect_url(short_code):
    if short_code not in url_store:
        return jsonify({"error": "Not found"}), 404

    clicks[short_code] += 1
    return redirect(url_store[short_code]["original_url"])

@app.route("/api/stats/<short_code>")
def stats(short_code):
    if short_code not in url_store:
        return jsonify({"error": "Not found"}), 404

    return jsonify({
        "url": url_store[short_code]["original_url"],
        "clicks": clicks[short_code],
        "created_at": url_store[short_code]["created_at"].isoformat()
    })
