from config import ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
from resources import app
import logging
from logging.handlers import SMTPHandler

credentials = None
if MAIL_USERNAME or MAIL_PASSWORD:
    credentials = (MAIL_USERNAME, MAIL_PASSWORD)
mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-reply@' + MAIL_SERVER, ADMINS, 'NYC_API failure', credentials)
mail_handler.setLevel(logging.ERROR)
app.logger.addHandler(mail_handler)


def logger_message(msg):
    app.logger.error(msg)