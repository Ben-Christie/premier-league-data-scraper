from unidecode import unidecode
from data import nations, fbref_positions
from rapidfuzz import process
import csv
import os


def add_player_to_dict(name, club, dictionary):
    # split name
    surname = ''
    forename = ''

    # simplify name
    name = unidecode(name)

    # split on space, maximum number of splits is 1
    names = name.split(' ', 1)

    # if surname (brazilian players often go by 1 name)
    if len(names) > 1:
        forename = names[0]
        surname = names[1]
    elif len(names) == 1:
        surname = names[0]

    # if the player has not been seen before, add it to the players dictionary
    if name not in dictionary:

        dictionary[name] = {
            # assign the player name and use unidecode to remove accents
            'surname': surname,
            'forename': forename,
            'club': club
        }

    return name


def clean_fbref_data_points(attribute_name, attribute_value):
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
            attribute_value = fbref_positions[parts[0]]
    elif 'minutes' in attribute_name:
        attribute_value = attribute_value.replace(',', '')

    return attribute_name, attribute_value


def integer_conversion(attribute_value):
    try:
        attribute_value = int(attribute_value)
    except ValueError:
        pass

    return attribute_value


def csv_split(players):

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


def fuzzy_match_players(search_term, players):
    # list of keys (names) in the main players dict
    player_names = list(players.keys())

    # fuzzy match search term with keys (names)
    best_match = process.extractOne(
        search_term, player_names, score_cutoff=70)

    # if we find something
    if best_match:
        matched_name, score, index = best_match
        return matched_name
    else:
        return "no match"
