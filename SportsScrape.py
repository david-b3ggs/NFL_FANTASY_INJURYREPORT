from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

URL = "https://www.nfl.com/news/all-news"
headlines = []
keywords = ["injured, injury, out, starter"]

port = 465
login = "DavesEdgeBaby@gmail.com"
password = "Idaho11!"

sender = "DavesEdgeBaby@gmail.com"
receiver = "david_beggs@baylor.edu, grantswingler@gmail.com"

req = requests.get(URL)
soup = BeautifulSoup(req.content, "html5lib")
table = soup.find('h3', attrs = {'class': 'all_quotes'})

for row in table.findAll('h3', attrs = {'class': 'd3-o-media-object__title'}):
    quote ={}
    quote['Headline'] = row.h3.text
    URLString = str(quote['Headline']).replace(' ', '-')
    quote['URL'] = URL + "/" + URLString
    headLineWords = str(quote['Headline']).split()
    for i in headLineWords:
        if i in keywords:
            headlines.append(quote)
            break

message = MIMEMultipart("alternative")
message["Subject"] = "Fantasy Update"
message["To"] = receiver
message["From"] = sender
sendString = ""

for q in headlines:
    sendString += q["Headline"] + '\n' + q['URL'] + '\n\n'


text = f"""\
Here's your fantasy update for waiver lookup news (will update with backups later)
{sendString}
"""

html = f"""\
<html>
    <body>
        <h4>Here's your fantasy update for waiver lookup news (will update with backups later)<h4>
        <p>{sendString}</p>
    </body>
</html>
"""

part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

message.attach(part1)
message.attach(part2)

with smtplib.SMTP("smtp.gmail.com", port) as server:
    server.login(login, password)
    server.sendmail(
        sender, receiver, message.as_string()
    )

    # Should add log later
    print("Updates sent")