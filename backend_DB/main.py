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
            session["email"] = user["email"]

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

    result = 0

    try:
        while True:
            sql = 'select count(*) from users where usernum = %s'
            cur.execute(sql, (check_usernum,))
            result = cur.fetchone()['count(*)']
            if result == 1:
                check_usernum += 1
            else:
                break
        
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
    
@app.route("/mypage", methods=["GET"])
def mypage():
    if not session.get('sign_in_status'):
        flash('ログインしてください')
        return redirect('/sign_in')
    else:
        usernum = session["usernum"]
        email = session["email"]
        accountname = session["accountname"]
        return render_template('mypage.html',email = email, usernum = usernum, accountname = accountname)

@app.route("/changeProfile",methods=["GET"])
def changeProfile():
    if not session.get('sign_in_status'):
        flash('ログインしてください')
        return redirect('/sign_in')
    else:
        usernum = session["usernum"]
        email = session["email"]
        accountname = session["accountname"]
        return render_template('changeProfile.html',email = email, usernum = usernum, accountname = accountname)

@app.route("/changeProfile",methods=["POST"])
def changeProfile_():
    usernum = session['usernum']

    gotPassword = request.form.get('password')

    gotPassword = hashlib.sha256(gotPassword.encode('utf-8')).hexdigest()

    #パスワードチェック
    try:
        cnx = database_connection()
        cur = cnx.cursor(dictionary=True)
        sql = 'select * from users where password = %s'
        cur.execute(sql,(gotPassword, ))

        passwordCheck = cur.fetchone()

        if not passwordCheck:
            flash('パスワードが違います')
            return redirect('/changeProfile')
    except Exception as e:
        print(e)
        return redirect('/')
    

    #新登録情報のチェックと更新
    try:
        newEmail = request.form.get('newEmail')
        newAccountname = request.form.get('newAccountname')

        #デバックチェック用
        print(f'newaccountname:{newAccountname}')
        print(f'newEmail:{newEmail}')

        if not newEmail and not newAccountname:
            flash('変更したい情報を1つ以上入力してください')
            return redirect('/changeProfile')


        cnx = database_connection()
        cur = cnx.cursor(dictionary=True)

        if newEmail:
            sql = 'UPDATE users SET email = %s WHERE usernum = %s'
            cur.execute(sql,(newEmail, usernum, ))
        if newAccountname:
            sql = 'UPDATE users SET accountname = %s WHERE usernum = %s'
            cur.execute(sql, (newAccountname, usernum, ))
    except Exception as e:
        print(e)
        return redirect('/')



    #登録情報更新後のアカウント情報取得
    if cnx.is_connected():
        cur = cnx.cursor(dictionary=True)
        cur.execute(
            "SELECT * FROM users WHERE usernum = %s",
            (usernum,)
        )

        user = cur.fetchone()

    if user:
        session['accountname'] = user['accountname']
        session["email"] = user["email"]

        
        accountname = user['accountname']
        email = user["email"]

        flash('アカウント情報が変更されました')

    return render_template('mypage.html',usernum = usernum,accountname = accountname, email = email)


@app.route("/changePassword",methods=["GET"])
def changePassword():
    if not session.get('sign_in_status'):
        flash('ログインしてください')
        return redirect('/sign_in')
    else:
        usernum = session["usernum"]
        email = session["email"]
        accountname = session["accountname"]
        return render_template('changePassword.html',email = email, usernum = usernum, accountname = accountname)


@app.route("/changePassword",methods=["POST"])
def changePassword_():
    usernum = session['usernum']

    oldPassword = request.form.get('oldPassword')
    
    oldPassword = hashlib.sha256(oldPassword.encode('utf-8')).hexdigest()
    

    #パスワードチェック
    try:
        cnx = database_connection()
        cur = cnx.cursor(dictionary=True)
        sql = 'select * from users where password = %s'
        cur.execute(sql,(oldPassword, ))

        passwordCheck = cur.fetchone()

        if not passwordCheck:
            flash('パスワードが違います')
            return redirect('/changePassword')
    except Exception as e:
        print(e)
        return redirect('/')
    
    #新パスワードのチェック
    try:
        newPassword = request.form.get('newPassword')
        checkNewPassword = request.form.get('checkNewPassword')

        if not newPassword or not checkNewPassword:
            flash('新パスワードを入力してください')
            return redirect('/changePassword')

        newPassword = hashlib.sha256(newPassword.encode('utf-8')).hexdigest()
        checkNewPassword = hashlib.sha256(checkNewPassword.encode('utf-8')).hexdigest()

        #デバック確認用
        print(f'newpassword:{newPassword}')
        print(f'checknewpassword:{checkNewPassword}')

        if newPassword != checkNewPassword:
            flash('新パスワードが一致しません')
            return redirect('/changePassword')
        
    except Exception as e:
        print(e)
        return redirect('/')


    #パスワードを新パスワードに変更
    try:
        cnx = database_connection()
        cur = cnx.cursor(dictionary=True)

        sql = 'UPDATE users SET password = %s WHERE usernum = %s'
        cur.execute(sql,(newPassword, usernum, ))

        cnx.commit()

    except Exception as e:
        print(e)
        return redirect('/')


    usernum = session['usernum']
    accountname = session['accountname']
    email = session['email']

    flash('パスワードが変更されました')

    return render_template('mypage.html',usernum = usernum,accountname = accountname, email = email)



#flask起動
if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=8080)