import pandas as pd


df = pd.read_csv('dw_export.csv')

df['city'].fillna(df['parent_city'].apply(lambda x: x.split('/')[-1] if pd.notna(x) else None), inplace=True)

df['player_anchor'] = df.apply(lambda row: f'<a href="{row["player_wiki_link"]}">{row["name"] + " - " + row["birth_date"]}</a>', axis=1)

grouped = df.groupby('city').agg({
    'LAT': 'first',
    'LON': 'first',
    'population': 'first',
    'player_anchor': lambda x: '<br>'.join(x)
}).reset_index()

grouped['LAT'] = grouped['LAT'].apply(lambda x: None if pd.isna(x) else x)
grouped['LON'] = grouped['LON'].apply(lambda x: None if pd.isna(x) else x)
grouped['population'] = grouped['population'].apply(lambda x: None if pd.isna(x) else x)

grouped.columns = ['city', 'LAT', 'LON', 'population', 'players']
grouped.to_csv('reduced_city_data.csv', index=False)