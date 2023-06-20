from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from website import database
from flask_login import login_required, logout_user, current_user
from requests import get
from mail import validate_email_regex
from callmodel import predict_gender
auth = Blueprint("auth", __name__)
import os
import math
import random
import smtplib
from dt import getdate
otp=""
digits="0123456789"
email5=""
email6=""
@auth.route("/login", methods=["GET", "POST"])
def login():
    global email6
    if request.method == "POST":
        email = request.form.get("email")
        email6=email

        password = request.form.get("password")
        user = database.check_email(email)
        if user:
            or_pass = database.get_pass(email)
            if check_password_hash(or_pass, password):

                flash("", category="success")
                mainmail=email
                curr_ip = get('https://api.ipify.org').content.decode('utf8')
                curr_episode=database.get_episode(email)
                curr_date = getdate()

                if(curr_episode)=="episode1" and database.getchat(email)=='':

                    database.update_time(email,curr_date,curr_episode)
                else:
                    epdate=database.get_episodetime(email,curr_episode)

                    if(curr_date==epdate):
                        pass
                    else:
                        database.createnewepisode(email,curr_date,curr_episode)





                old_ip = database.get_ip(email)
                if curr_ip == old_ip:
                    pass
                else:
                    new_ip = database.update_ip(email,curr_ip)
                return render_template("home.html", user=current_user)
            else:
                flash("Incorrect password!", category="error")
        else:
            flash("User does not exist!", category="error")

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/register", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        gender=predict_gender(name)
        password = request.form.get("password")
        password_confirm = request.form.get("password-confirm")

        user = database.check_email(email)
        if user:
            flash("Email already exists!", category="error")
        elif len(email) < 4 or validate_email_regex(email) == False:
            flash("Invalid Email!", category="error")
        elif len(name) < 4:
            flash("Name is less than 4 characters!", category="error")
        elif len(password) < 8:
            flash("Name is less than 8 characters!", category="error")
        elif password != password_confirm:
            flash("Passwords don\'t mach!", category="error")
        else:
            ip = get('https://api.ipify.org').content.decode('utf8')




            database.Create_user(uemail=email, uname=name, upass=generate_password_hash(password, method="sha256"), ip_add = ip,gender1=gender)
            flash("Account Successfully Created", category="success")
            return redirect(url_for("auth.login"))

    return render_template("register.html", user=current_user)


def otp_gen():
    global otp
    for i in range(6):
        otp += digits[math.floor(random.random() * 10)]
    return otp



@auth.route("/forget", methods=["GET", "POST"])
def forget():
    global otp
    otp=""
    global email5
    if request.method == "POST":
        email5 = request.form.get("email")
        user = database.check_email(email5)
        if user:
            otp = otp_gen()
            msg = email_body = f"We have received a request to reset your account password.If you didn't request, please contact our support team immediately at amjadmoiz11@gmail.com.\n\nYour otp to reset password is {otp}"
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("amjadmoiz11@gmail.com", "wbzzljlhsjxbahcu")
            emailid = email5
            s.sendmail('&&&&&&&&&&&', emailid, msg)
            return render_template("forget2.html", email=email5)
        else:
            flash("User does not exist!", category="error")
    return render_template("forget.html",user=current_user)

@auth.route("/verify_otp", methods=["POST"])
def verify_otp():
    if request.method == "POST":
        global otp
        email = request.form.get("email")
        user_otp = request.form.get("otp")
        if user_otp==otp:
            return render_template("forget3.html", email=email5)
            otp=""
        else:
            flash("Invalid OTP. Please try again.", category="error")
            return redirect(url_for("auth.forget"))
    return render_template("forget2.html",user=current_user)

@auth.route("/update_password", methods=["POST"])
def update_password():
    if request.method == "POST":

        new_password = request.form.get("password")

        new_password=generate_password_hash(new_password, method="sha256")
        database.update_pass(email5,new_password)
        flash("Password updated successfully.", category="success")
        return redirect(url_for("auth.login"))
    return render_template("forget3.html", user=current_user)




