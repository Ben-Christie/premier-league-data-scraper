from selenium.webdriver.common.by import By
from data import fbref_urls, fbref_exclude_keywords
from helper import add_player_to_dict, clean_fbref_data_points, integer_conversion


def fbref(players, driver):

    # loop through all fbref urls one-by-one
    for url in fbref_urls:
        driver.get(url)
        driver.implicitly_wait(10)

        title_element = driver.find_element(By.XPATH, './/h1/span')
        title = title_element.text.strip().split()

        # get club name from the title of the page
        club = " ".join(title[1:len(title) - 1])

        # contains the processed attributes for each player
        seenAttributes = {}

        # get all the tables from the page and store as team data
        tables = driver.find_elements(By.TAG_NAME, 'table')

        # loop through all the tables one-by-one
        for table in tables:
            rows = table.find_elements(By.XPATH, './/tbody/tr')

            # loop through all the rows one-by-one (each row == player)
            for row in rows:
                # verify the data in the row, and get the name of the player
                if 'data-row' in row.get_attribute('outerHTML'):
                    th_element = row.find_element(By.TAG_NAME, 'th')
                    player_name = th_element.text.strip()

                    # skip over rows if the name is not an actual player
                    if not player_name or any(char.isdigit() for char in player_name) or player_name in ['Player', 'Date']:
                        continue

                    # add new player to the list of players
                    surname = add_player_to_dict(player_name, club, players)

                    if surname not in seenAttributes:
                        seenAttributes[surname] = set()

                    # get the players individual player dictionary
                    player = players[surname]
                    player_attributes = seenAttributes[surname]

                    # get the cells/data points from the row
                    cells = row.find_elements(By.XPATH, './/td')

                    # loop through all the cells/data points one-by-one
                    for cell in cells:
                        attribute_name = cell.get_attribute("data-stat")
                        attribute_value = cell.text.strip()

                        # Check if the attribute should be excluded based on keywords or has been processed already
                        if any(keyword in attribute_name for keyword in fbref_exclude_keywords) or attribute_value == "" or attribute_name in seenAttributes[surname]:
                            continue

                        # clean data points
                        attribute_name, attribute_value = clean_fbref_data_points(
                            attribute_name, attribute_value)

                        # try to convert to int if possible
                        attribute_value = integer_conversion(attribute_value)

                        # remove players if they haven't played a game
                        if attribute_name == 'games' and attribute_value < 1:
                            players.pop(surname)
                            break

                        if attribute_name == 'games' and 'games' in player and attribute_value > player['games']:
                            player['club'] = club

                        if attribute_name in player and isinstance(attribute_value, int):
                            player[attribute_name] += attribute_value
                        else:
                            player[attribute_name] = attribute_value

                        seenAttributes[surname].add(attribute_name)
