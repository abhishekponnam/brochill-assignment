from flask import Flask, request, render_template
import mysql.connector

app = Flask(__name__)

# Home page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Image upload functionality
        image = request.files['image']
        tags = request.form['tags']
        image_path = 'static/images/' + image.filename
        image.save(image_path)

        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin",
            database="brochill2",
            port=3306
        )
        cursor = db.cursor()
        sql = "INSERT INTO images (path, tags) VALUES (%s, %s)"
        val = (image_path, tags)
        cursor.execute(sql, val)
        db.commit()

        return render_template('index.html', success_message='Image uploaded successfully!')

    return render_template('index.html')


# Search functionality
@app.route('/search', methods=['GET'])
def search():
    tags = request.args.get('tags')

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="brochill2",
        port=3306
    )
    cursor = db.cursor()
    sql = "SELECT * FROM images WHERE tags LIKE %s ORDER BY path DESC"
    val = ("%" + tags + "%",)
    cursor.execute(sql, val)
    results = cursor.fetchall()

    return render_template('index.html', results=results, search_tags=tags)


if __name__ == '__main__':
    app.run(debug=True)
