from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL
import os

CELEBRITY_FOLDER = os.path.join('static', 'celeb-images')

app = Flask(__name__)

# database connection info. 
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'bri70122'
app.config['MYSQL_DATABASE_DB'] = 'cancelled_webdb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['UPLOAD_FOLDER'] = CELEBRITY_FOLDER

mysql = MySQL()
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

@app.route('/', methods=['GET', 'POST'])
def test():
    if request.method == "POST":
        return render_template('test.html')
    return render_template('test.html')

#endpoint for search
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        celeb = "%" + request.form['celeb'] + "%"
        cursor.execute("SELECT name, reason, image from cancel_celeb WHERE name LIKE %s", (celeb))
        conn.commit()
        data = cursor.fetchall()
        print(data)
        image = data[0][2]
        print(image)
        full_filenme = os.path.join(app.config['UPLOAD_FOLDER'], image)
        print(full_filenme)
        if len(data) == 0 and celeb == 'all':
            cursor.execute("SELECT name, reason, image from cancel_celeb")
            conn.commit()
            data = cursor.fetchall()
        return render_template('search.html', data=data, celeb_image=full_filenme)
    return render_template('search.html')

if __name__=='__main__':
    app.debug = True 
    app.run()