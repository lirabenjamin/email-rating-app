import pandas as pd
import json

# Load the data
data = pd.read_parquet('instance/texts_to_rate.parquet')

data = data[['text_id', 'text']]
data.rename(columns={'text': 'content', "text_id": "id"}, inplace=True)

# Convert DataFrame to JSON
json_data = data.to_dict(orient='records')

# Save JSON to file
with open('instance/emails2.json', 'w') as f:
    json.dump(json_data, f, indent=2)
