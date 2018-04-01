import smtplib
import time
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import datetime
import requests


def sendMail(title, price, description, city, link, date, photoLink):
    date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y")
    gmailUser = 'marktplaats.bot@gmail.com'
    gmailPassword = 'joost111'

    sentFrom = gmailUser
    to = 'marktplaats.bot@gmail.com'

    msg = MIMEMultipart()
    msg['Subject'] = 'Nieuwe marktplaats advertentie'
    msg['From'] = sentFrom
    msg['To'] = to
    body = ('Nieuw product met titel: "' + title +
            '" \n\n Deze kost: ' + str(price).replace('.', ',') +
            '\n\nDe beschrijving is: "' + description +
            '"\n\n De persoon woont in: ' + city +
            '\n\n De link is: ' + link + '\n\n Deze staat er sinds '
            + date + ' op')
    html = ('<html><head></head><body><br>Nieuw product met titel: "' + title +
            '" <br><br> Deze kost: ' + str(price).replace('.', ',') +
            '<br><br>De beschrijving is: "' + description +
            '"<br><br> De persoon woont in: ' + city +
            '<br><br> De link is: <a href="' + link + '">' + link +
            '</a><br><br> Deze staat er sinds '
            + date + ' op</body></html>')
    f = requests.get(photoLink)
    img = MIMEImage(f.content)
    msg.attach(img)
    msg.attach(MIMEText(html, 'html', 'utf-8'))
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmailUser, gmailPassword)
        server.sendmail(sentFrom, to, msg.as_string().encode('ascii'))
        server.close()
        print('Sent email')
    except:
        raise
        print('Something went wrong..')
