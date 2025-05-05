from selenium.webdriver.common.by import By
from data import sofifa_urls
from unidecode import unidecode
from helper import integer_conversion, fuzzy_match_players


def sofifa(players, driver):
    # loop through all sofifa urls one by one
    for url in sofifa_urls:
        driver.get(url)
        driver.implicitly_wait(10)

        club = (driver.find_element(By.XPATH, './/h1')).text

        # get all the tables from the page and store as tables
        tables = driver.find_elements(By.TAG_NAME, 'table')

        for table in tables:
            # loop through all the rows one-by-one (each row == player)
            rows = table.find_elements(By.XPATH, './/tbody/tr')

            for row in rows:
                name = unidecode(row.find_element(
                    By.XPATH, './/td[2]/a').get_attribute('innerText'))
                overall = row.find_element(
                    By.XPATH, './/td[4]/em').get_attribute('innerText')
                potential = row.find_element(
                    By.XPATH, './/td[5]/em').get_attribute('innerText')

                # locate the right spot for the data to be appended to
                players_key = fuzzy_match_players(name, players)

                if players_key != "no match" and players_key in players and players[players_key]['club'] == club:
                    players[players_key]['overall'] = integer_conversion(
                        overall)
                    players[players_key]['potential'] = integer_conversion(
                        potential)
