import os, requests
from datetime import datetime, date
from bs4 import BeautifulSoup

def get_draws_by_year(year: int) -> list:
    url = os.getenv("EUROMILLIONS_WEB_BASE_URL") + f'/results-history-{year}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    page = requests.get(url, headers=headers)

    if page.status_code == 403:
        print(f"❌ Erreur 403 : Accès refusé à {url}. Essaye un VPN ou utilise Selenium.")
        return []

    html = BeautifulSoup(page.content, 'html.parser')

    content = html.find(id='content')
    if content is None:
        print(f"⚠️ Aucun 'content' trouvé pour {year}. La structure HTML a peut-être changé.")
        return []

    draws = content.find('tbody').find_all('tr', class_='resultRow')
    draws.reverse()  # Trier les résultats par ordre croissant

    return draws

def get_latest_draws() -> list:
    url = os.getenv("EUROMILLIONS_WEB_BASE_URL") + '/results'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }

    page = requests.get(url, headers=headers)

    if page.status_code != 200:
        print(f"❌ Erreur {page.status_code} en récupérant les derniers tirages")
        return []

    html = BeautifulSoup(page.content, 'html.parser')

    draws = html.find(id='content')

    if draws is None:
        print("⚠️ Aucun 'content' trouvé. La structure HTML a changé ?")
        return []

    return draws


def get_date(details_route: str) -> date:
    date_str = details_route.split('/')[2]
    parsed_date = datetime.strptime(date_str, '%d-%m-%Y')

    return parsed_date.date()

def get_numbers(html) -> list:
    numbers = []
    balls = html.find_all('li', class_='ball')
    if balls[0].text == '-':
        return numbers

    for ball in balls: numbers.append(int(ball.text))

    return numbers

def get_stars(html) -> list:
    stars = []
    balls_star = html.find_all('li', class_='lucky-star')
    if balls_star[0].text == '-':
        return stars

    for ball_star in balls_star: stars.append(int(ball_star.text))

    return stars

def get_details(details_route: str) -> list:
    url = os.getenv("EUROMILLIONS_WEB_BASE_URL") + details_route
    page = requests.get(url)

    html = BeautifulSoup(page.content, 'html.parser')

    prizes = []
    has_winner = False

    body = html.find(id="PrizePT")
    body = body if body is not None else html.find(id="PrizeES")
    if body is None:
        return [prizes, has_winner]

    rows = body.find('tbody').find_all('tr')
    if len(rows) == 0:
        return [prizes, has_winner]

    for row in rows:
        if row.find('td').text.replace(' ', '').strip() == 'Totals':
            continue

        prize = {
            "prize": 0,
            "winners": 0,
            "combination": ""
        }

        columns = row.find_all('td')
        for column in columns:
            if column['data-title'] == 'Numbers Matched':
                value = column.text.replace(' ', '').strip()
                if len(value) == 1:
                    value = f"{value}+0"
                prize['combination'] = value
            elif column['data-title'] == 'Prize Per Winner':
                prize['prize'] = float(column.text.replace(',', '').replace('€', '').strip())
            elif column['data-title'] == 'Total Winners':
                prize['winners'] = column.text.replace(',', '').replace('Rollover! ', '').replace('Rolldown! ', '').strip()

        if prize['combination'] == "5+2" and int(prize['winners']) > 0:
            has_winner = True

        prizes.append(prize)

    return [prizes, has_winner]


def get_statistics(db):
    stats = db.get_statistics()
    return [
        {"number": row["number"], "frequency": row["frequency"], "type": row["type"]}
        for row in stats
    ]

def get_predictions(db):
    return db.get_predictions()
