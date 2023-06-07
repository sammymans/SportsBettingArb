from bs4 import BeautifulSoup
import requests
from collections import defaultdict
from datetime import datetime
import json
import pandas as pd

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import random


url = 'https://www.covers.com/sport/baseball/mlb/odds'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')


today_date = datetime.today().date()
data = defaultdict(lambda: defaultdict(list))

# 1. get games
tbody = soup.find('tbody', class_='games-tbody')
for tr in tbody.find_all('tr'):
    date = tr.find('div', class_="__date").text.strip().split(',')[0]
    print(date)
    if date == "Today":
        away_element = tr.find('div', class_='__away')
        away_text = away_element.get_text(strip=True)
        split_text = away_text.split("(", 1)
        away_text = split_text[0].strip()
        print('Away:', away_text)

        home_element = tr.find('div', class_='__home')
        home_text = home_element.get_text(strip=True)
        split_text = home_text.split("(", 1)
        home_text = split_text[0].strip()
        print('Home:', home_text)
    else:
        break

    data[(away_text, home_text)] = {}

    print('---')

print(data)

# 2. get odds

mapped = {}
count = 0
for key in data:
    mapped[count] = key
    count += 1

tbody = soup.find('tbody', class_='odds-tbody')
count = 0
bookies = set()
for tr in tbody.find_all('tr', class_='covers-CoversOdds-mainTR oddsGameRow'):
    if count == len(mapped):
        break
    odds = {}
    for td in tr.find_all('td'):
        book = td['data-book']
        bookies.add(book)
        odd = td.find('div', class_ = '__bookOdds covers-Covers-Odds-withNoBorder')

        if odd:
            home_odds = odd.find('div', class_=lambda value: value and '__homeOdds' in value).find('div', class_='Decimal __decimal').text
            away_odds = odd.find('div', class_=lambda value: value and '__awayOdds' in value).find('div', class_='Decimal __decimal').text
        else:
            home_odds = 0
            away_odds = 0
            
        print('Away:', away_odds)
        print('Home:', home_odds)

        odds[book] = [away_odds, home_odds]

        print('---')

    data[mapped[count]] = odds
    count += 1

# 3. find opps

def ip(o1, o2):
    return (1/o1 + 1/o2)

result = []
# [ip, game, bookie1, team, amt + bookie2, team, amt]

stake = 100

for game, bookies in data.items():
    bookie_list = list(bookies.keys())
    for i in range(len(bookie_list)):
        for j in range(i + 1, len(bookie_list)):
            bookie1 = bookie_list[i]
            bookie2 = bookie_list[j]
            home_odds_bookie1 = float(data[game][bookie1][1])
            away_odds_bookie1 = float(data[game][bookie1][0])
            home_odds_bookie2 = float(data[game][bookie2][1])
            away_odds_bookie2 = float(data[game][bookie2][0])

            if home_odds_bookie1 == 0 or away_odds_bookie1 == 0 or home_odds_bookie2 == 0 or away_odds_bookie2 == 0: continue

            val1 = ip(home_odds_bookie1, away_odds_bookie2)
            val2 = ip(home_odds_bookie2, away_odds_bookie1)

            if val1 < 1.0:
                if home_odds_bookie1 < away_odds_bookie2:
                    other_bet = stake * home_odds_bookie1 / away_odds_bookie2
                    result.append([val1, game, bookie1, game[1], max(stake, other_bet), bookie2, game[0], min(stake, other_bet)])
                else:
                    other_bet = stake * away_odds_bookie2 / home_odds_bookie1
                    result.append([val1, game, bookie1, game[1], min(stake, other_bet), bookie2, game[0], max(stake, other_bet)])
            if val2 < 1.0:
                if home_odds_bookie2 < away_odds_bookie1:
                    other_bet = stake * home_odds_bookie2 / away_odds_bookie1
                    result.append([val2, game, bookie1, game[0], max(stake, other_bet), bookie2, game[1], min(stake, other_bet)])
                else:
                    other_bet = stake * away_odds_bookie2 / home_odds_bookie1
                    result.append([val2, game, bookie1, game[0], min(stake, other_bet), bookie2, game[1], max(stake, other_bet)])

