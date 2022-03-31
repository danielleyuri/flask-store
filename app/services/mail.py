from app.extensions import mail
from flask import current_app, render_template
from flask_mail import Message


# Envio de e-mail para o envio de senha temporaria
def send_mail(subject, to, template, **kwargs): 
     msg = Message(subject=subject, recipients=[to], sender=current_app.config["MAIL_SENDER"])

     msg.body = render_template(f"mails/{template}.txt", **kwargs)
     msg.body = render_template(f"mails/{template}.html", **kwargs)
 
     mail.send(msg)
