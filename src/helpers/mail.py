

import config

from google.appengine.api import mail

def send_mail_to_user(to, subject, body, **kw):
  mail.send_mail(sender='MemeGen <noreply@' + config.EMAIL_DOMAIN + '>',
    to=to,
    subject=subject,
    body=body)
