from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
app = Flask(__name__)

@app.route("/")
def index():
    homepage = "<h1>黃汶樺Python讀取Firestore</h1>"
    homepage += "<a href=/account>網頁表單輸入實例</a><br><br>"
    homepage += "<a href=/search>課程查詢</a><br><br>"
    return homepage

@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        user = request.form["user"]
        pwd = request.form["pwd"]
        result = "您輸入的帳號是：" + user + "; 密碼為：" + pwd 
        return result
    else:
        return render_template("account.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        Cond = request.form["keyword"]
        teacher = request.form["teacher"]
        result = "您輸入的課程關鍵字是：" + Cond
        result = "您輸入的老師關鍵字是：" + teacher

        db = firestore.client()
        collection_ref = db.collection("111")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if Cond in dict["Course"] and teacher in dict["Leacture"]:
                #print("{}老師開的{}課程,每週{}於{}上課".format(dict["Leacture"], dict["Course"],  dict["Time"],dict["Room"]))
                result += dict["Leacture"] + "老師開的" + dict["Course"] + "課程,每週"
                result += dict["Time"] + "於" + dict["Room"] + "上課<br>"
        
        if result =="":
            result = "抱歉,查無相關條件的選修課程"
        
        return result
    else:
        return render_template("search.html")

if __name__ == "__main__":
    app.run()