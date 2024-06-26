import csv

collected_data = dict()

with open('city_pops.csv', 'r', newline='', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)

    for row in reader:
        collected_data[row[0]] = (row[1], row[2])

with open('city_pops_v2.csv', 'r', newline='', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)

    for row in reader:
        collected_data[row[0]] = (row[1], row[2])

with open("city_pops_merged.csv", 'w', newline='', encoding='utf-8') as csv_file:
    city_population_dict = collected_data
    writer = csv.writer(csv_file)
    writer.writerow(['city', 'population', 'wiki'])
    for city, data in city_population_dict.items():
        writer.writerow([city, data[0], data[1]])