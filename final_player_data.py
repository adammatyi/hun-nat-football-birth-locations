import csv
import locale

collected_data = []
cities = dict()

with open("city_pops_merged_manual.csv", 'r', newline='', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)

    for row in reader:
        row[1] = float(row[1].replace(' ', '').replace(',', '.').replace(u"\u00A0", ""))
        # city,population,wiki,parent,manual
        cities[row[0]] = {"city": row[0], "population": row[1], "wiki": row[2], "parent": row[3], "manual": row[4]}

with open("hun_nat_birth_data.csv", 'r', newline='', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)

    for row in reader:
        # city,population,wiki,parent,manual
        collected_data.append({'name': row[0], 'birth_date': row[2], 'player_wiki_link': row[3], 'city': row[1], 'population': cities[row[1]]["population"], "city_wiki": cities[row[1]]["wiki"], "parent_city": cities[row[1]]["parent"], "is_manual": cities[row[1]]["manual"]})


with open("final_player_data.csv", 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=collected_data[0].keys())
    writer.writeheader()
    writer.writerows(collected_data)
