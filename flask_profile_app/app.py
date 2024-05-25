from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_users_by_group(group_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE group_id = ?", (group_id,))
    users = cursor.fetchall()
    conn.close()
    return users

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            Province TEXT NOT NULL,
            District TEXT NOT NULL,
            group_id INTEGER

        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        province = request.form['province']
        district = request.form['district']
        group_id = request.form['group_id']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (name, surname, Province, District, group_id) VALUES (?, ?, ?, ?, ?)",
                  (name, surname, province,district,group_id))
        conn.commit()
        conn.close()

        return redirect(f'/members/{group_id}')
    return render_template('register.html')

@app.route('/group', methods=['GET', 'POST'])
def group():
    if request.method == 'POST':
        group_id = request.form['group_id']
        return redirect(f'/members/{group_id}')  # Corrected the syntax here
    return render_template('group.html')


@app.route('/members/<int:group_id>')
def members(group_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE group_id=?", (group_id,))
    members = c.fetchall()
    conn.close()
    return render_template('members.html', members=members)

if __name__ == '__main__':
    app.run(debug=True)
