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
from art import text2art
# https://googleapis.dev/python/google-api-core/latest/exceptions.html
# https://stackoverflow.com/questions/23945784/how-to-manage-google-api-errors-in-python

colorama.init(autoreset=True)  # auto-reset color for each new line

# global variable to avoid repeating 
SEPARATE = ('----------------------------------------------------------------\n').center(80)

# TIM checks:
# TODO API exceptions ok?
# TODO any classes I could implement? 
# TODO ensure happy will meet all marking criteria
# TODO loading whilst running functions? https://stackoverflow.com/questions/22029562/python-how-to-make-simple-animated-loading-while-process-is-running
# TODO centering issue and line breaks

# ESSENTIAL TODOs: 
# TODO ADD LINTER SCREENSHOT BEFORE SUBMITTING AFTER ALL COMMENTS REMOVED
# TODO refactor by using function decorators directly above function def for printing running tests or uploading something (see screenshot)
# TODO check text formatting in heroku no spillover
# TODO ENSURE ALL TODOS removed before submitting
# TODO remove any unused imports.
# TODO make sure only one number is allowed for q1
# TODO remove commented out sections from readme
# TODO remove commented out sections from testing
# TODO make all questions, input text prompts and elements consistent in their styling.

# OTHER:
# TODO tabulate final data points in main so looks nice in terminal. Or write as a function?
# TODO NOT IMPORTANT https://pypi.org/project/tabulate/


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
    try: # TODO check tim example for text align using function and see github page mutiple print statements
        opening_text = (
            f'{SEPARATE}{Fore.BLACK}{Back.LIGHTYELLOW_EX}WELCOME TO ZOMBIE BINGO{Style.RESET_ALL}{SEPARATE}Let\'s play bingo: how close is the zombie apocalypse according to the news?\nGuess the right key words and you win a point!\n{Style.DIM}(Press ctrl + c to exit){Style.RESET_ALL}\n{SEPARATE}')
        # Clear terminal for terminal readability
        os.system('clear')
        # Loading and introduction text to user
        heading = text2art(('Zombie Bingo!').center(20), font="small")
        print(f'{Fore.GREEN}{heading}')
        print((f'{Fore.RED}o==[]::::::::::::::>').center(40))
        print(opening_text.center(25))
        input('Press enter to continue...').center(25)
        print(f'{Fore.BLACK}{Back.LIGHTYELLOW_EX}Gathering the hottest info: please wait a moment...')
        animation_loop(2)
    except KeyboardInterrupt as e:
        print(SEPARATE)
        print(f'\n{Fore.RED}Ouch! Don\'t poke me when I\'m booting up the program!')
        while True:
            print(SEPARATE)
            key_interrupt = input(
                f'Do you want to continue launching the game?\n{Fore.LIGHTYELLOW_EX}Type y or n:\n')  # noqa
            if key_interrupt.lower() == 'y':
                print('\nCool, I\'ll start the game')
                os.system('clear')
                start_game()
                break
            elif key_interrupt.lower() == 'n':
                print('\nOk, I\'ll close the game! See you soon!\n')
                False
                sys.exit(0)
            elif key_interrupt.lower() != 'y' and key_interrupt.lower() != 'n':  
                print(
                    f'Please enter either y or n. {Fore.LIGHTYELLOW_EX}You wrote: {key_interrupt}')  # noqa
    except ImportError as e:
        print(f'Import Error: {e.args}')
    except RuntimeError as e:
        print(f'Runtime Error: {e.args}')
    except Exception as e:
        print(f'Error: {e.with_traceback}')
    finally:
        False  # backup to safely handle while loop 


def animation_loop(sec):
    """
    Loading animation loop of rotating slashes.

    Credit: https://medium.com/@joloiuy/creating-captivating-\
        terminal-animations-in-python-a-fun-and-interactive-guide-\
            2eeb2a6b25ec
    """
    animation = "|/-\\"
    start_time = time.time()

    try:
        while True:
            for i in range(4):
                time.sleep(0.1)  # speed of animation
                sys.stdout.write("\r" + animation[i % len(animation)])
                sys.stdout.flush()
            if time.time() - start_time > sec:  # duration of {i} seconds
                break
        os.system('clear')
        sys.stdout
    except (AttributeError, ValueError):
        sec = 3  # Defaults to 3 seconds if needed
    except Exception as e:
        print(f'General error occurred: {e.__traceback__}')


