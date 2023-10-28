from flask import Flask, render_template, request, redirect, flash, url_for
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "blog_post"

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO register (name, email, password) VALUES(%s, %s, %s)", (username, email, password))
        mysql.connection.commit()
        cur.close()
        flash('Registration successful!')
        return redirect(url_for('login'))

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Please provide both username and password.')
            return redirect(url_for('login'))

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM register WHERE name = %s", (username,))
        user = cur.fetchone()

        if user and user[3] == password:  # Assuming password is stored at index 3 in your database
            flash('Login successful!', 'success')
            return redirect(url_for('blog'))  # Redirect to the blog page upon successful login
        else:
            flash('Invalid username or password.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')


    

@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    users = cur.execute("SELECT * FROM blog")

    if users > 0:
        userDetails = cur.fetchall()
        return render_template('users.html', userDetails=userDetails)
    
    
@app.route('/blog', methods=['GET', 'POST'])
def blog():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO blog (title, author, content) VALUES (%s, %s, %s)", (title, author, content))
        mysql.connection.commit()
        cur.close()

        flash('Blog post submitted successfully!')
        return redirect(url_for('home'))

    return render_template('blog.html')



if __name__ == '__main__':
    app.run(debug=True)

