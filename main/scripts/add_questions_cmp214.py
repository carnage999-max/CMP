import requests
import pandas as pd
from bs4 import BeautifulSoup


url = "https://mcqmate.com/topic/database-management-system?page=3"

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

questions = {}

questions_elements = soup.select("thead tr td h2")

for element in questions_elements:
    questions[element.get_text()] = []

    
options = []
options_elements = soup.select('tbody tr td')
for option in options_elements:
    options.append(option.get_text())
option_pairs = [(options[i], options[i + 1]) for i in range(0, len(options), 2)]

options.clear()
for option in option_pairs:
    options.append(option[0] + option[1])
    
option_set = [(options[i], options[i + 1], options[i + 2], options[i + 3]) for i in range(0, len(options), 4)]
options.clear()
for option in option_set:
    options.append(option[0] + "\n" + option[1] + "\n" + option[2] + "\n" + option[3])

answers_elements = soup.select('tfoot tr td')
answers = [answer.get_text() for answer in answers_elements]

for key, options, answer in zip(questions, options, answers):
    questions[key] = {'options': options.split('\n'), 'answer': answer}

# Convert the dictionary to a DataFrame
df = pd.DataFrame.from_dict(questions, orient='index')

# Reset the index to make 'Questions' a column
df.reset_index(inplace=True)
df.rename(columns={'index': 'Questions'}, inplace=True)

# Save the DataFrame to a CSV file
csv_file_path = 'cmp214_2.csv'
df.to_csv(csv_file_path, index=False)

