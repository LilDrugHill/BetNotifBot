import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json
import asyncio


LINK = "https://www.excapper.com/"
TOPIC = "fav"


async def main_f(email, psw):
    html = await get_html_with_matches(LINK, email, psw)

    new_ids = set(await parse_html(html))

    with open("games_id.json") as f:
        j = json.load(f)
        old_ids = set(j["games_id"])
        notif_id = set(j["notified_id"])

    if not new_ids.issubset(old_ids):

        new_matches = old_ids ^ new_ids ^ notif_id
        alert = True, new_matches

        with open("games_id.json", "w") as f:
            if notif_id == {}:
                json.dump({"games_id": list(new_ids), "notified_id": list(new_matches)}, f)
            else:
                json.dump({"games_id": list(new_ids), "notified_id": list(notif_id.union(new_matches))}, f)
    else:
        _ = 0
        alert = False, _

    return alert


async def get_html_with_matches(link, email, psw):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("detach", True)
    options.add_argument("--disable-logging")
    options.add_argument("window-size=1920x935")
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url=link)

    driver.find_element(by=By.XPATH, value="/html/body/div[1]/div/div[2]/a").click()

    driver.find_element(by=By.NAME, value="email").send_keys(email)
    driver.find_element(by=By.NAME, value="psw").send_keys(psw)

    driver.find_element(
        by=By.XPATH, value="/html/body/div[1]/div/div[2]/div/div/div[1]/form/input[2]"
    ).click()

    await asyncio.sleep(2)

    html = driver.page_source

    driver.quit()

    return html


async def parse_html(html):
    soup = BeautifulSoup(html, "lxml")
    matches_block = soup.find_all("div", id=TOPIC)
    matches_list = matches_block[0].table
    matches_notes = matches_list.find_all("td", class_="a_link hide")
    return [matches_note.get("game_id") for matches_note in matches_notes[1:]]
