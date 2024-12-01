import pandas as pd
from openai import OpenAI

#TODO: REMOVE API KEY BEFORE UPLOADING
client = OpenAI(
    api_key = "")

csv_filepath = "Organized_Car_Data/Chevrolet/Coupe.csv"
pd.set_option('display.max_columns', None)
csv = pd.read_csv(csv_filepath, encoding='utf-8')

#print(csv.columns)
#print(csv.head())

user_query = "Under 30000"

prompt = f"""
You are an assistant that helps search through a car database.
Here is a portion of the database:
{csv}

User Query: {user_query}
Based on the above data, provide the most relevant rows or answers.
"""

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "system", "content": "You are an assistant that searches a CSV of cars."},
              {"role": "user", "content": prompt}]
)

message_content = response.choices[0].message.content

print(message_content)