def get_wordbank_list():
    """
    Returns all words in the wordbank as a list.
    """
    try:
        wordbank = SHEET.worksheet('wordbank').col_values(2)[1:]

    except Exception as e:
        # If the error is a connection error, wait and try again.
        if e.message in [403, 500, 503]:
            time.sleep(5)
        else: raise RuntimeError(
            f'Error: {e.with_traceback}: please restart the game.\n')
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
            title_collection.append(news_item['title'])  # ensures only title text returned
    # credit secopshub.com for requests exceptions below. See readme.md for details
    # except requests.exceptions.HTTPError as errh:
    #     return "An Http Error occurred:" + repr(errh)
    # except requests.exceptions.ConnectionError as errc:
    #     return "An Error Connecting to the API occurred:" + repr(errc)
    # except requests.exceptions.Timeout as errt:
    #     return "A Timeout Error occurred:" + repr(errt)
    # except requests.exceptions.RequestException as err:
    #     return "An Unknown Error occurred" + repr(err)
    except Exception:
        print("An Unknown Error occurred")
        while True:
            try:
                user_response = int(input('Press 1 to try again, or 9 to use the \
                    preloaded headlines I cooked up yesterday'))
                if user_response == 1:
                    print('Trying again!')
                    get_headlines()
                    break
                elif user_response == 9:
                    print('OK! I\'ll use a precooked batch of headlines I have \
                        saved...\n')
                    print('Please hold...')
                    animation_loop(2)
                    global _headlines
                    _headlines = test_get_headlines() # TODO does this work? Try when internet off
                    title_collection = _headlines
                    break
            except ValueError:
                print('Please enter 1 or 9')
    return title_collection


def test_get_headlines():
    """
    FOR TESTING PURPOSES ONLY TO AVOID MAXING OUT API REQUESTS.
    Used as backup if headlines API fails / no internet connection.
    """
    title_collection = 'Global Leaders Convene for Climate Summit; chaos \
        destruction survival desolation catastrophePledge Action on \
        Climate Change. Tech Giants Unveil New Innovations at Annual \
        Conference, Economic Uncertainty Looms as Stock Markets \
        Fluctuate, Health Experts Warn of Potential New Wave \
        of Pandemic Cases. Renewable Energy Surges, Outpacing Fossil \
        Fuel Investments, Political Turmoil Erupts in Region, Raising \
        Concerns for Stability. Breakthrough in Medical Research Offers \
        Hope for Rare Diseases, Education Sector Faces Challenges Amidst \
        Shift to Online Learning. Space Exploration Reaches New Heights \
        with Successful Satellite Launch, Environmentalists Rally for \
        Conservation Efforts in Face of Biodiversity Loss.'
    return title_collection


def process_data(data):
    """
    Returns string list all lowercase, with punctuation removed.
    Turns any ints into version (e.g. 1 -> 'one').
    """
    data = str(data)
    try:
        # remove punctuation
        data = re.sub(r'[^\w\s]', '', data)
        data = data.lower()
        data = data.split()

        # turn any int within text into words
        for word in data:
            if word is int:
                word = inflect.engine().number_to_words(word)
                data = ' '.join(data)
            data = list(data)
    except TypeError as e:
        pprint(f'String needed to process data. Data is currently \
            {type(data)}.')
        raise e.with_traceback()
    except Exception as e:
        raise Exception(
            'An error occurred while processing data. Please try again.')
    return data


def find_list_intersections(list1, list2):
    """
    Returns list of all intersections between list1 and list2.
    """
    try:
        intersections = set(list1).intersection(list2)
    except TypeError as e:
        pprint(f'List parameters must be list types: \
            find_list_intersections function received: {type(list1)} \
                and {type(list2)}.\nPlease try again.')
        raise e.with_traceback()
    except Exception:
        raise Exception('An error occurred while finding list \
            intersections. Please try again.')
    return intersections


def remove_common_words(data):
    """
    Returns string list with common words removed.
    """
    common_words = SHEET.worksheet('wordbank').col_values(3)[1:]  # TODO make a function to avoid repeating this
    try:
        # find all words in data that are not in common_words
        words_to_remove = find_list_intersections(common_words, data)
        data = [word for word in data if word not in stopwords.words('english') and word not in words_to_remove]
    except ValueError as e:
        raise ValueError('Could not find words to remove. \
            Check stopwords and worksheet connectivity.')
    except Exception as e:
        raise e.with_traceback()
    return data


