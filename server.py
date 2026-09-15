import os
import requests
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder=".")

KEY = os.getenv("TWELVE_DATA_API_KEY", "")

@app.get("/")
def home():
    return send_from_directory(".", "index.html")

@app.get("/api/quotes")
def quotes():
    if not KEY:
        return jsonify(error="TWELVE_DATA_API_KEY missing"), 503

    out = {}

    for symbol in request.args.get("symbols", "").split(","):
        symbol = symbol.strip()
        if not symbol:
            continue

        try:
            response = requests.get(
                "https://api.twelvedata.com/quote",
                params={"symbol": symbol, "apikey": KEY},
                timeout=10
            )

            data = response.json()

            if data.get("status") == "error":
                out[symbol] = {"error": data.get("message", "API error")}
            else:
                out[symbol] = {
                    "price": data.get("close") or data.get("price"),
                    "percent_change": data.get("percent_change", 0)
                }

        except Exception as e:
            out[symbol] = {"error": str(e)}

    return jsonify(out)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8080"))
)
