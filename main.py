from selenium import webdriver
from selenium.webdriver.common.by import By
from unidecode import unidecode
from data import urls, nations, positions
import csv
import os

# Create a single webdriver instance
driver = webdriver.Chrome()

players = {}

for url in urls:
    driver.get(url)
    driver.implicitly_wait(10)

    title_element = driver.find_element(By.XPATH, './/h1/span')
    title = title_element.text.strip().split()

    club = " ".join(title[1:len(title) - 1])

    team_data = driver.find_elements(By.TAG_NAME, 'table')

    for table in team_data:
        rows = table.find_elements(By.XPATH, './/tbody/tr')

        for row in rows:
            if 'data-row' in row.get_attribute('outerHTML'):
                th_element = row.find_element(By.TAG_NAME, 'th')
                full_player_name = th_element.text.strip()

                if not full_player_name or any(char.isdigit() for char in full_player_name) or full_player_name in ['Player', 'Date']:
                    continue

                if full_player_name not in players:
                    players[full_player_name] = {
                        'full_name': unidecode(full_player_name)}

                player = players[full_player_name]

                player['club'] = club

                cells = row.find_elements(By.XPATH, './/td')

                exclude_keywords = ["90", "pct", "gca", "per", "x", "sca",
                                    "plus", "matches", "games_complete", "average_shot_distance", "goals_assists", "goals_pens", 'tackles_interceptions', 'cards_yellow_red', 'gk_games', 'gk_games_starts', 'gk_minutes', 'gk_goals_against', 'gk_wins', 'gk_ties', 'gk_losses', 'gk_avg_distance_def_actions']

                for cell in cells:
                    attribute_name = cell.get_attribute("data-stat")
                    attribute_value = cell.text.strip()

                    # Check if the attribute should be excluded based on keywords
                    if any(keyword in attribute_name for keyword in exclude_keywords) or attribute_value == "":
                        continue

                    # Custom processing for certain attributes (e.g., nationality, age)
                    if "nationality" in attribute_name:
                        attribute_name = 'nation'
                        parts = attribute_value.split()
                        if parts and len(parts) == 2:
                            attribute_value = nations[parts[1]]
                    elif "age" in attribute_name:
                        parts = attribute_value.split('-')
                        if parts:
                            attribute_value = parts[0]
                    elif "position" in attribute_name:
                        parts = attribute_value.split(',')
                        if parts:
                            attribute_value = positions[parts[0]]

                    try:
                        attribute_value = int(attribute_value)
                    except ValueError:
                        pass

                    # remove players if they haven't played a game
                    if attribute_name == 'games' and attribute_value < 1:
                        players.pop(full_player_name)
                        break

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
