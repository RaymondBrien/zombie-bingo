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
    wordbank = SHEET.worksheet('wordbank')
    wordbank_list = wordbank.col_values(2)[1:]
    
    return wordbank_list

def get_headlines():
    """
    Returns a list of words from the buzzwords list. 
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

    response = requests.post(url, json=payload, headers=headers)

    primary_text = response.json()
    title_collection = []
    for news_item in primary_text['news']:
        title_collection.append(news_item['title'])
    print(title_collection)
    
    return title_collection

def get_buzzwords(data):
    """
    Returns a dictionary of the most common words in the data.
    """
    tokens = word_tokenize(data)

    stop_words = set(stopwords.words('english'))
    filtered_words = [w for w in tokens if w not in stop_words]
    word_counts = Counter(filtered_words)
    
    num_keywords = 10
    buzzwords = word_counts.most_common(num_keywords)
    print('buzzwords:')
    for buzzword, frequency in buzzwords:
        print(buzzword, '-', frequency)
    
    
def validate_data(data):
    """
    Returns True if words are correctly formatted. 
    Words must be in string format, single words and lowercase. 
    Otherwise returns False with error message.
    """
    
def main():
    """
    Runs the main functions.
    """
    wordbank_list = get_wordbank_list()
    pprint(wordbank_list)
    headlines = get_headlines
    buzzwords = get_buzzwords(headlines)
    pprint(buzzwords)


    
# main()
get_headlines()

