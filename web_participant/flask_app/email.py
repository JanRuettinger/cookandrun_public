from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from .factory import mail
import boto3


def send_async_email(app, ses, sender, recipients, subject, text, html):
    with app.app_context():
        current_app.logger.info("In Sending Thread")
        ses.send_email(
            Source=sender,
            Destination={'ToAddresses': recipients},
            Message={
                'Subject': {'Data': subject},
                'Body': {
                    'Text': {'Data': text},
                    'Html': {'Data': html}
                }
            }
        )


def send_email(recipients, sender=None, subject='', template='', **kwargs):
    ses = boto3.client(
        'ses',
        region_name=current_app.config['SES_REGION_NAME'],
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY']
    )
    if not sender:
        sender = current_app.config['SES_EMAIL_SOURCE']

    html = render_template(template + '.html', **kwargs)
    text = render_template(template + '.txt', **kwargs)

    app = current_app._get_current_object()
    thr = Thread(target=send_async_email, args=[app, ses, sender, [recipients], subject,
        text, html])
    thr.start()
    return thr

