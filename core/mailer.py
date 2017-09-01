import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

COMMASPACE = ', '


class Mailer:
    @staticmethod
    def sent_mail(host, port, password, sender, recipients, subject, body, attachments):

        # Create the enclosing (outer) message
        outer = MIMEMultipart()
        outer['Subject'] = subject
        outer['To'] = COMMASPACE.join(recipients)
        outer['From'] = sender
        outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

        text = MIMEText(body)
        outer.attach(text)

        # List of attachments

        # Add the attachments to the message
        for file in attachments:
            try:
                with open(file, 'rb') as fp:
                    msg = MIMEBase('application', "octet-stream")
                    msg.set_payload(fp.read())
                encoders.encode_base64(msg)
                msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
                outer.attach(msg)
            except BaseException as exception:
                logging.error("ERROR: While loading attachment for error mail: %s" % repr(exception))
                raise

        composed = outer.as_string()

        # Send the email
        try:
            with smtplib.SMTP_SSL(host, port) as s:
                s.login(sender, password)
                s.sendmail(sender, recipients, composed)
            logging.info("Email successfully sent.")
        except BaseException as exception:
            logging.error("ERROR: Unable to send the email: %s" % repr(exception))
            raise