for i in range(len(result)):
    t1, t2 = result[i][1]
    result[i][1] = t1 + ' vs. ' + t2

result.sort()
print(result)

df = pd.DataFrame(result, columns=['implied probaility', 'game name', 'bookkeeper 1', 'team 1', 'bet amount', 'bookkeeper 2', 'team 2', 'bet amount'])
df.to_excel(f"{today_date} - for benny.xlsx", index=False)

subject_headers = ["Betting Bonanza: Where Luck Meets Logic",
"Laughing All the Way to the Bank: Funny Betting Opportunities Inside",
"Arbitrage Alert: Money, Memes, and Mischief",
"Betting Funnies: Laughing Your Way to Profit",
"Jokes on the Bookies: Hilarious Arbitrage Opportunities",
"Tickle Your Funny Bone and Your Wallet: Arbitrage Time!",
"Funny Business: Betting Your Way to a Chuckle and a Profit",
"Arbitrage Laughs: Smiling All the Way to the Bank",
"Chuckles and Cash: Hottest Betting Opportunities",
"Betting Bloopers: Laughing at the Bookies' Expense",
"Wager Wizards: A Comedy of Betting Skills",
"Mirthful Money: Unveiling Betting Arbitrage Chuckles",
"Laughable Lines: Betting Opportunities That'll Crack You Up",
"Hilarious High Stakes: Where Betting and Comedy Collide",
"Betting Blunders: Making Profits and Poking Fun at the Odds",
"Funny Money: Discovering the Playful Side of Betting",
"The Humor of High Odds: Where Bets Meet Belly Laughs",
"Arbitrage Antics: Comical Opportunities You Won't Believe",
"Jestful Jackpots: Uncovering Betting's Funniest Moments",
"Betting Banter: Laughing Your Way to Winning Bets",
"Comic Cash: Unraveling the Funny Side of Betting",
"Risky Business: Hilarity and High Profits Await",
"Betting Chuckles: A Side-Splitting Path to Extra Cash",
"Witty Wagers: Unveiling the Humorous World of Betting",
"Money and Merriment: Betting Opportunities That Amuse",
"Giggles and Gambles: Hottest Laughs in the Betting Scene",
"Arbitrage Adventures: A Funny Journey to Winning Bets",
"Laugh Out Loud: Betting Opportunities to Crack You Up",
"The Comedy of Betting: Jokes, Wagers, and Wins",
"Rolling in Laughter, Rolling in Cash: Funny Betting Moments",
"BET ON THIS ONE FAGGOTS",]

# 4. send email
sender_email = 'sfarnum1132@gmail.com'
password = 'ptsmxddykanlzwgh'
subject_string = random.choice(subject_headers)
subject = f"{subject_string}: {today_date}"
recipients = ['sfarnum1132@gmail.com', 'rohansaxena1738@gmail.com', 'schneeweissbenjamin@gmail.com']
attachment_file_name = f"{today_date} - for benny.xlsx"

def send_email(sender_email, password, recipient, attachment_file_name, subject):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject

    binary_excel = open(attachment_file_name, 'rb')

    payload = MIMEBase('application', 'vnd.ms-excel', Name=os.path.basename(attachment_file_name))

    payload.set_payload(binary_excel.read())
    binary_excel.close()

    encoders.encode_base64(payload)

    payload.add_header('Content-Disposition', 'attachment', filename=attachment_file_name)
    msg.attach(payload)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:

        server.ehlo()  # Can be omitted
        server.starttls()
        server.ehlo()  # Can be omitted

        server.login(sender_email, password)
        server.sendmail(sender_email, recipient, msg.as_string())


if result == []:
    print('no arb opps')
else:
    cnt = 0
    for rec in recipients:
        cnt += 1
        send_email(sender_email, password, rec, attachment_file_name, subject)
        print(str(cnt) + 'email sent successfully')