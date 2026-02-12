from flask import Flask, render_template, request, jsonify
import math
import re

app = Flask(__name__)

GUESSES_PER_SECOND = 10_000_000_000

@app.route("/")
def home():
    return render_template("index.html")


def calculate_charset(password):
    charset = 0
    if re.search(r"[a-z]", password):
        charset += 26
    if re.search(r"[A-Z]", password):
        charset += 26
    if re.search(r"[0-9]", password):
        charset += 10
    if re.search(r"[^a-zA-Z0-9]", password):
        charset += 32
    return charset

def format_time(seconds):
    units = [
        ("years", 60*60*24*365),
        ("days", 60*60*24),
        ("hours", 60*60),
        ("minutes", 60),
        ("seconds", 1)
    ]
    for name, unit in units:
        if seconds >= unit:
            return f"{seconds / unit:.2f} {name}"
    return "instantly"

@app.route("/check", methods=["POST"])
def check_password():
    password = request.json.get("password", "")
    length = len(password)

    if length == 0:
        return jsonify({"error": "Empty password"})

    charset = calculate_charset(password)
    combinations = charset ** length
    avg_time = combinations / (2 * GUESSES_PER_SECOND)

    entropy = math.log2(combinations)

    if entropy < 40:
        strength = "Very Weak"
    elif entropy < 60:
        strength = "Weak"
    elif entropy < 80:
        strength = "Moderate"
    elif entropy < 100:
        strength = "Strong"
    else:
        strength = "Very Strong"

    return jsonify({
        "entropy": round(entropy, 2),
        "strength": strength,
        "crack_time": format_time(avg_time)
    })

if __name__ == "__main__":
    app.run()
