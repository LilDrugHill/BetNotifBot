import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json


LINK = "https://www.excapper.com/"
# fav, live, premach
TOPIC = 'fav'


def main_f(email, psw):
    html = get_html_with_matches(LINK, email, psw)

    new_ids = parse_html(html)

    with open('games_id.json') as f:
        old_ids = json.load(f)['games_id']

    if not set(new_ids).issubset(old_ids):
        alert = True
        with open('games_id.json', 'w') as f:
            json.dump({'games_id': new_ids}, f)
    else:
        alert = False
    print(new_ids)
    print(old_ids)
    print(alert)
    return alert


def get_html_with_matches(link, email, psw):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x935')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url=link)

    driver.find_element(by=By.XPATH, value="/html/body/div[1]/div/div[2]/a").click()

    driver.find_element(by=By.NAME, value="email").send_keys(email)
    driver.find_element(by=By.NAME, value="psw").send_keys(psw)

    driver.find_element(by=By.XPATH, value="/html/body/div[1]/div/div[2]/div/div/div[1]/form/input[2]").click()

    time.sleep(2)

    html = driver.page_source

    driver.quit()

    return html


def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    matches_block = soup.find_all('div', id=TOPIC)
    matches_list = matches_block[0].table
    matches_notes = matches_list.find_all('tr', class_='a_link')
    return [int((matches_note.get('game_id'))) for matches_note in matches_notes]
