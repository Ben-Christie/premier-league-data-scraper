from selenium import webdriver
from selenium.webdriver.common.by import By
from unidecode import unidecode
from data import urls, nations, positions
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

    # holds the encountered attributes for each player at the club, so we don't duplicate data
    seenAttributes = {}

    # get all the tables from the page and store as team data
    team_data = driver.find_elements(By.TAG_NAME, 'table')

    # loop through all the tables one-by-one
    for table in team_data:
        rows = table.find_elements(By.XPATH, './/tbody/tr')

        # loop through all the rows one-by-one (each row == player)
        for row in rows:
            # verify the data in the row, and get the name of the player
            if 'data-row' in row.get_attribute('outerHTML'):
                th_element = row.find_element(By.TAG_NAME, 'th')
                full_player_name = th_element.text.strip()

                # skip over rows if the name is not an actual player
                if not full_player_name or any(char.isdigit() for char in full_player_name) or full_player_name in ['Player', 'Date']:
                    continue

                # if the player has not been seen before, add it to the players dictionary
                if full_player_name not in players:
                    players[full_player_name] = {
                        # assign the player name and use unidecode to remove accents
                        'full_name': unidecode(full_player_name),
                        'club': club,
                    }

                    # create an entry for the player if it doesn't exist
                    seenAttributes[full_player_name] = set()

                # get the players individual player dictionary
                player = players[full_player_name]

                # get the cells/data points from the row
                cells = row.find_elements(By.XPATH, './/td')

                # exclude data points containing these titles
                exclude_keywords = ["90", "pct", "gca", "per", "x", "sca",
                                    "plus", "matches", "games_complete", "average_shot_distance", "goals_assists", "goals_pens", 'tackles_interceptions', 'cards_yellow_red', 'gk_games', 'gk_games_starts', 'gk_minutes', 'gk_goals_against', 'gk_wins', 'gk_ties', 'gk_losses', 'gk_avg_distance_def_actions']

                # loop through all the cells/data points one-by-one
                for cell in cells:
                    attribute_name = cell.get_attribute("data-stat")
                    attribute_value = cell.text.strip()

                    # Check if the attribute should be excluded based on keywords
                    if any(keyword in attribute_name for keyword in exclude_keywords) or attribute_value == "" or attribute_name in seenAttributes[full_player_name]:
                        continue

                    # Add the attribute name to seenAttributes for this player
                    seenAttributes[full_player_name].add(attribute_name)

                    # Custom processing for certain attributes (e.g., nationality, age)
                    if 'nationality' in attribute_name:
                        attribute_name = 'nation'
                        parts = attribute_value.split()
                        if parts and len(parts) == 2:
                            attribute_value = nations[parts[1]]
                    elif 'age' in attribute_name:
                        parts = attribute_value.split('-')
                        if parts:
                            attribute_value = parts[0]
                    elif 'position' in attribute_name:
                        parts = attribute_value.split(',')
                        if parts:
                            attribute_value = positions[parts[0]]
                    elif 'minutes' in attribute_name:
                        attribute_value = attribute_value.replace(',', '')

                    # try to convert to int if possible
                    try:
                        attribute_value = int(attribute_value)
                    except ValueError:
                        pass

                    # remove players if they haven't played a game
                    if attribute_name == 'games' and attribute_value < 1:
                        players.pop(full_player_name)
                        break
                    elif attribute_name == 'games' and 'games' in player and attribute_value > player['games']:
                        player['club'] = club

                    if attribute_name in player:
                        player[attribute_name] += attribute_value
                    else:
                        player[attribute_name] = attribute_value

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
