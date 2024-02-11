import requests

from bs4 import BeautifulSoup
import pandas as pd

import csv



def scrapeQuestions():
    url = "https://www.javatpoint.com/operating-system-mcq-part-2"

    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    result = {}

    question_element = soup.select(".pq")
    for question in question_element:
        result[question.get_text()] = ""

    options = []
    option_element = soup.select(".pointsa")
    for option in option_element:
        options.append(option.get_text())

    answers = []
    answer_element = soup.select(".testanswer")
    for answer in answer_element:
        answers.append(answer.get_text())

    for question, option, answer in zip(result, options, answers):
        result[question] = {'options': option.split('\n'), 'answer': answer}

    # Convert the dictionary to a DataFrame
    df = pd.DataFrame.from_dict(result, orient='index')

    # Reset the index to make 'Questions' a column
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Questions'}, inplace=True)

    # Save the DataFrame to a CSV file
    csv_file_path = 'cmp217_2.csv'
    df.to_csv(csv_file_path, index=False)


if __name__ == '__main__':
    scrapeQuestions()
    