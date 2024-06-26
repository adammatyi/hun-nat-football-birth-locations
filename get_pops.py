import csv

in_csv_file_path = 'hun_nat_birth_data_wiki_l.csv'

with open(in_csv_file_path, 'r', newline='', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)

    for row in reader:
        city_link = row[2].strip()
        if city_link == "":
            print(row[0])
            print(row[1])
