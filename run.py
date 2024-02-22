# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials
import json
import requests
import nltk 
import pprint
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
from google.api_core.exceptions import AlreadyExists # https://googleapis.dev/python/google-api-core/latest/exceptions.html #https://stackoverflow.com/questions/23945784/how-to-manage-google-api-errors-in-python

colorama.init(autoreset=True) #auto-reset color for each new line

# global variable to avoid repeating TODO is this the best way to do this?
separate = '----------------------------------------------------------------\n'
SEPARATE = separate.center(80)

# REFACTORING TODOs:
# TODO Handle errors including MAIN.
# TODO test errors and document
# TODO look up how to handle empty input errors (perhaps with counter or len) 
# TODO error for second user questsion - if not right type, look back to ask second Q again so doesn't just complete the program running
# TODO make all questions, input text prompts and elements consistent in their styling.
# TODO get system type - if mac or linux, use os.system(clear). If windows use 'cls' instead. Try as class on init?
# TODO use this link to add zombie art at beggining and end: https://www.tutorialspoint.com/display-images-on-terminal-using-python#:~:text=There%20are%20several%20Python%20libraries,%2C%20OpenCV%2C%20and%20ASCII%20Art.
# TODO https://pypi.org/project/tabulate/
# TODO remove any unused imports. 
# TODO check deployed version on heroku. Note differences for readme

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
        # Loading and introduction text to user
        heading = text2art('Zombie Bingo!', font="small")
        print(heading.center(80)) #why doesn't this work TODO fix center
        print(SEPARATE)
        print((f'{Fore.BLACK}{Back.LIGHTYELLOW_EX}Gathering the hottest info: please wait a moment...'))
        animation_loop(2)
        print('\n' + SEPARATE)
        print('Let\'s play bingo: how close is the zombie apocalypse according to the news? Guess the right key words and you win a point!') #TODO center and with border 
        print('\n' + SEPARATE)
        animation_loop(1)
    except KeyboardInterrupt as e:
        print(SEPARATE)
        print(f'\n{Fore.RED}Ouch! Don\'t poke me when I\'m booting up the program!')
        while True:
            print(SEPARATE)
            key_interrupt = input(f'Do you want to continue launching the game?\n{Fore.LIGHTYELLOW_EX}Type y or n:\n')
            if key_interrupt.lower() == 'y':
                print('\nCool, I\'ll start the game')
                os.system('clear') # add 'cls' parameter? CLear for Linux and MacOS? 
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
    except Exception as e:
        print(f'Error: {e.__traceback__}')
    finally:
        False # to prevent any uncaught while loop issues from KeyboardInterrupt.

def animation_loop(i): #TODO handle attribute error and value error - assign I as 3 seconds, exception 
    """
    Loading animation loop of rotating slashes.

    Credit: https://medium.com/@joloiuy/creating-captivating-terminal-animations-in-python-a-fun-and-interactive-guide-2eeb2a6b25ec
    """
    animation = "|/-\\"
    start_time = time.time()
    
    try:
        while True:
            for i in range(4):
                time.sleep(0.1)  # Feel free to experiment with the speed here
                sys.stdout.write("\r" + animation[i % len(animation)])
                sys.stdout.flush()
            if time.time() - start_time > i:  # The animation will last for {i} seconds
                break
        os.system('clear')
        sys.stdout
    except (AttributeError, ValueError):
        i = 3 # Defaults to 3 seconds if needed  
    except Exception as e:  
        print(f'General error occurred: {e.__traceback__}')   
