from unidecode import unidecode
from data import nations, positions


def add_player_to_dict(name, club, dictionary):
    # if the player has not been seen before, add it to the players dictionary
    if name not in dictionary:
        dictionary[name] = {
            # assign the player name and use unidecode to remove accents
            'full_name': unidecode(name),
            'club': club,
        }


def clean_data_points(attribute_name, attribute_value):
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

    return attribute_name, attribute_value


def integer_conversion(attribute_value):
    try:
        attribute_value = int(attribute_value)
    except ValueError:
        pass

    return attribute_value
