import smtplib
import time
import imaplib
import email
import requests
import json

# -------------------------------------------------
#
# Utility to read email from Gmail Using Python then
# send results to Slack.
#
# ------------------------------------------------

ORG_EMAIL   = "@gmail.com"
FROM_EMAIL  = "plttradealerts" + ORG_EMAIL
FROM_PWD    = "Surfer17!"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"
SUBJECT_TO_SEARCH = '(SUBJECT "Awesome Bot Triggered")'
EMAIL_SUBJECT_FILENAME = "awesome_email_subject.txt"

def read_email_subject_file():
  try:
    f = open(EMAIL_SUBJECT_FILENAME, "r+")
  except IOError:
    f = open(EMAIL_SUBJECT_FILENAME, "w+")
  return f.readline()

def update_email_subject_file(email_subject):
  f = open(EMAIL_SUBJECT_FILENAME, "w")
  f.write(email_subject)

def get_subject_from_gmail():
  try:
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(FROM_EMAIL, FROM_PWD)
    mail.select('inbox')

    _type, data = mail.search(None, SUBJECT_TO_SEARCH)
    try:
      mail_ids = data[0]
    except IndexError:
      return

    id_list = mail_ids.split()
    if not id_list:
      return
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])

    # if len(id_list) > 1:
    #   for i in range(latest_email_id, first_email_id, -1):
    #     typ, data = mail.fetch(i, '(RFC822)')

    #     for response_part in data:
    #       if isinstance(response_part, tuple):
    #         msg = email.message_from_string(response_part[1])
    #         email_subject = msg['subject']
    #         email_from = msg['from']
    #         email_body = msg['body']
    # else:
    typ, data = mail.fetch(latest_email_id, '(RFC822)')

    if not data:
      return
    
    for response_part in data:
      if isinstance(response_part, tuple):
        msg = email.message_from_string(response_part[1])
        email_subject = msg['subject']
    return email_subject
  except Exception as e:
    print e

def send_result_to_slack(subject):
  '''
  Send email subject via webhook url to Slack.
  '''
  payload = {'text': subject}
  headers = {'content-type': 'application/json'}

  r = requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload), headers=headers)

def main():
  email_subject = get_subject_from_gmail()
  if email_subject is None:
    return
  if email_subject == read_email_subject_file():
    return
  else:
    send_result_to_slack(email_subject)
    update_email_subject_file(email_subject)

if __name__ == '__main__':
  main()
