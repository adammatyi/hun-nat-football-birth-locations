import pandas as pd
from bs4 import BeautifulSoup

# Read the CSV into a DataFrame
df = pd.read_csv('city_pops_scaled.csv')

# Define a function to clean HTML tags
def clean_html_tags(html):
    soup = BeautifulSoup(html, 'html.parser')
    return len(soup.find_all('a'))

# Apply the function to clean the 'players' column
df['player_count'] = df['players'].apply(clean_html_tags)

# Assuming you have already read the CSV into a DataFrame named df

# Convert population to numeric (handling NaNs if any)
df['population'] = pd.to_numeric(df['population'], errors='coerce')

# Extract the number of players from the 'players' column
df['num_players'] = df['players'].str.count('<a')

# Finding the smallest city with at least two players
smallest_city_with_two_players = df[df['num_players'] >= 2].nsmallest(1, 'population')

# Finding the city with the most players
city_with_most_players = df.nlargest(1, 'num_players')

# Finding the city with the highest ratio of players to population
df['player_population_ratio'] = df['num_players'] / df['population']
city_with_highest_ratio = df.nlargest(1, 'player_population_ratio')
df = df.sort_values('player_population_ratio')
# Print results
print("Smallest city with at least two players:")
print(smallest_city_with_two_players[['city', 'num_players', 'population']])

print("\nCity with the most players:")
print(city_with_most_players[['city', 'num_players']])

print("\nCity with the highest ratio of players to population:")
print(city_with_highest_ratio[['city', 'num_players', 'population', 'player_population_ratio']])
