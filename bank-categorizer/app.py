from flask import Flask, render_template, request, jsonify
import os, json

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_project', methods=['POST'])
def save_project():
    data = request.get_json()
    filename = data.get("filename")
    content = data.get("content")
    if not filename or not content:
        return jsonify({"error": "Missing filename or content"}), 400
    path = os.path.join(UPLOAD_FOLDER, f"{filename}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=2, ensure_ascii=False)
    return jsonify({"message": f"Saved {filename}.json successfully"})

@app.route('/list_projects')
def list_projects():
    files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".json")]
    return jsonify(files)

@app.route('/load_project/<filename>')
def load_project(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(path):
        return jsonify({"error": "File not found"}), 404
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
