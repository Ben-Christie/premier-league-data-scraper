from selenium import webdriver
from selenium.webdriver.common.by import By
from data import urls, exclude_keywords
from helper import add_player_to_dict, clean_data_points, integer_conversion
import csv
import os


# Create a single webdriver instance
driver = webdriver.Chrome()

players = {}

# loop through all urls one-by-one
for url in urls:
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
                add_player_to_dict(player_name, club, players)

                if player_name not in seenAttributes:
                    seenAttributes[player_name] = set()

                # get the players individual player dictionary
                player = players[player_name]
                player_attributes = seenAttributes[player_name]

                # get the cells/data points from the row
                cells = row.find_elements(By.XPATH, './/td')

                # loop through all the cells/data points one-by-one
                for cell in cells:
                    attribute_name = cell.get_attribute("data-stat")
                    attribute_value = cell.text.strip()

                    # Check if the attribute should be excluded based on keywords or has been processed already
                    if any(keyword in attribute_name for keyword in exclude_keywords) or attribute_value == "" or attribute_name in seenAttributes[player_name]:
                        continue

                    # clean data points
                    attribute_name, attribute_value = clean_data_points(
                        attribute_name, attribute_value)

                    # try to convert to int if possible
                    attribute_value = integer_conversion(attribute_value)

                    # remove players if they haven't played a game
                    if attribute_name == 'games' and attribute_value < 1:
                        players.pop(player_name)
                        break

                    if attribute_name == 'games' and 'games' in player and attribute_value > player['games']:
                        player['club'] = club

                    if attribute_name in player and isinstance(attribute_value, int):
                        player[attribute_name] += attribute_value
                    else:
                        player[attribute_name] = attribute_value

                    seenAttributes[player_name].add(attribute_name)


# Close the webdriver instance
driver.quit()

# split into csv based on player position
positions_csv = {
    'Goalkeeper': 'goalkeeper.csv',
    'Defender': 'defender.csv',
    'Midfielder': 'midfielder.csv',
    'Forward': 'forward.csv'
}

# initialise dicts to store players by position
players_by_position = {
    position: [] for position in positions_csv.keys()
}

# categorise players by position
for _, player_data in players.items():
    position = player_data['position']
    players_by_position[position].append(player_data)

# Get the path to the Downloads directory
downloads_directory = os.path.join(os.path.expanduser('~'), 'Downloads')

# Create a new folder for the CSV files
output_directory = os.path.join(downloads_directory, 'pl_player_data')

# Ensure the directory exists; if not, create it
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# write players by position to csv
for position, players_list in players_by_position.items():
    csv_filename = positions_csv[position]

    csv_path = os.path.join(output_directory, 'pl_' + csv_filename)

    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = players_list[0].keys() if players_list else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for player in players_list:
            writer.writerow(player)
