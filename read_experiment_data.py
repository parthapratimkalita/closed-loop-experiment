import pandas as pd
import json
import re
import os


def read_experiment_data():
    #  Load the JSON file
    file_name = 'experimentData.json'

    # Construct the full path to the file in the Downloads folder
    downloads_folder = os.path.expanduser('~/Downloads')
    file_path = os.path.join(downloads_folder, file_name)

    with open(file_path, 'r') as file:
        data = json.load(file)

    pattern = re.compile(r'>red</div>|>green</div>')
    filtered_data = [row for row in data if pattern.search(row['stimulus'])]

    filtered_df = pd.DataFrame(filtered_data)[['rt', 'response', 'stimulus']]
    filtered_df['rt'] = filtered_df['rt'].fillna(3000)
    filtered_df['response'] = filtered_df['response'].fillna('j')

    return filtered_df
