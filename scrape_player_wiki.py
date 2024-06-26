import csv
import os
import re
from functools import lru_cache

import requests
from bs4 import BeautifulSoup


@lru_cache(maxsize=None)
def fetch_city_pops(url):
    print(f"Parsing {url}")
    if url == "": return 'Population data not found'
    target_response = requests.get(url)
    target_content = target_response.content

    target_soup = BeautifulSoup(target_content, 'html.parser')
    infobox = target_soup.find('table', class_='infobox ujinfobox')
    if infobox:
        if url.find("hu.wikipedia.org"):
            population_pattern = re.compile(r'\b\d{1,6}\s*fő\b')
            matches = infobox.find_all(text=population_pattern)

            pop_list = [match.strip() for match in matches if match.strip().endswith('fő')]
            return pop_list[0].replace("fő", "").replace(u"\u00A0", "") if pop_list else None

    return 'Population data not found'


missing_pops = set()
collected_data = dict()

with open('city_pops.csv', 'r', newline='', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)

    for row in reader:
        if not row[1].strip().isnumeric():
            missing_pops.add(row[0])


missing_player_data = []

with open('hun_nat_birth_data.csv', 'r', newline='', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)

    for row in reader:
        if row[1].strip() in missing_pops:
            missing_player_data.append(row)


for player_data in missing_player_data:
    player_link = player_data[3]
    print(f"=================================================================")
    print(f"Parsing {player_link}")
    soup = BeautifulSoup(requests.get(player_link).content, "html.parser")

    infobox = soup.find("table", class_="infobox")

    if infobox:
        birth_place_row = infobox.find('td', text='Születési hely')

        if birth_place_row:
            table_row = birth_place_row.parent
            table_value = table_row.find_all('td')[1]
            first_child = table_value.contents[0]

            if first_child.name == 'a':
                city_link = 'http://hu.wikipedia.org' + first_child.get('href')
                print(f"City link found: {city_link}")
                pops = fetch_city_pops(city_link)
                collected_data[player_data[1]] = (pops, city_link)


with open("city_pops_v2.csv", 'w', newline='', encoding='utf-8') as file:
    city_population_dict = collected_data
    writer = csv.writer(file)
    writer.writerow(['city', 'population', 'wiki'])
    for city, data in city_population_dict.items():
        writer.writerow([city, data[0], data[1]])