def get_wordbank_list():  #TODO handle exception see last google import with links above
    """
    Returns all words in the wordbank as a list.
    """
    try:
        wordbank = SHEET.worksheet('wordbank').col_values(2)[1:] # write as a function instead

    except HttpError as err: #TODO handle exception
    # If the error is a rate limit or connection error,
    # wait and try again.
    if err.resp.status in [403, 500, 503]:
        time.sleep(5)
    else: raise
    
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
            
    #credit: https://www.secopshub.com/t/handling-api-errors-using-python-requests/589
    except requests.exceptions.HTTPError as errh: #TODO add snippet credit to Readme.
        return "An Http Error occurred:" + repr(errh)
    except requests.exceptions.ConnectionError as errc:
        return "An Error Connecting to the API occurred:" + repr(errc)
    except requests.exceptions.Timeout as errt:
        return "A Timeout Error occurred:" + repr(errt)
    except requests.exceptions.RequestException as err:
        return "An Unknown Error occurred" + repr(err)
    except Exception:
        print("An Unknown Error occurred")
        while True:
            user_response = input('Press 1 to try again, or 9 to use the preloaded headlines I cooked up yesterday')
            if user_response == 1:
                print('Trying again! Please hold...')
                get_headlines()
                break
            elif user_response == 9:
                print('OK! I\'ll use a precooked batch of headlines I have saved...\n')
                print('Please hold...')
                animation_loop()
                HEADLINES = test_get_headlines() #TODO does this work? Try when internet off
                break
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
    try:
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
    except  TypeError as e:
        pprint(f'String needed to process data. Data is currenctly {type(data)}.')
        raise e.with_traceback()
    except Exception as e:
        pprint(f'An error occurred while processing data. Please try again.')
        raise Exception
    return data

def find_list_intersections(list1, list2):  
    """
    Returns list of all intersections between list1 and list2.
    """
    try:
        intersections = set(list1).intersection(list2)
    except TypeError as e:
        pprint(f'List parameters must be list types: find_list_intersections function received: {type(list1)} and {type(list2)}.\nPlease try again.')
        raise e.with_traceback()
    except Exception:
        raise Exception(f'An error occurred while finding list intersections. Please try again.')
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
    except ValueError as e: 
        raise ValueError('Could not find words to remove. Check stopwords and worksheet connectivity.')
    except Exception as e:
        raise e.with_traceback()
    return data
    
def percentage_of_wordbank_matches(data):  #TODO handle ValueError, TypeError, Exception exception 
    """
    Returns percentage of matches between data and wordbank.
    This defines the percentage likelihood of apocalypse.
    """
    wordbank = SHEET.worksheet('wordbank').col_values(2)[1:] #TODO add as a function to avoid repeating this
    matches = find_list_intersections(wordbank, data)
    try:    
        #find percentage of wordbank matches
        # print(f'percentage = {len(matches)} divided by {len(wordbank)} * 100') #TODO remove this print statement before submit - only for testing
        percentage = len(matches) / (len(wordbank)) * 100
        percentage = math.floor(percentage)
    except ValueError as e:
        raise ValueError('Could not find wordbank matches. Check worksheet connectivity.')
    except ZeroDivisionError as e:
        raise ValueError('Zero division error')
        print(f'percentage = {len(matches)} divided by {len(wordbank)} * 100') # TODO confirm if works
    except Exception as e:
        print('An error occurred')
        raise e.with_traceback()
    return percentage

def get_wordbank_matches_list(data): #TODO handle exception, TypeError 
    """
    Returns list of wordbank matches.
    """
    wordbank = SHEET.worksheet('wordbank').col_values(2)[1:] #TODO use function to avoid repeating
    try:
        #find number of matches between data and wordbank 
        matches = find_list_intersections(wordbank, data)
    except TypeError as e:
        raise TypeError('Could not parse wordbank matches')
        print(f'{wordbank}, {data}') #TODO test - reachable?
    except Exception as e:
        raise e.with_traceback()   
    return matches
    
def update_worksheet_row(worksheet_name, values): #TODO handle exception generic 
    """
    Adds data to spreadsheet as a new row.
    """
    try:
        print(f'Updating {worksheet_name} worksheet...\n')
        SHEET.worksheet(worksheet_name).append_row(values) 
        print(f'{Fore.LIGHTGREEN_EX}{worksheet_name} worksheet successfully updated...\n')
        
    except TypeError as e:
        raise TypeError('data must be a list') and print(e.with_traceback()) #TODO sort so doesn't finish program, will ask to start again.

def update_worksheet_cell(worksheet_name, data): #TODO handle exception, API (RUntime?) error  
    """
    Adds data to spreadsheet as a new cell.
    """
    try:
        print(f'Updating {worksheet_name} worksheet...\n')
        SHEET.worksheet(worksheet_name).append_row(data) 
        print(f'{worksheet_name} worksheet successfully updated...\n')
        
    except TypeError as e:
        raise TypeError('data must not be a list') and print(e.with_traceback()) #TODO sort so doesn't finish program, will ask to start again.
        
