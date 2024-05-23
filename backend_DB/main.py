from flask import Flask, render_template, redirect, request, session ,flash ,url_for
import mysql.connector
import hashlib
import random
from collections import Counter
from flask import flash

app = Flask(__name__)
app.secret_key = 'あなたのシークレットキー'


def database_connection():
    # どこに接続をするか
    return mysql.connector.connect(
        user='root',
        password='',
        # password='root',
        host='localhost',
        port='3306',
        database='dakend'
    )


@app.route("/")
def index():
    #セッションから必要な情報を取得
    sign_in_status = session.get("sign_in_status", False)
    #user_num = session.get("usernum", None)
    #user_name = session.get("username", None)
    #user_points = session.get("points", None)

    return render_template("index.html", sign_in_status = sign_in_status)#,user_num = user_num, userName=user_name, points=user_points)


@app.route("/sign_in",methods=["GET"])
def sign_in():

    if session.get("sign_in"):
        flash('既にログインしています')
        return redirect("/")

    return render_template("sign_in.html")

@app.route("/sign_in",methods=["POST"])
def sign_in_():
    flash('')

    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        flash('メールとパスワードを入力してください')
        return redirect("/sign_in")
    
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    try:
        cnx = database_connection()
        if cnx.is_connected():
            cur = cnx.cursor(dictionary=True)
            cur.execute(
                "SELECT * FROM users WHERE email = %s and password = %s",
                (email, password,)
            )

        user = cur.fetchone()

        if user:
            session["sign_in"] = True
            session["usernum"] = user['usernum']
            session['username'] = user['username']
            session['acountname'] = user['acountname']

            usernum = user['usernum']
            username = user['username']
            acountname = user['acountname']

        else:
            flash('メールアドレスまたはパスワードが違います')
            return redirect('/sign_in')
        cnx.close
    
    except Exception as e:
        print(e)
        return redirect('/sign_in') 


    return render_template("index.html",email = email, usernum = usernum, username = username, acountname = acountname)


@app.route("/sign_out")
def sign_out():
    session["sign_in_status"] = False
    
    return redirect("/")





#flask起動
if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=8080)