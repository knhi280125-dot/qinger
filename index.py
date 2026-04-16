import os
from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__, template_folder='templates', static_folder='templates', static_url_path='')

# Kết nối Firebase
cred_path = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    teachers = []
    keyword = ""
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        # Truy vấn vào bộ dữ liệu của Nhi
        docs = db.collection("靜宜資管").stream()
        for doc in docs:
            data = doc.to_dict()
            # Kiểm tra nếu tên giáo viên có chứa từ khóa Nhi nhập
            if keyword and keyword in str(data.get("name", "")):
                teachers.append(data)
    return render_template('search.html', teachers=teachers, keyword=keyword)

app = app
