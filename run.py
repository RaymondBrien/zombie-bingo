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
import math 

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

def test_get_headlines():
    """
    FOR TESTING PURPOSES ONLY TO AVOID MAXING OUT API REQUESTS.
    """
    title_collection = 'Global Leaders Convene for Climate Summit; Pledge Action on Climate Change. Tech Giants Unveil New Innovations at Annual Conference, Economic Uncertainty Looms as Stock Markets Fluctuate, Health Experts Warn of Potential New Wave of Pandemic Cases. Renewable Energy Surges, Outpacing Fossil Fuel Investments, Political Turmoil Erupts in Region, Raising Concerns for Stability. Breakthrough in Medical Research Offers Hope for Rare Diseases, Education Sector Faces Challenges Amidst Shift to Online Learning. Space Exploration Reaches New Heights with Successful Satellite Launch, Environmentalists Rally for Conservation Efforts in Face of Biodiversity Loss.'
    return title_collection
    
def process_data(data):
    """
    Returns string list all lowercase, with punctuation removed.
    Turns any ints into version (e.g. 1 -> 'one').
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
        data = list(data)
        
    return data

def remove_common_words(data):
    """
    Returns string list with common words removed.
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
        words_to_remove = [set(common_words).intersection(data)]
        # buzzwords = [word for word in buzzwords if word not in stopwords.words('english')]
        data = [word for word in data if word not in stopwords.words('english') and word not in words_to_remove]
    except Exception as e:
        raise e.with_traceback()
    return data
    
def percentage_of_wordbank_matches(data):
    """
    Returns percentage of matches between data and wordbank.
    This defines the percentage likelihood of apocalypse.
    """
    wordbank = SHEET.worksheet('wordbank').col_values(2)[1:]
    
    #find number of matches between data and wordbank 
    matches = set(wordbank).intersection(data)

    #find percentage of wordbank matches
    print(f'percentage = {len(matches)} divided by {len(wordbank)} * 100')
    percentage = len(matches) / (len(wordbank)) * 100
    percentage = math.floor(percentage)
    return percentage

def get_wordbank_matches_list(data):
    """
    Returns list of wordbank matches.
    """
    wordbank = SHEET.worksheet('wordbank').col_values(2)[1:]
    
    #find number of matches between data and wordbank 
    matches = set(wordbank).intersection(data)
    return matches
    
def add_to_worksheet_(worksheet_name, data):
    """
    Adds data to spreadsheet as a new row.
    """
    
    try:
        print(f'Updating {worksheet_name} worksheet...\n')
        #adds new row to worksheet
        SHEET.worksheet(worksheet_name).append_row(data) 
        
        print(f'{worksheet_name} worksheet successfully updated...\n')
    
    except Exception as e:
        raise e.with_traceback()
    
def get_user_input1():
    """
    Returns user input 1.
    """
    while True:
        print('------------------------------------------------------------')
        print('Welcome pesimist. How likely is doomsday today? (/100)\n')
        print('Your answer should be a number between 1 and 100.\n')
        print('Example: 65\n')
        print('------------------------------------------------------------\n')
        user_answer = int(input('\nEnter a number: '))

        if validate_user_input1(user_answer):
            print('Answer received, thank you!\n')
            break
            
    return user_answer
 
def validate_user_input1(user_input1):
    """
    Converts user input to integer.
    If user input is not an integer, or if number 
    is not between 0 and 100, raises ValueError exception.
    Returns int.
    """
    try:
        while int(user_input1) == True:
            if user_input1 < 0 or user_input1 > 100:
                raise ValueError(f'Invalid input: {user_input1}. Your number must be between 0 and 100')
    
    except ValueError as e:
        print(f'You wrote: {e}.\n Please enter a number between 1 and 100.\n') 
        return False

    return True

def get_user_input2():
    """
    Returns user input 2 as list of strings.
    """
    while True:
        print('------------------------------------------------------------')
        print('Nice one. \n')
        print('For some bonus points, enter 3 buzzwords you think are in the news today \n')
        print('Example: apocalypse, AI, mutation\n')
        print('------------------------------------------------------------')
        input_data = input('Enter 3 buzzwords: ')
        user_answer = input_data.split(',')

        if validate_user_input2(user_answer):
            print('------------------------------------------------------------')
            print('Answer received, thank you!\n')
            break
            
    return user_answer
    
def validate_user_input2(user_input2):
    """
    If user input is not a string, or if total number of provided buzzwords
    is not 3, raises ValueError exception.
    """
    try:
        [str(value) for value in user_input2]
        if len(user_input2)!= 3:
            raise ValueError(
                f'Please enter 3 buzzwords, separated by commas.\n You entered: {len(user_input2)}\n')
    
    except ValueError as e:
        print(f'Invalid: {e}. Please enter 3 buzzwords. Numbers are not allowed.\n')
        return False

    return True
  
def calculate_user_buzzword_points(keyword_list, user_list):
    """
    Find any matches between API headlines and user buzzwords.
    Generate score - one point per matched buzzword.
    Maximum of three points per turn.
    """
    
    matches_list = set(user_list).intersection(keyword_list)
    points = len(matches_list)
    
    return points

def calculate_user_percentage_score(user_input1, percentage):
    """
    If user is within 10% range of actual percentage, 
    return 1 point. Else return 0.
    """
    if user_input1 <= percentage + 10 and user_input1 >= percentage - 10:
        return 1
    else:
        return 0
    
# def calculate_user_total_score(score1, score2):
#     """
#     Returns total score of user input.
#     """
#     # score1 = calculate_user_buzzword_points()
#     # score2 = calculate_user_percentage_score()
    
#     total = score1 + score2
#     return total

def main():
    """
    Runs all program functions.
    """
    print('\nRunning Zombie Bingo...\n')
    print('----------------------------------------------------------------')
    print('\nWelcome to the Zombie Bingo!\n')
    
    # commented output for testing purposes, using testing headlines instead 
    # to avoid maxing API requests
    # headlines = get_headlines()
    
    headlines = test_get_headlines()
    processed_headlines = process_data(headlines)
    keyword_list = remove_common_words(processed_headlines)
    percentage = percentage_of_wordbank_matches(keyword_list)
    headline_matches = get_wordbank_matches_list(keyword_list)
    

    answer1 = get_user_input1()
    answer2 = get_user_input2() 
    # convert answer 1 to string list to concatenate with answer 2 as full answer
    answer1 = list(str(answer1))
    full_answer = answer1 + answer2
    print(f'full_answer: {full_answer}')
    
    user_matches = calculate_user_buzzword_points(answer2, headline_matches)
    user_percentage_score = calculate_user_percentage_score(answer1, percentage)
    user_total_score = user_matches + user_percentage_score
    
    # add_new_worksheet_row('user_input', answer2)
       
    print(f'Today\'s apocalypse likelihood: {percentage}%')
    print(f'Number of headline words which match doomsday wordbank: {len(headline_matches)}')
    print(f'Keyword matches: {headline_matches}')
    print('\n----------------------------------------------------------------\n')
    print(f'\nYour score: {user_total_score}\n')

    # add_new_worksheet_single_cell('end_calculator', percentage)
    # add_new_worksheet_row('keywords', matches)

    
main()
