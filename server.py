import os,requests
from flask import Flask,jsonify,request,send_from_directory
app=Flask(__name__,static_folder=".")
KEY=os.getenv("TWELVE_DATA_API_KEY","")
@app.get("/")
def home(): return send_from_directory(".", "index.html")
@app.get("/api/quotes")
def quotes():
    if not KEY:return jsonify(error="TWELVE_DATA_API_KEY missing"),503
    out={}
    for s in request.args.get("symbols","").split(","):
        if not s:continue
        try:
            d=requests.get("https://api.twelvedata.com/quote",params={"symbol":s,"apikey":KEY},timeout=10).json()
            if d.get("status")!="error":out[s]={"price":d.get("close") or d.get("price"),"percent_change":d.get("percent_change",0)}
        except: pass
    return jsonify(out)
app.run(host="0.0.0.0",port=int(os.getenv("PORT","8080")))
