# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials
import json
import requests
import nltk 
from nltk.corpus import stopwords
import re
import inflect
import math 
import colorama
from colorama import Fore, Back, Style
import time
import sys
import os
if os.path.exists('env.py'):
    import env
# import art # - needed?
from art import *

colorama.init(autoreset=True) #auto-reset color for each new line

# global variable to avoid repeating
SEPARATE = '----------------------------------------------------------------\n'


# REFACTORING TODOs:
# TODO error handling with SPEICIFIC error types
# TODO error for second user questsion - if not right type, look back to ask second Q again so doesn't just complete the program running
# TODO validate against marking criteria 

# TODO use this link to add zombie art at beggining and end: https://www.tutorialspoint.com/display-images-on-terminal-using-python#:~:text=There%20are%20several%20Python%20libraries,%2C%20OpenCV%2C%20and%20ASCII%20Art.
# TODO https://pypi.org/project/tabulate/
# TODO remove any unused imports. 
# TODO check deployed version on heroku so far. Note differences for readme
# TODO use spinning icon to indicate progress or stop user typing and indicate loading.

SCOPE = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive'
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('zombie_bingo')

def start_game():
    """
    Starts the game with small loading screen
    """
    try:
        print(f'{Fore.BLACK}{Back.LIGHTYELLOW_EX}****LOADING ZOMBIE BINGO****')
        animation_loop()
        print(SEPARATE)
        print(text2art('Zombie Bingo!', font="small"))
        print('Gathering the hottest info: please wait a moment')
    except KeyboardInterrupt as e:
        print(SEPARATE)
        print(f'\n{Fore.RED}Ouch! Don\'t poke me when I\'m booting up the program!')
        while True:
            print(SEPARATE)
            key_interrupt = input(f'\Do you want to continue launching the game?\n{Fore.LIGHTYELLOW_EX}Type y or n:\n')
            if key_interrupt.lower() == 'y':
                print('\nCool, I\'ll start the game')
                os.system('cls') # add 'clear' parameter for Linux and MacOS? 
                start_game()
                break
            elif key_interrupt.lower() == 'n':
                print('\nOk, I\'ll close the game! See you soon!\n')
                False
                sys.exit(0)
            elif key_interrupt.lower() != 'y' and key_interrupt.lower() != 'n':
                print(f'Please enter either y or n. {Fore.LIGHTYELLOW_EX}You wrote: {key_interrupt}')
    except ImportError as e:
        print(f'Import Error: {e.args}')
    except RuntimeError as e:
        print(f'Runtime Error: {e.args}')
    finally:
        False # to prevent any uncaught while loop issues from KeyboardInterrupt.

def animation_loop():
    animation = "|/-\\"
    start_time = time.time()
    while True:
        for i in range(4):
            time.sleep(0.1)  # Feel free to experiment with the speed here
            sys.stdout.write("\r" + animation[i % len(animation)])
            sys.stdout.flush()
        if time.time() - start_time > 3:  # The animation will last for 10 seconds
            break
    sys.stdout
def get_wordbank_list():
    """
    Returns all words in the wordbank as a list.
    """
    wordbank = SHEET.worksheet('wordbank').col_values(2)[1:] # write as a function instead
    
    return wordbank
def get_headlines():
    """
    Returns a list of headlines titles as strings, from top newsnow API. 
    """
    url = "https://newsnow.p.rapidapi.com/newsv2"

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
        "X-RapidAPI-Key": os.environ.get('RAPID_API_KEY'),
        "X-RapidAPI-Host": "newsnow.p.rapidapi.com"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)

        primary_text = response.json()
        title_collection = []
        for news_item in primary_text['news']:
            title_collection.append(news_item['title'])
    except Exception as e: #TODO handle with SPECIFIC exception
        raise Exception #TODO as above
    return title_collection

def test_get_headlines():
    """
    TODO remove when finished?
    FOR TESTING PURPOSES ONLY TO AVOID MAXING OUT API REQUESTS. 
    """
    title_collection = 'Global Leaders Convene for Climate Summit; chaos destruction survival desolation catastrophePledge Action on Climate Change. Tech Giants Unveil New Innovations at Annual Conference, Economic Uncertainty Looms as Stock Markets Fluctuate, Health Experts Warn of Potential New Wave of Pandemic Cases. Renewable Energy Surges, Outpacing Fossil Fuel Investments, Political Turmoil Erupts in Region, Raising Concerns for Stability. Breakthrough in Medical Research Offers Hope for Rare Diseases, Education Sector Faces Challenges Amidst Shift to Online Learning. Space Exploration Reaches New Heights with Successful Satellite Launch, Environmentalists Rally for Conservation Efforts in Face of Biodiversity Loss.'
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

