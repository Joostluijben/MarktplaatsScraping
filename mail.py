import smtplib
import time
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText

def sendMail(title,price,description, city, link, date):
    gmailUser = 'joost.luijben@gmail.com'
    gmailPassword = 'joostyoshi'

    sentFrom = gmailUser
    to = 'joost.luijben@gmail.com'

    msg = MIMEMultipart()
    msg['Subject'] = 'Nieuwe marktplaats advertentie'
    msg['From'] = sentFrom
    msg['To'] = to
    body =  ('Nieuw product met titel: "' + title +
            '" \n\n Deze kost: ' + str(price).replace('.', ',') +
            '\n\nDe beschrijving is: "' + description +'"\n\n De persoon woont in: ' + city +
            '\n\n De link is: ' + link + '\n\n Deze staat er sinds ' + date + ' op')
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmailUser, gmailPassword)
        server.sendmail(sentFrom, to, msg.as_string().encode('ascii'))
        server.close()
        print('Sent email')
    except:
        print('Something went wrong..')
