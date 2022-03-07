
from flask import Flask, render_template, request
from smtplib import SMTP, SMTPResponseException, SMTPAuthenticationError
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/generic')
def generic():
    return render_template('generic.html')


@app.route('/elements')
def elements():
    return render_template('elements.html')


@app.route('/send_email', methods=["POST"])
def send_email():
    # Gather info from form
    from_email = request.form["email"]
    email_message = request.form["message"]
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    category = request.form["category"]

    # test_email
    smtp_email = os.getenv("my_email")
    smtp_pass = os.getenv("password")

    # Prod email
    smtp_email = os.getenv("codejet_email")
    smtp_pass = os.getenv("codejet_password")

    if from_email == "" or first_name == "" or first_name == "" or email_message == "" or category == "":
        return render_template("email_failure.html",
                               email=from_email,
                               name=f"{first_name} {last_name}",
                               message=email_message
                               )
    else:
        try:
            with SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(user=smtp_email, password=smtp_pass)
                connection.sendmail(
                    from_addr=from_email,
                    to_addrs="codejetsmtp@gmail.com",
                    msg=f"Subject: New Inquiry from {first_name} {last_name} at {from_email}!\n\n"
                        f"Category: {category}\n"
                        f"{email_message}")
        except SMTPResponseException as e:
            error_message = f"Sorry we could not complete the request due to{e.smtp_error}"
            return error_message
        else:
            message = "We will be in touch with you soon, " \
                      "please allow 3 business days for us to respond"
            return render_template("email_success.html", result=message)


if __name__ == "__main__":
    app.run(debug=True)

