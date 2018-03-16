import os
import smtplib
import yaml
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

COMMASPACE = ', '

ERROR_SUBJECT = '[pywikibot] Error during import'
ERROR_BODY = "Error occurred during import. See attached file for more information.\n\n"

SUCCESS_SUBJECT = '[pywikibot] Import finished'
SUCCESS_BODY = "The Import is finished. See attached file for more information.\n\n"

with open('../config.yaml', 'r', encoding='utf-8') as config_file:
    config = yaml.load(config_file)

SENDER = config['mail']['sender']
RECIPIENT = config['mail']['recipients']
HOST = config['mail']['host']
PORT = config['mail']['port']
PWD = config['mail']['password']
ATTACHMENTS = [config['log']]


def send(subject, body):

    outer = MIMEMultipart()
    outer['Subject'] = subject
    outer['To'] = COMMASPACE.join(RECIPIENT)
    outer['From'] = SENDER

    text = MIMEText(body)
    outer.attach(text)

    for file in ATTACHMENTS:
        try:
            with open(file, 'rb') as fp:
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(fp.read())

            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            outer.attach(msg)

        except BaseException as exception:
            logging.error(' Attachment could nit be loaded: ' + repr(exception))
            raise

    composed = outer.as_string()

    try:
        with smtplib.SMTP_SSL(HOST, PORT) as s:
            s.login(SENDER, PWD)
            s.sendmail(SENDER, RECIPIENT, composed)

        logging.info(" E-mail successfully send.")

    except BaseException as exception:
        logging.error(' E-mail could not be sent: ' + repr(exception))
        raise


def send_error():
    send(ERROR_SUBJECT, ERROR_BODY)


def send_success():
    send(SUCCESS_SUBJECT, SUCCESS_BODY)
