from selenium import webdriver
from selenium.webdriver.common.by import By

# Create a single webdriver instance
driver = webdriver.Chrome()

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

# Mapping of attribute names to sub-dictionaries
attribute_mapping = {
    # attacking stats
    'attacking_actions': ['goals', 'assists', 'progressive_carries', 'shots_on_target', 'assisted_shots', 'through_balls', 'take_ons', 'take_ons_won', 'take_ons_tackled', 'on_goals_for', 'shots'],
    # defensive stats
    'defensive_actions': ['tackles', 'tackles_won', 'tackles_def_3rd', 'tackles_mid_3rd', 'tackles_att_3rd', 'challenge_tackles', 'challenges', 'challenges_lost', 'blocks', 'blocked_shots', 'blocked_passes', 'interceptions', 'clearances', 'on_goals_against', 'ball_recoveries', 'aerials_won', 'aerials_lost'],
    # set piece stats
    'set_pieces': ['pens_made', 'pens_att', 'pens_won', 'pens_conceded', 'shots_free_kicks', 'passes_free_kicks', 'throw_ins', 'corner_kicks', 'corner_kicks_in', 'corner_kicks_out', 'corner_kicks_straight', 'fouled'],
    # mistake stats
    'mistakes': ['cards_yellow', 'cards_red', 'errors', 'miscontrols', 'dispossessed', 'offsides', 'fouls', 'own_goals'],
    # passing stats
    'passing': ['passes', 'progressive_passes', 'progressive_passes_received', 'passes_completed', 'passes_total_distance', 'passes_progressive_distance', 'passes_completed_short', 'passes_short', 'passes_completed_medium', 'passes_medium', 'passes_completed_long', 'passes_long', 'passes_into_final_third', 'passes_into_penalty_area', 'crosses_into_penalty_area', 'passes_live', 'passes_dead', 'passes_switches', 'crosses', 'passes_offside', 'passes_blocked', 'passes_received', 'passes_offsides'],
    # possession stats
    'possession': ['touches', 'touches_def_pen_area', 'touches_def_3rd', 'touches_mid_3rd', 'touches_att_3rd', 'touches_att_pen_area', 'touches_live_ball', 'carries', 'carries_distance', 'carries_progressive_distance', 'carries_into_final_third', 'carries_into_penalty_area'],
    # goalkeeping stats
    'goalkeeping': ['gk_shots_on_target_against', 'gk_saves', 'gk_clean_sheets', 'gk_pens_att', 'gk_pens_allowed', 'gk_pens_saved', 'gk_pens_missed', 'gk_free_kick_goals_against', 'gk_corner_kick_goals_against', 'gk_own_goals_against', 'gk_passes_completed_launched', 'gk_passes_launched', 'gk_passes', 'gk_passes_throws', 'gk_passes_length_avg', 'gk_goal_kicks', 'gk_goal_kicks_length_avg', 'gk_crosses', 'gk_crosses_stopped', 'gk_def_actions_outside_pen_area', 'gk_goal_kick_length_avg']
}

for url in urls:
    driver.get(url)
    driver.implicitly_wait(10)

    team_data = driver.find_elements(By.TAG_NAME, 'table')

    for table in team_data:
        rows = table.find_elements(By.XPATH, './/tbody/tr')

        for row in rows:
            th_element = row.find_element(By.XPATH, './/th')
            full_player_name = th_element.text.strip()

            if not full_player_name or any(char.isdigit() for char in full_player_name):
                continue

            if full_player_name not in players:
                players[full_player_name] = {'full_name': full_player_name}

            player = players[full_player_name]

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

                # Check if the attribute belongs to any sub-dictionary
                for sub_dict, attributes in attribute_mapping.items():
                    if attribute_name in attributes:
                        player.setdefault(sub_dict, {})[
                            attribute_name] = attribute_value
                        break
                else:
                    # If not found in any sub-dictionary, add it directly to the player dictionary
                    player[attribute_name] = attribute_value

# Close the webdriver instance
driver.quit()

# Now you have a list of player dictionaries, which you can process or store as needed
for player_name, player_data in players.items():
    print(player_name)
    print(player_data)
    print('\n')
