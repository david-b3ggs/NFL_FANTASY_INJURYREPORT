from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

URL = "https://www.nfl.com/injuries"
link = "https://www.nfl.com"
headlines = []

port = 465
login = "email"
password = r"password"

sender = "email"
receiver = "email, list"

req = requests.get(URL)
soup = BeautifulSoup(req.content, "html5lib")
table = soup.findAll('h3')

client = pymongo.MongoClient(<link>)
db = client.Injuries

InjuryReports = db.InjuryReports

for row in table:
    quote ={}
    rStr = str(row).split('\n')[1].lstrip().rstrip()
    report = InjuryReports.find_one({'Headline': rStr})


    if not report:
        quote['Headline'] = rStr
        quote['URL'] = link + row.parent.attrs['href']
        headlines.append(quote)
        result = InjuryReports.insert_one(quote)

if len(headlines) != 0:
    message = MIMEMultipart("alternative")
    message["Subject"] = "Fantasy Update"
    message["To"] = receiver
    message["From"] = sender
    sendString = ""

    for q in headlines:
        sendString += "<p>" + q["Headline"] + '\n' + q['URL'] + "</p>" + '\n'

    text = f("""\
    Here's your fantasy update for waiver lookup news (will update with backups later)
    {sendString}
   """)

    html = f("""\
    \<html>
        <body>
            <h4>Here's your fantasy update for waiver lookup news (will update with backups later)<h4>
            {sendString}
        </body>
    </html>
    """)

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    with smtplib.SMTP_SSL("smtp.gmail.com", port) as server:
        server.login(login, password)
        server.sendmail(
            sender, receiver, message.as_string()
        )
        server.close()

    # Should add log later
    print("Updates sent")
else:
    print("Nothing new to report")
