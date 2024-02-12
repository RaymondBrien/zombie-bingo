# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials
import json
from pprint import pprint
import requests

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

def get_buzzwords():
    """
    Returns a list of words from the buzzwords list. 
    """
    with open('newsnowCreds.json', 'r') as f:
        creds = json.load(f)
    
    url = "https://newsnow.p.rapidapi.com/headline"

    payload = { "text": "Europe" }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": creds["X-RapidAPI-Key"],
        "X-RapidAPI-Host": "newsnow.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    pprint(response.json())    


def process_text(text):
    """
    Returns a list of words from the text. 
    Parses into lowercase, removes punctuation, and splits on whitespace.
    """
    words = text.split()
    return words

def find_most_common_words(data):
    """
    Returns a dictionary of the most common words in the data.
    """
    word_counts = {}
    for word in data:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1
    return word_counts

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
    buzzwords = get_buzzwords()
    pprint(wordbank_list)
    pprint(buzzwords)
    
main()