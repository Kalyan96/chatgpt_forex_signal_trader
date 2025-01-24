import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import yagmail

yag = yagmail.SMTP('rootkalyan2@gmail.com', '@Bcde12345')
yag.send('rootkalyan@gmail.com', 'subject', 'This is the body of the message.')


# setup the parameters of the message
password = "@Bcde12345"
msg = MIMEMultipart()
msg['From'] = "rootkalyan2@gmail.com"
msg['To'] = "rootkalyan@gmail.com"
msg['Subject'] = "TTD website changed ! "

# add in the message body
message = "---"
msg.attach(MIMEText(message, 'plain'))

# create server
server = smtplib.SMTP('smtp.gmail.com: 587')

server.starttls()

# Login Credentials for sending the mail
server.login(msg['From'], password)

# send the message via the server
server.sendmail(msg['From'], msg['To'], msg.as_string())

server.quit()

print("successfully sent email to %s:" % (msg['To']))