def percentage_of_wordbank_matches(data):
    """
    Returns percentage of matches between data and wordbank.
    This defines the percentage likelihood of apocalypse.
    """
    wordbank = SHEET.worksheet('wordbank').col_values(2)[1:]  # TODO add as a function to avoid repeating this
    matches = find_list_intersections(wordbank, data)
    try:
        # find percentage of wordbank matches
        percentage = len(matches) / (len(wordbank)) * 100
        percentage = math.floor(percentage)
    except ValueError as e:
        raise ValueError('Could not find wordbank matches. \
            Check worksheet connectivity.')
    except ZeroDivisionError as e:
        raise ValueError('Zero division error')  # TODO confirm if works
    except Exception as e:
        print('An error occurred')
        raise e.with_traceback()
    return percentage


def get_wordbank_matches_list(data):
    """
    Returns list of wordbank matches.
    """
    wordbank = SHEET.worksheet('wordbank').col_values(2)[1:] #TODO use function to avoid repeating
    try:
        #find number of matches between data and wordbank
        matches = find_list_intersections(wordbank, data)
    except TypeError as e:
        print(f'{wordbank}, {data}')
        raise TypeError('Could not parse wordbank matches')
    except Exception as e:
        raise e.with_traceback()
    return matches


def update_worksheet_row(worksheet_name, values): # TODO add google API error handling once correctly imported see import list above
    """
    Adds data to spreadsheet as a new row.
    """
    try:
        print(f'Updating {worksheet_name} worksheet...\n')
        SHEET.worksheet(worksheet_name).append_row(values)
        print(f'{Fore.LIGHTGREEN_EX}{worksheet_name} worksheet successfully updated...\n')
    except TypeError as e:
        print('Data must be a list: please check')
        while True:
            user_response = input('Would you like to try again? y/n\n')
            if user_response == 'y'.lower():
                print('Trying again! Please hold...')
                animation_loop()
                update_worksheet_row(worksheet_name, values)
                break
            elif user_response == 'n'.lower():
                print('Ok. Clearing...')
                animation_loop()
                sys.stdout.flush()
                os.system('clear')
                break
    except Exception as e:
        print('An error occured. Check your internet connection and error details below:\n')
        raise e.with_traceback()


def update_worksheet_cell(worksheet_name, data): # TODO add google API error handling once correctly imported see import list above
    """
    Adds data to spreadsheet as a new cell.
    """
    try:
        print(f'Updating {worksheet_name} worksheet...\n')
        SHEET.worksheet(worksheet_name).append_row(data)
    except TypeError as e:
        raise TypeError(
            f'Data must be a list. When updating worksheet cell it was: {type(data)}') #TODO sort so doesn't finish program, will ask to start again.
    except Exception as e:
        print(f'An error occured. Check your internet connection and \
            error details below:\n{e.with_traceback}')
        while True:
            user_response = input('Would you like to try updating \
                worksheet again? y/n\n')
            if user_response == 'y'.lower():
                print('Trying again! Please hold...')
                animation_loop(1)
                update_worksheet_cell(worksheet_name, data)
                break
            elif user_response == 'n'.lower():
                print('Ok. Clearing...')
                animation_loop(1)
                sys.stdout.flush()
                os.system('clear')
                break


def get_user_input1(): # TODO 
    """
    Returns user input 1.
    """
    print(SEPARATE)
    print(
        f'{Fore.LIGHTRED_EX}Welcome pessimist. I have two questions for you.\n')
    print(f'{Fore.LIGHTRED_EX}{Back.LIGHTYELLOW_EX}Question 1: \
        {Style.BRIGHT}How likely is doomsday today?\n')
    print(f'{Style.NORMAL}Your answer should be a number between 0 and \
        100.\nEnter 0 if you think the world is in perfect \
            harmony.\nEnter 100 if Earth is burning\n')
    print(f'{Style.DIM}Here\'s an example: 65\n')
    print(SEPARATE)

    while True:
        user_answer = input('Enter a number: ')
        if validate_user_input1(user_answer):
            print(f'{Fore.LIGHTGREEN_EX}Awesome, thanks.\n')
            os.system('clear')  # clear needed to keep TODO add to testing as heroku known clear bug - more clears needed to keep tidy
            break
    return user_answer


def validate_user_input1(user_input1):
    """
    If user input is not an integer, or if number
    is not between 0 and 100, raises exception.
    Returns boolean. Handles empty answers.
    """
    # first check if answer given
    if user_input1 == '':
        print('Please enter a number')
        return False
    else:
        try: # try converting to integer
            user_input1 = int(user_input1)
            if user_input1 < 0 or user_input1 > 100:
                print(
                    'Woah, I said I number between 0 and 100.\nCheck your math...')
                return False
        except ValueError:
            print(f'I need a number, silly! You provided \
                {type(user_input1)}\n')
            return False
        except EOFError as e:
            print(f'EOF Error occurred: {e.with_traceback}. \
                I\'ll have to restart to make some space...') 
            main() # restarts game
        except Exception as e:
            raise Exception(f'Unknown error occurred: {e.with_traceback}')
    return True


