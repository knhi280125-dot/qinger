import os
import json
from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__, template_folder='templates', static_folder='templates', static_url_path='')
app.config['PROPAGATE_EXCEPTIONS'] = True

# Kết nối Firebase
cred_path = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")

if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"Lỗi Firebase: {e}")

db = firestore.client()

@app.route('/')
def home():
    # Thử gọi index.html, nếu không có thì gọi search.html để tránh lỗi 500
    try:
        return render_template('index.html')
    except:
        return render_template('search.html', teachers=[], keyword="Vui lòng kiểm tra file index.html trong templates")

@app.route('/search', methods=['GET', 'POST'])
def search():
    teachers = []
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        # Tìm trong collection của Nhi (靜宜資管)
        try:
            docs = db.collection("靜宜資管").stream()
            for doc in docs:
                data = doc.to_dict()
                if keyword and keyword in str(data.get("name", "")):
                    teachers.append(data)
        except:
            pass
    return render_template('search.html', teachers=teachers)

app = app
