# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials
import json
from pprint import pprint
import requests
import nltk
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords
from collections import Counter
import re
import inflect

SCOPE = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive'
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('zombie_bingo')

def get_wordbank_list():
    """
    Returns all words in the wordbank as a list.
    """
    wordbank = SHEET.worksheet('wordbank').col_values(2)[1:]
    
    return wordbank

def get_headlines():
    """
    Returns a list of headlines titles as strings, from top newsnow API. 
    """
    url = "https://newsnow.p.rapidapi.com/newsv2"
    with open('newsnowCreds.json', 'r') as f:  
        creds = json.load(f)
    
    payload = {
        "query": "AI",
        "time_bounded": True,
        "from_date": "01/02/2021",
        "to_date": "05/06/2021",
        "location": "us",
        "language": "en",
        "more_information": False,
        "max_result": 10
    }
    
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": creds["X-RapidAPI-Key"],
        "X-RapidAPI-Host": "newsnow.p.rapidapi.com"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)

        primary_text = response.json()
        title_collection = []
        for news_item in primary_text['news']:
            title_collection.append(news_item['title'])
    except Exception as e:
        print(e)
    return title_collection

def process_data(data):
    """
    Returns string list all lowercase, with punctuation removed.
    """
    data = str(data)
    # remove punctuation
    data = re.sub(r'[^\w\s]','', data)
    data = data.lower()
    data = data.split()
    
    # turn any int within text into words
    for word in data:
        if word is int:
            word = inflect.engine().number_to_words(word)
    data = ' '.join(data)
    return data

def get_buzzwords(data):
    """
    Returns a list of the most common words in the data and 
    how often each word appears.
    """
    # tokens = word_tokenize(data)

    # stop_words = set(stopwords.words('english'))
    # filtered_words = [w for w in tokens if w not in stop_words]
    # word_counts = Counter(filtered_words)
    
    # num_keywords = 10
    # buzzwords = word_counts.most_common(num_keywords)
    # for buzzword, frequency in buzzwords:
    #     pprint(buzzword, frequency)
    # buzzwords_count = f'buzzwords: {buzzwords}'
    # return buzzwords_count

    common_words = SHEET.worksheet('wordbank').col_values(3)[1:]
    try:
        #find all words in data that are not in common_words
        buzzwords = [set(common_words).intersection(data)]
        
    except Exception as e:
        raise e.with_traceback()
    return buzzwords
    
    
def percentage_of_matches(data):
    """
    Returns percentage of headline words (data) that are in the buzzword list.
    """
    
    
    
def main():
    """
    Runs all program functions.
    """
    headlines = get_headlines()
    print(headlines)
    processed_headlines = process_data(headlines)
    pprint(processed_headlines)
    buzzword_list = get_buzzwords(processed_headlines)
    print(buzzword_list)



    
# main()
get_headlines()