def get_user_input1(): #TODO handle EOFError and ValueError here
    """
    Returns user input 1.
    """
    print(SEPARATE)
    print(f'{Fore.LIGHTRED_EX}Welcome pessimist.\n')
    print(f'{Fore.LIGHTRED_EX}{Back.LIGHTYELLOW_EX}How likely is doomsday today?')
    print('\nYour answer should be a number between 1 and 100.\n')
    print(f'{Style.DIM}Here\'s an example: 65\n')
    print(SEPARATE)
    while True:
        user_answer = input('\nEnter a number: ')
        if validate_user_input1(user_answer):
            print(f'{Fore.LIGHTGREEN_EX}Awesome, thanks.\n')
            break
    return user_answer
 
def validate_user_input1(user_input1): # TODO fix logic and loop. Handle generic Excepion errors
    """
    If user input is not an integer, or if number 
    is not between 0 and 100, raises exception.
    Returns boolean.
    """
    try:
        user_input1 = int(user_input1) #TODO fix. At moment if false, still returns true? Test and know how if else, except and better error handling work better    
        if user_input1 < 0 or user_input1 > 100:
            print('Woah woah, I said I number between 0 and 100. Check your math...')
    except (ValueError, TypeError):
            print(f'I need a number, silly!. You provided {type(user_input1)}')
            return False
    return True
    
def get_user_input2():#TODO Handle, Type, Value and generic Excepion errors
    """
    Returns user input 2 as list of strings.
    """
    print(SEPARATE)
    print('For some bonus points, enter 3 key words you think are in the news today\n')
    print(f'{Style.DIM}Here\'s an example: apocalypse, AI, mutation\n')
    print(SEPARATE)
    
    while True:
        input_data = input('Enter 3 key words: ')
        user_answer = input_data.split(',')
        
        # validate answer 
        if validate_user_input2(user_answer):
            break
    print(SEPARATE)
    print(f'{Fore.LIGHTGREEN_EX}Gotcha! Let me log your answers to my worksheets.\n')
    print(SEPARATE)
    return user_answer        
    
def validate_user_input2(user_input2): # TODO debug; handle type, value, exception errors
    """
    Raises error if user input is not a string, 
    or if total number of provided key words
    is not 3.
    """
    try:        
        if len(user_input2)!= 3:
            print(f'Please enter 3 key words, separated by commas.\n You entered: {len(user_input2)}\n')
            return False
    except ValueError as e:
        print(f'Invalid Type: {e.args}. Please enter 3 key words. Numbers are not allowed.\n')
        return False
    return True
def calculate_user_buzzword_points(keyword_list, user_list): #TODO: Handle type, value and generic Excepion errors
    """
    Find any matches between API headlines and user buzzwords.
    Generate score - one point per matched buzzword.
    Maximum of three points per turn.
    """
    matches_list = find_list_intersections(user_list, keyword_list)
    points = len(matches_list)
    return points

def calculate_user_percentage_score(user_input1, percentage):#TODO: Handle type, value and generic Excepion errors
    """
    If user is within 10% range of actual percentage, 
    return 1 point. Else return 0.
    """
    if user_input1 <= percentage + 10 and user_input1 >= percentage - 10:
        #1 point awarded to user
        return 1
    else:
        return 0

def get_user_scores_list(): #TODO: Handle type, API, timeout, value and generic Excepion error
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
def get_user_average_score(user_scores): #TODO: Handle type, value, ZeroDivisionError and generic Excepion error
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
        os.system('clear') # clear terminal
        main()
    else:
        print(f'{Fore.RESET}Thank you for playing!')
        exit() # terminate program

def main(): #TODO: Handle any leftover errors not handled in individual functions. 
    """
    Runs all program functions.
    """
    start_game()

    # headlines = get_headlines() # commented output for testing purposes, using testing headlines instead to avoid maxing API requests*****
    
    # main functions
    HEADLINES = test_get_headlines()
    processed_headlines = process_data(HEADLINES)
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
    user_percentage_score = calculate_user_percentage_score(int(answer1), percentage) #TODO test functions correctly
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
    print(f'{Fore.RED}{Style.BRIGHT}****  We are forcasting a {percentage}% chance of apocalypse today!  ****') # TODO add border and center? Or emoji?
    print(SEPARATE + '\n') 

    # play again y/n
    play_again()

if __name__ == '__main__':    
    main()

