from flask import Flask, render_template, request, redirect, url_for
import sqlite3, os

app = Flask(__name__)
app.config['DB_NAME'] = os.getcwd() + '/buku.db'

conn = cursor = None

def openDB():
    """
        Open Database Connection
    """
    global conn, cursor
    conn = sqlite3.connect(app.config['DB_NAME'])
    cursor = conn.cursor()

def closeDB():
    """
        Close Database Connection
    """
    global conn, cursor
    cursor.close()
    conn.close()

@app.route('/')
def index():
    openDB()
    data = []
    for id,title,author,publisher in cursor.execute('SELECT * FROM buku'):
        data.append((id,title,author,publisher))
    closeDB()
    return render_template('index.html', data=data)

@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        id = request.form['id']
        title = request.form['title']
        author = request.form['author']
        publisher = request.form['publisher']
        data = id,title,author,publisher
        openDB()
        cursor.execute('INSERT INTO buku VALUES(?,?,?,?)', data)
        conn.commit()
        closeDB()
        return redirect(url_for('index'))
    else:
        return render_template('tambah.html')

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    openDB()
    result = cursor.execute('SELECT * FROM buku WHERE id=?', (id,))
    data = cursor.fetchone()
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        publisher = request.form['publisher']
        cursor.execute('''
        UPDATE buku SET title=?, author=?, publisher=? WHERE id=?
        ''', (title, author, publisher, id))
        conn.commit()
        closeDB()
        return redirect(url_for('index'))
    else:
        closeDB()
        return render_template('edit.html', data=data)

@app.route('/hapus/<id>', methods=['GET', 'POST'])
def hapus(id):
    openDB()
    cursor.execute('DELETE FROM buku WHERE id=?', (id,))
    conn.commit()
    closeDB()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)