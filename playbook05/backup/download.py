import imaplib as im
import os
import email

mail = im.IMAP4_SSL('imap.gmail.com')
mail.login('plexigebris@gmail.com','Gebris@10192029')

mail.select('inbox')

result, data = mail.uid('search', None, "ALL")
##print(data)

inbox_item_list = data[0].split()
##print(inbox_item_list)

most_recent = inbox_item_list[-1]
result, email_data = mail.uid('fetch', most_recent, '(RFC822)')
##print(email_data)

raw_email = email_data[0][1].decode('utf-8')
email_message = email.message_from_string(raw_email)

##print(f"Recepients: {email_message['To']\n}")
##print(f"Sender: {email_message['Sender']\n}")
##print(f"Subject: {email_message['Subject']\n}")
##print(f"Date: {email_message['Date']\n}")
##print(f"CC: {email_message['CC']\n}")

for part in email_message.walk():
  if part.get_content_type() == 'text/plain':
    body = part.get_payload(decode=True)
    save_string = str("" + "Content" + ".eml")
  else:
    continue

for part in email_message.walk():
  if part.get_content_maintype() == 'multipart':
    continue

  if part.get('Content-Disposition') is None:
    continue
  fileName = part.get_filename()
  if bool(fileName):
    filePath = os.path.join('/opt/ansi_sigtel/playbook05', fileName)
    if not os.path.isfile(filePath):
      fp = open(filePath, 'wb')
      fp.write(part.get_payload(decode=True))
      fp.close()
    subject = str(email_message).split("Subject: ", 1)[1].split("\nTos:", 1)[0]