def get_user_input2():
    """
    Returns user input 2 as list of strings.
    """
    print(SEPARATE)
    print(f'{Fore.LIGHTRED_EX}{Back.LIGHTYELLOW_EX}Question 2:')
    print(f'{Style.BRIGHT}Enter 3 key words you think are in the news today, each separated by a comma like the example below\n')
    print(f'{Style.NORMAL}I\'ll check your answers against the top \
        headlines from today.\nEach word you get right will get you a \
            juicy point so choose wisely.\n')
    print(f'{Style.DIM}Here\'s an example: apocalypse, AI, mutation\n')
    print(SEPARATE)
    while True:
        input_data = input('Enter 3 key words: ')
        # user_answer = input_data.split(',')
        user_answer = [x.strip() for x in input_data.split(',')]
        # validate answer
        if validate_user_input2(user_answer):
            break
    print(SEPARATE)
    print(
        f'{Fore.LIGHTGREEN_EX}Gotcha! Logging your answers to my spreadsheets.')
    print('Hang on just a moment...\n')
    print(SEPARATE)
    return user_answer


def validate_user_input2(user_input2):
    """
    Raises error if user input is not a string,
    or if total number of provided key words
    is not 3.
    """
    # first check if user input is correct amount of words
    if len(user_input2) != 3:
        print(SEPARATE)
        print(f'You only gave me {len(user_input2)} answer(s) or forgot to add commas...')
        print('Please enter 3 key words, remembering to separate each by a comma.')
        print(f'{Style.DIM}Here\'s an example: apocalypse, AI, mutation\n')
        return False
    else:
        try: 
            # check if all items in user_input2 list are words
            results = list(filter(lambda word: not word[1], map(lambda word: (word, word.isalpha()), user_input2)))  # noaq
            for result in results:
                print(f'{Fore.RED}{result[0]} is not valid')
                return False
        except ValueError as e:
            print(f'Invalid Type: {e.args}. Please enter 3 key words. \
                Numbers are not allowed.\n')
            return False
    

        except TypeError as e:
            print(f'Please only use words.\nYou wrote: {user_input2} which \
                is type {type(user_input2)}.\nPlease enter 3 key words. \
                    Numbers and symbols are not allowed.\n')
        except ValueError as e:
            print(f'Invalid Type: {e.args}. Please enter 3 key words. \
                Numbers are not allowed.\n')
            return False
        except Exception as e:
            raise Exception(f'Unknown error occurred: {e.with_traceback}')
    return True


def calculate_user_buzzword_points(keyword_list, user_list):
    """
    Find any matches between API headlines and user key words.
    Generate score - one point per matched key word.
    Maximum of three points per turn.
    """
    try:
        matches_list = find_list_intersections(user_list, keyword_list)
        points = len(matches_list)
    except ValueError as e:
        raise ValueError(f'Invalid Value: {e.args}. Please enter 3 key \
            words. Numbers are not allowed.\n')
    except TypeError as e:
        raise TypeError(f'Invalid Type: {e.args}. Please enter 3 key words. \
            Numbers are not allowed.\n')
    except Exception as e:
        raise Exception(f'Unknown error occurred: {e.with_traceback}')
    return points


def calculate_user_percentage_score(user_input1, percentage):
    """
    Ensures both user_input1 and percentage are integers.
    If user is within range of actual percentage,
    return 1 point. Else return 0 points.
    Points will be added to total score count.
    """
    try:
        user_input1 = int(user_input1)
        percentage = int(percentage)

        if user_input1 in range(percentage - 10, percentage + 10)
            #1 point awarded to user
            return 1
        else:
            return 0
    except ValueError as e:
        raise ValueError(f'Invalid Value: {e.args}. Please enter 3 key \
            words. Numbers are not allowed.\n')
    except TypeError as e:
        raise TypeError(f'Invalid Type: {e.args}. Please enter 3 key words. \
            Numbers are not allowed.\n')
    except Exception as e:
        raise Exception(f'Unknown error occurred: {e.with_traceback}')


