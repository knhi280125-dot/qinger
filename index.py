from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

cred = credentials.Certificate("serviceAccountKey.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        keyword = request.form.get("keyword")
        teachers = []
        docs = db.collection("靜宜資管").stream()
        for doc in docs:
            data = doc.to_dict()
            if keyword in data.get("name", ""):
                teachers.append(data)
        return render_template("search.html", teachers=teachers, keyword=keyword)
    return render_template("search.html")

if __name__ == "__main__":
    app.run(debug=True)