def find_list_intersections(list1, list2):
    """
    Returns list of all intersections between list1 and list2.
    """
    intersections = set(list1).intersection(list2)
    return intersections

def remove_common_words(data):
    """
    Returns string list with common words removed.
    """
    common_words = SHEET.worksheet('wordbank').col_values(3)[1:] #TODO make a function to avoid repeating this
    try:
        #find all words in data that are not in common_words
        words_to_remove = find_list_intersections(common_words, data)
        data = [word for word in data if word not in stopwords.words('english') and word not in words_to_remove]
    except Exception as e: #TODO add specific exception
        raise e.with_traceback()
    return data
    
def percentage_of_wordbank_matches(data):
    """
    Returns percentage of matches between data and wordbank.
    This defines the percentage likelihood of apocalypse.
    """
    wordbank = SHEET.worksheet('wordbank').col_values(2)[1:] #TODO add as a function to avoid repeating this
    matches = find_list_intersections(wordbank, data)
    
    #find percentage of wordbank matches
    print(f'percentage = {len(matches)} divided by {len(wordbank)} * 100')
    percentage = len(matches) / (len(wordbank)) * 100
    percentage = math.floor(percentage)
    return percentage

def get_wordbank_matches_list(data):
    """
    Returns list of wordbank matches.
    """
    wordbank = SHEET.worksheet('wordbank').col_values(2)[1:] #TODO use function to avoid repeating
    
    #find number of matches between data and wordbank 
    matches = find_list_intersections(wordbank, data)
    return matches
    
def update_worksheet_row(worksheet_name, values):
    """
    Adds data to spreadsheet as a new row.
    """
    try:
        print(f'Updating {worksheet_name} worksheet...\n')
        SHEET.worksheet(worksheet_name).append_row(values) 
        print(f'{Fore.LIGHTGREEN_EX}{worksheet_name} worksheet successfully updated...\n')
        
    except TypeError as e:
        raise TypeError('data must be a list') and print(e.with_traceback()) #TODO sort so doesn't finish program, will ask to start again.

def update_worksheet_cell(worksheet_name, data):
    """
    Adds data to spreadsheet as a new cell.
    """
    try:
        print(f'Updating {worksheet_name} worksheet...\n')
        SHEET.worksheet(worksheet_name).append_row(data) 
        print(f'{worksheet_name} worksheet successfully updated...\n')
        
    except TypeError as e:
        raise TypeError('data must not be a list') and print(e.with_traceback()) #TODO sort so doesn't finish program, will ask to start again.
        
def get_user_input1():
    """
    Returns user input 1.
    """
    while True:
        print(SEPARATE)
        print('Welcome pessimist. How likely is doomsday today? (/100)\n')
        print('Your answer should be a number between 1 and 100.\n')
        print('Example: 65\n')
        print(SEPARATE) # TODO add graphics? Or Color?
        user_answer = int(input('\nEnter a number: '))

        if validate_user_input1(user_answer):
            print(f'{Fore.LIGHTGREEN_EX}Answer received, thank you!\n')
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
        if type(user_input1) == int: #TODO fix. At moment if false, still returns true? Test and know how if else, except and better error handling work better
        # while int(user_input1) == True:
            if user_input1 < 0 or user_input1 > 100:
                raise ValueError(f'Invalid input: {user_input1}. Your number must be between 0 and 100')
        else:
            raise ValueError(f'Invalid input, expected an integer, got {type(user_input1)}')
    except ValueError as e:
        print(f'You wrote: {e}.\n Please enter a number between 1 and 100.\n') 
        return False

    return True #TODO Debug logixc

def get_user_input2():
    """
    Returns user input 2 as list of strings.
    """
    print(SEPARATE)
    print('For some bonus points, enter 3 key words you think are in the news today\n')
    print('Here\'s an example: apocalypse, AI, mutation\n')
    print(SEPARATE)
    input_data = input('Enter 3 key words: ')
    user_answer = input_data.split(',')

    if validate_user_input2(user_answer):
        print(SEPARATE + '\n')
        print(f'{Fore.LIGHTGREEN_EX}Gotcha! Let me have a think now.\n')
        print(SEPARATE + '\n')
        
    return user_answer
    
