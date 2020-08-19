import os
from imaplib import IMAP4_SSL
from configparser import ConfigParser

config = ConfigParser()
config.read("imap-checker.ini")
imap_host = config['MailRu']['imap_host']
imap_port = config['MailRu']['imap_port']
username = config['MailRu']['username']
token = config['MailRu']['token']
action_url = config['MailRu']['action_url']
history_url = config['MailRu']['history_url']

with IMAP4_SSL(host=imap_host, port=imap_port) as M:
    M.login(username, token)
    M.select()
    return_code, mail_ids = M.search(None, 'UnSeen')
    mail_ids_splitted= mail_ids[0].decode().split(" ")
    if mail_ids_splitted[0] == '':
        unread_count = 0
        os.system("termux-notification-remove imap-checker")
    else:
        unread_count = len(mail_ids_splitted)
        os.system("termux-notification -i imap-checker \
        -t 'mail.ru' \
        -c 'unread messages: {}' \
        --action 'termux-open-url {}; \
          termux-notification-remove imap-checker' \
        --button1 'history' \
        --button1-action 'termux-open-url {}; \
          termux-notification-remove imap-checker' \
        --led-color 0000FF".format(unread_count, action_url, history_url))

