import csv
import time

import requests
from bs4 import BeautifulSoup
import re

base_url = 'https://www.magyarfutball.hu'
url = f"{base_url}/hu/szemelyek/valogatott_jatekosok"
response = requests.get(url)
web_content = response.content

soup = BeautifulSoup(web_content, 'html.parser')

pattern = re.compile(r'^/hu/szemelyek/valogatott_jatekosok/[a-z]')
links = soup.find_all('a', href=pattern)

collected_links = [link['href'] for link in links]
collected_data = []


def get_page_content_with_retries(url, retries=3, delay=5):
    """
    Attempts to retrieve the content of the given URL with retries on failure.

    Args:
        url (str): The URL to fetch.
        retries (int): The number of retry attempts.
        delay (int): The delay between retries in seconds.

    Returns:
        str: The content of the page if successful, None otherwise.
    """
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            attempt += 1
            if attempt < retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
    print(f"Failed to retrieve content from {url} after {retries} attempts.")
    return None


for link in collected_links:
    full_url = base_url + link
    print(f"Parsing letter {full_url[-1].upper()}")
    target_response = requests.get(full_url)
    target_content = target_response.content
    target_soup = BeautifulSoup(target_content, 'html.parser')
    table_rows = target_soup.find_all('tr')
    print(f"Found {len(table_rows)-1} entries")
    for row in table_rows:
        if row.find_all('th'):
            continue

        cells = row.find_all('td')
        if len(cells) >= 3:
            name = cells[0].find('a').text.strip()
            print(f"Player: {name}")
            city = cells[1].text.strip()
            birth_date = cells[2].text.strip()
            # player_content = requests.get(base_url+cells[0].find('a')["href"]).content
            player_content = get_page_content_with_retries(base_url+cells[0].find('a')["href"])
            soup = BeautifulSoup(player_content, 'html.parser')
            wiki_link = soup.select_one("a[href*=wikipedia]")["href"] if soup.select_one("a[href*=wikipedia]") is not None else None
            collected_data.append({'name': name, 'city': city, 'birth_date': birth_date, 'wiki_link': wiki_link})

csv_file_path = 'hun_nat_birth_data.csv'

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['name', 'city', 'birth_date', 'wiki_link']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(collected_data)