def validate_user_input2(user_input2): # TODO add error handling with specific exception
    """
    If user input is not a string, or if total number of provided key words
    is not 3, raises ValueError exception.
    """
    while True:
        try:        
            if len(user_input2)!= 3:
                raise Exception ( 
                    f'Please enter 3 key words, separated by commas.\n You entered: {len(user_input2)}\n')
        except ValueError as e:
            print(f'Invalid Type: {e.args}. Please enter 3 key words. Numbers are not allowed.\n')
            return False
  
def calculate_user_buzzword_points(keyword_list, user_list):
    """
    Find any matches between API headlines and user buzzwords.
    Generate score - one point per matched buzzword.
    Maximum of three points per turn.
    """
    matches_list = find_list_intersections(user_list, keyword_list)
    points = len(matches_list)
    return points

def calculate_user_percentage_score(user_input1, percentage):
    """
    If user is within 10% range of actual percentage, 
    return 1 point. Else return 0.
    """
    if user_input1 <= percentage + 10 and user_input1 >= percentage - 10:
        #1 point awarded to user
        return 1
    else:
        return 0

def get_user_scores_list():
    """
    Gets column data from user scores logged from each time 
    user completes game.
    """
    sheet_values = SHEET.worksheet('end_calculator').col_values(2)[1:] # avoid repetition with function instead
    user_scores = []
    for value in sheet_values:
        value = int(value)
        user_scores.append(value)
    return user_scores
def get_user_average_score(user_scores):
    """
    Returns average score for user.
    """
    score = sum(user_scores) / len(user_scores)    
    return math.floor(score)
def play_again():
    """ 
    Starts program again if y.
    Finishes program if n.
    """
    if input(f'Would you like to play again? {Fore.LIGHTBLACK_EX}({Fore.GREEN}y{Fore.LIGHTBLACK_EX}/{Fore.RED}n{Fore.LIGHTBLACK_EX}): ').lower() == 'y':
        main()
    else:
        print('Thank you for playing!')
        exit()

def main():
    """
    Runs all program functions.
    """
    start_game()

    # headlines = get_headlines() # commented output for testing purposes, using testing headlines instead to avoid maxing API requests*****
    
    # main functions
    headlines = test_get_headlines()
    processed_headlines = process_data(headlines)
    keyword_list = remove_common_words(processed_headlines)
    percentage = percentage_of_wordbank_matches(keyword_list)
    headline_matches = get_wordbank_matches_list(keyword_list) # TODO make headline matches alphabetical so appear nicely in worksheet 
    
    # concatenate program answers for easy worksheet parsing
    program_full_answer = list(str(percentage)) + list(headline_matches) 
    # print(f'program_full_answer: {program_full_answer}') # for debugging purposes only

    # get user answers
    answer1 = get_user_input1()
    answer2 = get_user_input2() 
    
    # concatenate user answers for easy worksheet parsing
    user_full_answer = list(str(answer1)) + answer2
    # print(f'program full_answer: {user_full_answer}') # for debuggging purposes only
    
    # calculate scores
    user_matches = calculate_user_buzzword_points(answer2, headline_matches)
    user_percentage_score = calculate_user_percentage_score(answer1, percentage) #TODO test functions correctly
    user_total_score = user_matches + user_percentage_score
    scores_history = get_user_scores_list()
    average_score = get_user_average_score(scores_history)
    end_results = [percentage, user_total_score]
    # print(f'End results: {end_results}\n') # for debug purposes only

    # update worksheets
    update_worksheet_row('program_answers', program_full_answer)
    update_worksheet_row('user_answers', user_full_answer)
    update_worksheet_cell('end_calculator', end_results)

    # report info to terminal for user
    print(SEPARATE + '\n') #TODO tabulate these data points so looks nice in terminal. Or write as a function?
    print(f'{Fore.GREEN}Your answers: {user_full_answer}\n') #TODO DEBUG picks up a two digit number as two numbers: e.g. 65, 66 = '6','6'
    print(f'{Fore.RED}Today\'s keywords in the news headlines were:\n{Fore.LIGHTYELLOW_EX}{headline_matches}\n')
    print(f'You won: {user_total_score} point(s)\n') #TODO add graphic depending on how many points out of max won. (Smiley face or cool terminal graphic). Will need new function.
    print(f'Your average score is: {average_score} point(s)')
    print(SEPARATE + '\n') 
    print(f'****{Fore.RED}{Style.BRIGHT}Today there is a {percentage}% chance of apocalypse!****')
    print(SEPARATE + '\n') 

    # play again y/n
    play_again()

if __name__ == '__main__':    
    main()

