from selenium import webdriver
from selenium.webdriver.common.by import By

# URL of the webpage
urls = [
    "https://fbref.com/en/squads/18bb7c10/Arsenal-Stats",
    "https://fbref.com/en/squads/8602292d/Aston-Villa-Stats",
    "https://fbref.com/en/squads/4ba7cbea/Bournemouth-Stats",
    "https://fbref.com/en/squads/cd051869/Brentford-Stats",
    "https://fbref.com/en/squads/d07537b9/Brighton-and-Hove-Albion-Stats",
    "https://fbref.com/en/squads/943e8050/Burnley-Stats",
    "https://fbref.com/en/squads/cff3d9bb/Chelsea-Stats",
    "https://fbref.com/en/squads/47c64c55/Crystal-Palace-Stats",
    "https://fbref.com/en/squads/d3fd31cc/Everton-Stats",
    "https://fbref.com/en/squads/fd962109/Fulham-Stats",
    "https://fbref.com/en/squads/822bd0ba/Liverpool-Stats",
    "https://fbref.com/en/squads/e297cd13/Luton-Town-Stats",
    "https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats",
    "https://fbref.com/en/squads/19538871/Manchester-United-Stats",
    "https://fbref.com/en/squads/b2b47a98/Newcastle-United-Stats",
    "https://fbref.com/en/squads/e4a775cb/Nottingham-Forest-Stats",
    "https://fbref.com/en/squads/1df6b87e/Sheffield-United-Stats",
    "https://fbref.com/en/squads/361ca564/Tottenham-Hotspur-Stats",
    "https://fbref.com/en/squads/7c21e445/West-Ham-United-Stats",
    "https://fbref.com/en/squads/8cec06e1/Wolverhampton-Wanderers-Stats"
]

players = {}

for url in urls:
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get(url)

    team_data = driver.find_elements(By.TAG_NAME, 'table')

    # Loop through each WebElement and extract player data
    for table in team_data:
        rows = table.find_elements(By.XPATH, './/tbody/tr')

        for row in rows:
            th_element = row.find_element(By.XPATH, './/th')
            full_player_name = th_element.text

            if not full_player_name or any(char.isdigit() for char in full_player_name):
                continue

            if full_player_name not in players:
                player = {"full_name": full_player_name}
                players[full_player_name] = player

            cells = row.find_elements(By.XPATH, './/td')

            exclude_keywords = ["90", "pct", "gca",
                                "per", "x", "sca", "plus", "matches", "games_complete", "average_shot_distance"]

            for cell in cells:
                attribute_name = cell.get_attribute("data-stat")
                attribute_value = cell.text

                if not any(keyword in attribute_name for keyword in exclude_keywords) and not attribute_value == "":
                    if "nationality" in attribute_name:
                        parts = attribute_value.split()
                        if parts:
                            attribute_value = parts[-1]
                    elif "age" in attribute_name:
                        parts = attribute_value.split('-')
                        if parts:
                            attribute_value = parts[0]

                    try:
                        attribute_value = float(attribute_value)
                    except ValueError:
                        pass

                    players[full_player_name][attribute_name] = attribute_value

    driver.quit()

    # Filter out dictionaries with empty full_name or containing numbers
    filtered_players = {name: data for name, data in players.items(
    ) if name and not any(char.isdigit() for char in name)}

    # Print the list of filtered player dictionaries
    for player_name, player_data in filtered_players.items():
        print(player_data)
        print('\n')