def get_user_scores_list(): #TODO: Handle API error
    """
    Gets column data from user scores logged from each time
    user completes game.
    """
    try:
        sheet_values = SHEET.worksheet('end_calculator').col_values(2)[1:] # TODO avoid repetition with function instead
        user_scores = []
        for value in sheet_values:
            value = int(value)
            user_scores.append(value)
    except TypeError as e:
        print(f'Error getting user scores. This is what I got: \
            {sheet_values}')
        raise TypeError(f'Invalid Type: {e.args}\n.Check sheet values \
            from end_calculator worksheet as well as internet connection') # TODO are e.args useful here? Or e.with_traceback or something else more helpful?
    except TimeoutError as e:
        pprint(f'Timeout Error: {e}.\n.Check your internet connection. \
            I\'ll try again if I have a connection now...') # TODO test timeout
        animation_loop(1)
        get_user_scores_list() # TODO will this stop the program even if successful? Is there a method to retry that part of main?
    except Exception as e:
        raise Exception(f'Unknown error occurred: {e.with_traceback}')
    return user_scores


def get_user_average_score(user_scores):
    """
    Returns average score for user from all games played.
    """
    try:
        score = sum(user_scores) / len(user_scores)
    except ZeroDivisionError:
        score = 0
        print(f'{Fore.LIGHTRED_EX}There was an issue calculating your \
            average score. Your score has not been counted.\n')
        print(f'User scores came back as: {user_scores}. Check your \
            worksheet and internet connection if this doesn\'t look right...')
    except TypeError as e:
        raise TypeError(f'Invalid Type: {e.args}. User scores came back \
            as {type(user_scores)}\n')
    except Exception as e:
        raise Exception(f'Unknown error occurred: {e.with_traceback}')
    return math.floor(score)


def play_again():
    """
    Starts program again if y.
    Finishes program if n.
    Handles if user input invalid.
    """
    answer= input(f'Would you like to play again? {Fore.LIGHTBLACK_EX}({Fore.GREEN}y{Fore.LIGHTBLACK_EX}/{Fore.RED}n{Fore.LIGHTBLACK_EX}): ')
    try:
        if answer.lower() == 'y':
                os.system('clear')
                main()
        elif answer.lower() == 'n':
            print(f'{Fore.RESET}Thank you for playing!')
            exit() # terminate program
        else:
            print(f'{Fore.LIGHTRED_EX}Please enter y or n.')
            play_again()
    except ValueError as e:
        raise ValueError(f'Invalid Value: {e.args}. Please enter y or n.')



def main(): 
    """
    Runs all program functions.
    """
    start_game()

    global _headlines 
    _headlines = get_headlines() # TODO put back in before submitting: commented output for testing purposes, using testing headlines instead to avoid maxing API requests*****

    # global _headlines
    # _headlines = test_get_headlines() # TODO sort before submitting
    processed_headlines = process_data(_headlines)
    keyword_list = remove_common_words(processed_headlines)
    percentage = percentage_of_wordbank_matches(keyword_list)
    headline_matches = get_wordbank_matches_list(keyword_list) 

    # TODO Add animation loop whilst functions above are running to keep user updated - see link below
    # https://stackoverflow.com/questions/22029562/python-how-to-make-simple-animated-loading-while-process-is-running
    animation_loop(1)

    # concatenate program answers for easy worksheet parsing
    program_full_answer = list(str(percentage)) + list(headline_matches)

    # get user answers
    answer1 = get_user_input1()
    answer2 = get_user_input2()

    # concatenate user answers for easy worksheet parsing
    print(answer1)
    user_full_answer = [answer1] + answer2
    print(f'user full answer: {user_full_answer}')

    # calculate scores
    user_matches = calculate_user_buzzword_points(answer2, headline_matches)
    user_percentage_score = calculate_user_percentage_score(int(answer1), percentage) #TODO test functions correctly
    user_total_score = user_matches + user_percentage_score
    scores_history = get_user_scores_list()
    average_score = get_user_average_score(scores_history)
    end_results = [percentage, user_total_score]

    # update worksheets
    update_worksheet_row('program_answers', program_full_answer)
    update_worksheet_row('user_answers', user_full_answer) 
    update_worksheet_cell('end_calculator', end_results)

    # report info to terminal for user
    print(SEPARATE)
    print(f'{Fore.GREEN}Your answers: {user_full_answer}\n') 
    print(f'{Fore.RED}Today\'s keywords in the news headlines were:\n{Fore.LIGHTYELLOW_EX}{headline_matches}')
    print(f'You won: {user_total_score} point(s)\n')
    print(f'Your average score is: {average_score} point(s)')
    print(SEPARATE + '\n')
    print(f'{Fore.RED}{Style.BRIGHT}****  We are forecasting a {percentage}% chance of apocalypse today!  ****')
    print(SEPARATE + '\n')

    # play again y/n
    play_again()



# clear()
# launching zombie bingo 
# clear 
if __name__ == '__main__':
    main()
