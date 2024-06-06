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
    usernum = session.get("usernum", None)
    accountname = session.get("accountname", None)
    

    return render_template("index.html", sign_in_status = sign_in_status, usernum = usernum, accountname = accountname)#,user_num = user_num, userName=user_name, points=user_points)


@app.route("/sign_in",methods=["GET"])
def sign_in():

    if session.get("sign_in_status"):
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
            session["sign_in_status"] = True
            session["usernum"] = user['usernum']
            session['accountname'] = user['accountname']

            usernum = user['usernum']
            accountname = user['accountname']

        else:
            flash('メールアドレスまたはパスワードが違います')
            return redirect('/sign_in')
        cnx.close
    
    except Exception as e:
        print(e)
        return redirect('/sign_in') 


    return render_template("index.html",sign_in_status=session.get('login',True),email = email, usernum = usernum, accountname = accountname)


@app.route("/sign_out")
def sign_out():
    session['sign_in_status'] = False
    session['usernum'] = False
    session['accountname'] = False

    return redirect("/")


@app.route("/sign_up", methods=["GET"])
def sign_up():
    if session.get('sign_in_status'):
        flash('すでにログインしています')
        return redirect('/')
    return render_template("sign_up.html")

@app.route("/sign_up", methods=["POST"])
def sign_up_():
    flash('')

    email = request.form.get("email")
    password = request.form.get("password")
    accountname = request.form.get("accountname")    

    if not email or not password or not accountname:
        flash('情報を正しく入力してください')
        print(email)
        print(password)
        print(accountname)
        return render_template("sign_up.html")

    password = hashlib.sha256(password.encode('utf-8')).hexdigest()


    #まずemailがかぶっていないかのチェック
    check_email = 0

    try:
        cnx = database_connection()
        cur = cnx.cursor(dictionary=True)
        sql = 'select count(*) from users where email = %s'
        cur.execute(sql, (email,))
        check_email = cur.fetchone()['count(*)']
        if check_email == 1:
            flash('このemailアドレスは使用できません')
            return render_template('sign_up.html')
    except Exception as e:
        print(e)


    #新規追加ユーザーのusernumの決定
    check_usernum = 1
    check_result_usernum = 0

    flag = 0
    result = 0

    try:
        while flag == 0:
            sql = 'select count(*) from users where usernum = %s'
            cur.execute(sql, (check_usernum,))
            result = cur.fetchone()['count(*)']
            if result == 1:
                check_usernum += 1
            else:
                flag += 1
        
        resultusernum = check_usernum

    except Exception as e:
        print(e)


    #usernumが決定したのでusersテーブルに新規追加
    try:
        sql = "INSERT INTO users (usernum, email, password, accountname) VALUES (%s, %s, %s, %s)"
        cur.execute(sql, (resultusernum,email, password, accountname))
        cnx.commit()

    except Exception as e:
        print(e)


    return redirect("/sign_in")

@app.route("/game")
def game():
    if not session.get('sign_in_status'):
        flash('ログインしてください')
        return redirect('/sign_in')
    else:
        return render_template('game.html')



#flask起動
if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=8080)