from flask import Flask, render_template, request
import requests
import smtplib
import os

posts = requests.get("https://api.npoint.io/1c94ebcc9402cea17804").json()

app = Flask(__name__)

@app.route("/")
def get_all_posts():
    return render_template("index.html", all_posts=posts)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)

@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        print(name, email, phone, message)
        send_message(name, email, phone, message)
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)

def send_message(name, email, phone, message):
    password = os.environ["PASSWORD"]
    username = os.environ["EMAIL"]
    message = f"Subject: New Message\n\nName: {name}\nEmail: {email}\n Phone: {phone}\n Message: {message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=username, password=password)
        connection.sendmail(
            from_addr=username,
            to_addrs=username,
            msg=message,
        )

if __name__ == "__main__":
    app.run(debug=True)
