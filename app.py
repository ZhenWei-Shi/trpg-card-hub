import os
import json
import uuid
import sqlite3
from functools import wraps
from flask import Flask, request, jsonify, render_template, session

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'characters.db')
CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')


def get_config():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS characters (
                id TEXT PRIMARY KEY,
                data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('is_admin'):
            return jsonify({"status": "error", "message": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated


# ── 页面路由 ──────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create')
def create_page():
    return render_template('player.html')

@app.route('/list')
def list_page():
    return render_template('char_list.html')

@app.route('/admin')
def admin_page():
    return render_template('admin.html')


# ── 配置 API ──────────────────────────────────────────────────────────────────

@app.route('/api/config')
def api_config():
    return jsonify(get_config())


# ── 角色卡 API ────────────────────────────────────────────────────────────────

@app.route('/api/save', methods=['POST'])
def save_character():
    try:
        req_data = request.get_json()
        char_id = req_data.get('id')
        char_data = req_data.get('data', {})

        if not char_id:
            char_id = str(uuid.uuid4())

        processed_data = {
            "id": char_id,
            "name": char_data.get('name', '无名氏'),
            "realm": char_data.get('realm', ''),
            "appearance": char_data.get('appearance', ''),
            "background": char_data.get('background', ''),
            "password": char_data.get('password', ''),
            "stats": char_data.get('stats', {}),
            "assets": char_data.get('assets', {}),
            "traits": char_data.get('traits', []),
            "skills": char_data.get('skills', []),
            "items": char_data.get('items', [])
        }

        with get_db() as conn:
            existing = conn.execute('SELECT id FROM characters WHERE id = ?', (char_id,)).fetchone()
            if existing:
                conn.execute(
                    'UPDATE characters SET data = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                    (json.dumps(processed_data, ensure_ascii=False), char_id)
                )
            else:
                conn.execute(
                    'INSERT INTO characters (id, data) VALUES (?, ?)',
                    (char_id, json.dumps(processed_data, ensure_ascii=False))
                )
            conn.commit()

        return jsonify({"status": "success", "id": char_id})
    except Exception as e:
        print(f"Save error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/get/<char_id>', methods=['GET'])
def get_character(char_id):
    pwd = request.args.get('pwd', '')
    with get_db() as conn:
        row = conn.execute('SELECT data FROM characters WHERE id = ?', (char_id,)).fetchone()
    if not row:
        return jsonify({"status": "error", "message": "Character not found"}), 404
    char_data = json.loads(row['data'])
    if char_data.get('password') and char_data['password'] != pwd:
        return jsonify({"status": "error", "code": "WRONG_PASSWORD"}), 403
    return jsonify({"status": "success", "data": char_data})


@app.route('/api/verify/<char_id>', methods=['POST'])
def verify_password(char_id):
    data = request.get_json()
    pwd = data.get('password', '')
    with get_db() as conn:
        row = conn.execute('SELECT data FROM characters WHERE id = ?', (char_id,)).fetchone()
    if not row:
        return jsonify({"status": "error"}), 404
    char_data = json.loads(row['data'])
    if char_data.get('password') == pwd:
        return jsonify({"status": "success", "data": char_data})
    return jsonify({"status": "error", "message": "Wrong password"}), 403


@app.route('/api/list', methods=['GET'])
def get_all_characters():
    with get_db() as conn:
        rows = conn.execute('SELECT data FROM characters ORDER BY created_at DESC').fetchall()
    result = []
    for row in rows:
        char_data = json.loads(row['data'])
        result.append({
            "id": char_data['id'],
            "name": char_data['name'],
            "realm": char_data.get('realm', ''),
            "appearance": char_data.get('appearance', ''),
            "has_password": bool(char_data.get('password', '').strip()),
            "stats": char_data.get('stats', {}),
            "traits": char_data.get('traits', []),
            "skills": char_data.get('skills', [])
        })
    return jsonify({"status": "success", "list": result})


@app.route('/api/delete/<char_id>', methods=['DELETE'])
def delete_character(char_id):
    with get_db() as conn:
        result = conn.execute('DELETE FROM characters WHERE id = ?', (char_id,)).rowcount
        conn.commit()
    if result:
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Character not found"}), 404


# ── DM 管理后台 API ───────────────────────────────────────────────────────────

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    pwd = data.get('password', '')
    config = get_config()
    if pwd == config.get('admin', {}).get('password', ''):
        session['is_admin'] = True
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "密码错误"}), 403


@app.route('/api/admin/logout', methods=['POST'])
def admin_logout():
    session.pop('is_admin', None)
    return jsonify({"status": "success"})


@app.route('/api/admin/list', methods=['GET'])
@admin_required
def admin_list():
    with get_db() as conn:
        rows = conn.execute(
            'SELECT data, created_at, updated_at FROM characters ORDER BY created_at DESC'
        ).fetchall()
    result = []
    for row in rows:
        char_data = json.loads(row['data'])
        char_data['created_at'] = row['created_at']
        char_data['updated_at'] = row['updated_at']
        result.append(char_data)
    return jsonify({"status": "success", "list": result})


@app.route('/api/admin/delete/<char_id>', methods=['DELETE'])
@admin_required
def admin_delete(char_id):
    with get_db() as conn:
        result = conn.execute('DELETE FROM characters WHERE id = ?', (char_id,)).rowcount
        conn.commit()
    if result:
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 404


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)
