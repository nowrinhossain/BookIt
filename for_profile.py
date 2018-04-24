from flask import Flask, render_template, request, redirect, url_for
from mysql.connector import MySQLConnection, Error
import MySQLdb
import sys
from PIL import Image
import base64
import six
import io
import PIL.Image
import pymysql
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)

conn = MySQLdb.connect(host="localhost", user="root", password="allahpleasehelpme", db="bookit_db")






@app.route("/",methods=["POST","GET"])



def read_blob():

        myname = "nowrinneetu95@gmail.com"
        cursor = conn.cursor()
        cursor.execute("SELECT username,location,user_image FROM user WHERE email LIKE %s",(myname,))
        info = cursor.fetchone()
        username = info[0]
        location = info[1]
        user_image = info[2]

        if request.method == "POST":


            user_email = "nowri@gmail.com"
            book_name = str(request.form["book_name"])
            writer_name = str(request.form["writer_name"])
            category = str(request.form["category"])
            book_photo = request.files["book_image"]
            for_sell_rent = str(request.form["for_sell_rent"])
            price = request.form["book_price"]
            book_photo.filename = user_email+book_name+writer_name+".png"  # some custom file name that you want


            if for_sell_rent=="Add book for give rent" :

                UPLOAD_FOLDER = 'static/rent_book_photo'
                ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
                app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

                photo_name = secure_filename(book_photo.filename)
                book_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_name))

                book_image_path = "/static/rent_book_photo/"+photo_name


                cursor.execute("INSERT INTO rent_book (user_email,book_name,writer_name,category,book_image_path)VALUES(%s,%s,%s,%s,%s)",
                                         (user_email, book_name, writer_name, category,book_image_path))


            if for_sell_rent=="Add book for sell" :

                UPLOAD_FOLDER = 'static/sell_book_photo'
                ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
                app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

                photo_name = secure_filename(book_photo.filename)
                book_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_name))

                book_image_path = "/static/sell_book_photo/"+photo_name


                cursor.execute("INSERT INTO sell_book (user_email,book_name,writer_name,category,book_image_path)VALUES(%s,%s,%s,%s,%s)",
                                         (user_email, book_name, writer_name, category,book_image_path))



        cursor.close()
        conn.commit()

        return render_template('user_profile.html', username=username ,location=location)


@app.route("/edit_profile", methods=["GET","POST"])
def edit_profile():

    if request.method == "POST" :
        user_email = 'nowrinneetu95@gmail.com'
        change_username = str(request.form["change_username"])
        change_password = str(request.form["change_password"])
        change_location = str(request.form["change_location"])

        cursor1 = conn.cursor()

        if change_username :
            cursor1.execute("""
               UPDATE user
               SET username=%s
               WHERE email=%s
            """, (change_username, user_email))

        if change_password :
            cursor1.execute("""
               UPDATE user
               SET password=%s
               WHERE email=%s
            """, (change_password, user_email))


        if change_location :
            cursor1.execute("""
               UPDATE user
               SET location=%s
               WHERE email=%s
            """, (change_location, user_email))


        conn.commit()
        conn.close()


        #cursor1.execute(" UPDATE user SET username=%s WHERE email='%s' " % (change_username,user_email))

        print(change_username)

        #return redirect(url_for())



    return render_template("edit_profile.html")







#def user(username):

@app.route("/view_books", methods=["GET","POST"])

def view_books():

    myname = "nowri@gmail.com"


    cursor = conn.cursor()
    cursor.execute("SELECT book_name,writer_name,book_image_path FROM sell_book WHERE user_email LIKE %s", (myname,))
    sell_info = cursor.fetchall()

    cursor.execute("SELECT book_name,writer_name,book_image_path FROM rent_book WHERE user_email LIKE %s", (myname,))
    rent_info = cursor.fetchall()


    return render_template("view_books.html",rent_info=rent_info, sell_info = sell_info)



@app.route("/rent_book", methods=["GET","POST"])

def rent_book():
    cursor = conn.cursor()

    category = ""

    cursor.execute("SELECT book_name,writer_name,book_image_path,rent_price FROM rent_book")

    rent_book_info= cursor.fetchall()

    if request.method == "POST":

        #category = str(request.form["category"])
        book_name = str(request.form["search_book"])
        writer_name = str(request.form["search_writer"])
        print(book_name)

        cursor.execute("SELECT book_name,writer_name,book_image_path,rent_price FROM rent_book WHERE book_name LIKE %s", (book_name,))
        rent_book_info = cursor.fetchall()


    return render_template("rent_book.html", rent_book_info=rent_book_info)

    conn.commit()
    conn.close()

    #return render_template("rent_book.html")



@app.route("/rent_book_category", methods=["GET","POST"])
def rent_book_category():

    #url_ = request.url()

    category = request.args.get('cat')
    book_name = request.args.get('name')
    print(category)

    cursor = conn.cursor()

    cursor.execute("SELECT book_name,writer_name,book_image_path,rent_price FROM rent_book WHERE category LIKE %s",
                   (category,))
    rent_book_info = cursor.fetchall()




    return render_template("rent_book_category.html", rent_book_info = rent_book_info)


if __name__ == "__main__":
    app.run(debug=True)