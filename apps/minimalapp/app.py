from email_validator import validate_email, EmailNotValidError
from flask import (
    Flask,
    current_app,
    g,
    render_template,
    url_for,
    request,
    redirect,
    flash,
    make_response,
    session,
)
import logging
import os
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail, Message

app = Flask(__name__)
app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ"

app.config["DEBUG"] = True
app.logger.setLevel(logging.DEBUG)
# リダイレクトを中断しないようにする
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
# DebugToolbarExtensionにアプリケーションをセットする
toolbar = DebugToolbarExtension(app)
app.logger.critical("fatal error")
app.logger.error("error")
app.logger.warning("warning")
app.logger.info("info")
app.logger.debug("debug")

# Mailクラスのコンフィグを追加
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")
# flask-mail拡張を登録する
mail = Mail(app)


@app.route("/")
def index():
    return "Hello, Flaskbook!"


@app.route("/hello/<name>", methods=["GET"], endpoint="hello-endpoint")
def hello(name):
    return f"Hello, {name}!"


@app.route("/name/<name>")
def show_name(name):
    return render_template("index.html", name=name)


@app.route("/contact")
def contact():
    # レスポンスオブジェクトを取得する
    response = make_response(render_template("contact.html"))
    # クッキーを設定する
    response.set_cookie("flaskbook key", "flaskbook value")
    # セッションを設定する
    session["username"] = "ichiro"
    # レスポンスオブジェクトを返す
    return response
    return render_template("contact.html")


@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        # フォーム属性を使ってフォームの値を取得する
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        send_email(
            email,
            "問い合わせありがとうございました。",
            "contact_mail",
            username=username,
            description=description,
        )

        is_valid = True
        if not username:
            flash("ユーザー名は必須です")
            is_valid = False
        if not email:
            flash("メールアドレスは必須です")
            is_valid = False
        try:
            validate_email(email)
        except EmailNotValidError:
            flash("メールアドレスの形式で入力してください")
            is_valid = False
        if not description:
            flash("問い合わせ内容は必須です")
            is_valid = False
        if not is_valid:
            return redirect(url_for("contact"))

        flash("問い合わせ内容はメールにて送信しました。問い合わせありがとうございます。")
        return redirect(url_for("contact_complete"))
    return render_template("contact_complete.html")


def send_email(to, subject, template, **kwargs):
    """メールを送信する関数"""
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)


with app.test_request_context():
    print(url_for("index"))
    print(url_for("hello-endpoint", name="world"))
    print(url_for("show_name", name="ichiro", page=1))

# アプリケーションコンテキストを取得してスタックへpushする
ctx = app.app_context()
ctx.push()

# current_appにアクセスが可能になる
print(current_app.name)
# >> apps.minimalapp.app

# グローバルなテンポラリ領域に値を設定する
g.connection = "connection"
print(g.connection)
# >> connection

with app.test_request_context("/users?updated=true"):
    # trueが出力される
    print(request.args.get("updated"))
