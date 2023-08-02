from threading import Thread
from flask import current_app, render_template
from . import mail
from flask_mail import Message

# Function to send email asynchronously
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

# Email support
def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['IMAGINESTUDIOS_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['IMAGINESTUDIOS_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)

    # Create a new thread to send the email asynchronously
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()

    # Return the thread object to allow monitoring the email sending status
    return thr
    # mail.send(msg)
