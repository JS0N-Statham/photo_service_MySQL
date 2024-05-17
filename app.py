from flask import Flask, request, render_template, redirect, session, flash, url_for
import pymysql.cursors
import json
import base64

app = Flask(__name__)
app.secret_key = 'secret_key'


def get_db_connection():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='1111',
                           database='object',
                           cursorclass=pymysql.cursors.DictCursor)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                query = ("SELECT id, data FROM users WHERE JSON_UNQUOTE(JSON_EXTRACT(data, '$.username')) = "
                         "%s AND JSON_UNQUOTE(JSON_EXTRACT(data, '$.password')) = %s")
                cursor.execute(query, (username, password))
                result = cursor.fetchone()
                if result:
                    session['user'] = {
                        'id': result['id'],
                        'username': json.loads(result['data'])['username']
                    }
                    return redirect(url_for('admin' if session['user']['username'] == 'ADMIN' else 'upload'))
                else:
                    flash('Неверные учетные данные')
    return render_template('login.html')


@app.route('/admin')
def admin():
    if 'user' in session and session['user']['username'] == 'ADMIN':
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                # Получение данных о пользователях
                cursor.execute("SELECT data FROM users")
                users = [json.loads(user['data']) for user in cursor.fetchall()]

                # Получение данных о фотографиях и соответствующих пользователях
                cursor.execute("""
                    SELECT u.data AS user_data, p.details AS photo_details
                    FROM photos p
                    JOIN users u ON p.user_id = u.id
                """)
                photos = [{'user': json.loads(row['user_data'])['username'],
                           'details': json.loads(row['photo_details'])}
                          for row in cursor.fetchall()]

        return render_template('admin.html', users=users, photos=photos)
    else:
        flash("Access restricted to administrators.")
        return redirect(url_for('login'))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        photo = request.files.get('photo')
        if photo and photo.filename:
            # Преобразование изображения в Base64
            photo_data = base64.b64encode(photo.read()).decode('utf-8')
            comment = request.form.get('comment', '')
            details = json.dumps({
                'image_data': photo_data,
                'comment': comment
            })
            with get_db_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO photos (user_id, details, image_data) 
                        VALUES (%s, %s, %s)
                    """, (session['user']['id'], details, photo_data))
                    connection.commit()
            flash('Фото успешно загружено')
            return redirect(url_for('success'))
    return render_template('upload.html')


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Вы успешно вышли из системы')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
