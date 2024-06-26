import csv
from functools import lru_cache

import requests

collected_data = []


@lru_cache(maxsize=None)
def check_wikipedia_page(city_name, wiki_base):
    print(f"Parsing {city_name} on {wiki_base}")
    wikipedia_url = f"{wiki_base}{city_name.replace(' ', '_')}"
    response = requests.head(wikipedia_url)

    if response.status_code == 200:
        print(f"The {wiki_base} Wikipedia page for {city_name} exists.")
        return wikipedia_url
    else:
        print(f"The {wiki_base} Wikipedia page for {city_name} does not exist.")
        return check_wikipedia_page(city_name, "https://en.wikipedia.org/wiki/") if not wiki_base == "https://en.wikipedia.org/wiki/" else None


in_csv_file_path = 'hun_nat_birth_data.csv'
out_csv_file_path = 'hun_nat_birth_data_wiki_l.csv'

with open(in_csv_file_path, 'r', newline='', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)

    for row in reader:
        city_name = row[1].strip()
        collected_data.append({'name': row[0], 'city': row[1], 'wiki': check_wikipedia_page(city_name, "https://hu.wikipedia.org/wiki/"), 'birth_date': row[2]})


with open(out_csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['name', 'city', 'wiki', 'birth_date']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(collected_data)