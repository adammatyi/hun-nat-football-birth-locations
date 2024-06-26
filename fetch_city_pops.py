import csv
import locale
import os
import re
from functools import lru_cache

from bs4 import BeautifulSoup
import requests

in_csv_file_path = 'hun_nat_birth_data_wiki_l_manual.csv'
out_csv_file_path = 'hun_nat_birth_data_pops.csv'

collected_data = []


@lru_cache(maxsize=None)
def fetch_city_pops(url):
    url = "http://hu.wikipedia.org/wiki/Sz%C5%91ny"
    print(f"Parsing {url}")
    if url == "": return 'Page not found'
    target_response = requests.get(url)
    target_content = target_response.content

    target_soup = BeautifulSoup(target_content, 'html.parser')
    infobox = target_soup.find('table', class_='infobox')
    if infobox:
        if "hu.wikipedia.org" in url:
            population_pattern = re.compile(r'\b\d{1,6}\s*fő\b')
            matches = infobox.find_all(text=population_pattern)

            pop_list = [match.strip() for match in matches if match.strip().endswith('fő')]
            return pop_list[0].replace("fő", "").replace(u"\u00A0", "") if pop_list else None
        elif "en.wikipedia.org" in url:
            population = None
            population_tag = infobox.find(text=re.compile('Population')).parent
            if population_tag:
                population_data_tag = population_tag.find_next('td')
                if population_data_tag:
                    population_text = population_data_tag.text.strip()
                    pattern = r'^\d{1,3}(?:,\d{3})*'
                    match = re.match(pattern, population_text)
                    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
                    return locale.atoi(match.group()) if match else None
            return population
    return 'City data not found'


with open(in_csv_file_path, 'r', newline='', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)

    for row in reader:
        city_name = row[1].strip()
        collected_data.append({'name': row[0], 'city': row[1], 'population': fetch_city_pops(row[2]), 'wiki': row[2], 'birth_date': row[3]})


with open(out_csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['name', 'city', 'population', 'wiki', 'birth_date']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(collected_data)


with open("city_pops.csv", 'w', newline='', encoding='utf-8') as file:
    city_population_dict = {item['city']: (item['population'], item['wiki']) for item in collected_data}
    writer = csv.writer(file)
    writer.writerow(['city', 'population', 'wiki'])
    for city, data in city_population_dict.items():
        writer.writerow([city, data[0], data[1]])