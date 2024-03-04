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
from art import text2art
from pyboxen import boxen
from rich.table import Table

colorama.init(autoreset=True)  # auto-reset color for each new line

# always centers text at 80 chars wide.
CENT = "{:^80}".format

# global variable to avoid repeating
SEPARATE = CENT('\n' + '* * * * *' + '\n')


# TODO ADD LINTER SCREENSHOT BEFORE SUBMITTING AFTER ALL COMMENTS REMOVED
# TODO add boxen credits to readme 
# TODO update requirements  
# TODO remove user full answer print to termianl in main
# TODO ENSURE ALL TODOS removed before submitting
# TODO remove commented out sections from testing

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
        # Clear terminal for terminal readability
        os.system('clear')
        heading = text2art(('Zombie Bingo!'), font="small")
        
        # Loading and introduction text to user
        print(f'{Fore.GREEN}\n{heading}{Fore.RED}o==[]::::::::::::::>\n')

        # User-initialized game start
        # boxen credit: https://github.com/savioxavier/pyboxen?tab=readme-ov-file
        print(
            boxen(
                "How close is the zombie apocalypse according to the news?\n",
                "Guess the right key words and you win a point!",
                title="[black on cyan] What is it? [/]",
                subtitle="*** LET'S PLAY ***",
                subtitle_alignment="center",
                color="yellow",
                padding=1,
            )
        )

        print(f'{Style.DIM}(Press ctrl + c to exit){Style.RESET_ALL}\n')
        input('Press enter to continue...')
        print(
            f'\n{Fore.BLACK}{Back.LIGHTYELLOW_EX}Gathering the hottest info:{Back.RESET}\n'
            f'{Style.DIM}please wait a moment...\n{Style.RESET_ALL}')
        animation_loop(2)
    # keyboard interrupt handling
    except KeyboardInterrupt as e:
        print(SEPARATE)
        print(
            f'\n{Fore.RED}** Ouch! **\n'
            'Don\'t poke me when I\'m booting up the program!\n')
        while True:
            print(SEPARATE)
            key_interrupt = input(
                'Do you want to continue launching the game?\n'
                F'{Fore.LIGHTYELLOW_EX}Type y or n:\n{Fore.RESET}')
            if key_interrupt.lower() == 'y':
                print('\nCool, I\'ll start the game')
                animation_loop(2)  # give user time to read
                os.system('clear')
                start_game()
                break
            elif key_interrupt.lower() == 'n':
                print(f'{Fore.RESET}\nOk, I\'ll close the game! See you soon!\n')
                False
                sys.exit(0)
            elif key_interrupt.lower() != 'y' and key_interrupt.lower() != 'n':
                print(
                    f'Please enter either y or n.'
                    f'{Fore.LIGHTYELLOW_EX}You wrote: {key_interrupt}')
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

    Credit:
    Medium @joloiuy - see README for details.
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
        else:
            raise RuntimeError(
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
        "to_date": "28/02/2024",
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
            # ensures only title text returned
            title_collection.append(news_item['title'])
    # credit ln 174-183: secopshub.com for requests exceptions below.
    # See readme.md for details.
    except requests.exceptions.HTTPError as errh:
        return "An Http Error occurred:" + repr(errh)
    except requests.exceptions.ConnectionError as errc:
        return "An Error Connecting to the API occurred:" + repr(errc)
    except requests.exceptions.Timeout as errt:
        return "A Timeout Error occurred:" + repr(errt)
    except requests.exceptions.RequestException as err:
        return "An Unknown Error occurred" + repr(err)
    except Exception:
        print(
            '\nHello there: rapid API has a cap on the number of requests...\n'
            'Looks like the requests are maxed out or another error occurred\n'
            '\nI have taken the liberty of handling this for you '
            'with some preloaded headlines\n'
            f'{SEPARATE}')
        while True:
            try:
                user_response = int(input(
                    f'{Fore.LIGHTYELLOW_EX}Type 1 if you want to try using '
                    'rapid API try again\n'
                    f'\n{Fore.LIGHTGREEN_EX}Type 9 to use the preloaded headlines '
                    f'I cooked up yesterday\n{Fore.RESET}\n'))
                if user_response == 1:
                    print('Trying again!')
                    get_headlines()
                    break
                elif user_response == 9:
                    print(
                        '\nOK!\n'
                        'I\'ll use a precooked batch of headlines I made earlier...\n')  # noqa
                    print(
                        f'{SEPARATE}'
                        '\nPlease hold...\n'
                        'The screen will clear and then ask you the first question!')
                    animation_loop(8)
                    global _headlines
                    _headlines = test_get_headlines()
                    title_collection = _headlines
                    break
            except ValueError:
                print('\nPlease enter 1 or 9')
    return title_collection


def test_get_headlines():  # backup headlines
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
        print(f'String needed to process data. Data is currently \
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
        print(f'List parameters must be list types: \
            find_list_intersections function received: {type(list1)} \
                and {type(list2)}.\nPlease try again.')
        raise e.with_traceback()
    except Exception:
        raise Exception(
            'An error occurred while finding list intersections.'
            'Please try again.')
    return intersections


def remove_common_words(data):
    """
    Returns string list with common words removed.
    """
    common_words = SHEET.worksheet('wordbank').col_values(3)[1:]
    try:
        # find all words in data that are not in common_words
        words_to_remove = find_list_intersections(common_words, data)
        data = [word for word in data if word not in stopwords.words('english') and word not in words_to_remove]  # noqa
    except ValueError as e:
        raise ValueError(
            'Could not find words to remove.'
            'Check stopwords and worksheet connectivity.')
    except Exception as e:
        raise e.with_traceback()
    return data


def percentage_of_wordbank_matches(data):
    """
    Returns percentage of matches between data and wordbank.
    This defines the percentage likelihood of apocalypse.
    """
    wordbank = SHEET.worksheet('wordbank').col_values(2)[1:]
    matches = find_list_intersections(wordbank, data)
    try:
        # find percentage of wordbank matches
        percentage = len(matches) / (len(wordbank)) * 100
        percentage = math.floor(percentage)
    except ValueError as e:
        raise ValueError(
            'Could not find wordbank matches.'
            'Check worksheet connectivity.')
    except ZeroDivisionError as e:
        raise ValueError('Zero division error')
    except Exception as e:
        print('An error occurred')
        raise e.with_traceback()
    return percentage


def get_wordbank_matches_list(data):
    """
    Returns list of wordbank matches.
    """
    wordbank = SHEET.worksheet('wordbank').col_values(2)[1:]
    try:
        # find number of matches between data and wordbank
        matches = find_list_intersections(wordbank, data)
    except TypeError as e:
        print(f'{wordbank}, {data}')
        raise TypeError('Could not parse wordbank matches')
    except Exception as e:
        raise e.with_traceback()
    return matches


def update_worksheet_row(worksheet_name, values):
    """
    Adds data to spreadsheet as a new row.
    """
    try:
        SHEET.worksheet(worksheet_name).append_row(values)
    except TypeError as e:
        print('Data must be a list: please check')
        while True:
            user_response = input('Would you like to try again? y/n\n')
            if user_response == 'y'.lower():
                print('Trying again! Please hold...')
                animation_loop(2)
                update_worksheet_row(worksheet_name, values)
                break
            elif user_response == 'n'.lower():
                print('Ok. Clearing...')
                animation_loop(2)
                sys.stdout.flush()
                os.system('clear')
                break
    except Exception as e:
        print(
            'An error occurred.'
            'Check your internet connection and error details below:\n')
        raise e.with_traceback()


def update_worksheet_cell(worksheet_name, data):
    """
    Adds data to spreadsheet as a new cell.
    """
    try:
        SHEET.worksheet(worksheet_name).append_row(data)
    except TypeError as e:
        raise TypeError(
            f'Data must be a list.'
            f'When updating worksheet cell it was: {type(data)}')
    except Exception as e:
        print(
            f'An error occurred. Check your internet connection'
            f'error details:\n{e.with_traceback}')
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


def get_user_input1():
    """
    Returns user input 1.
    """
    print(SEPARATE)
    print(
        f'{Fore.LIGHTRED_EX}Welcome pessimist.\n'
        'I have two questions for you.')
    print(SEPARATE)
    print(
        boxen(
            "[red on yellow] How likely is doomsday today?\n",
            "* * * * *\n",
            "Your answer should be a number between 0 and 100.",
            "Enter 0 if you think the world is in perfect harmony.",
            "Enter 100 if the earth is burning",
            title="[black on cyan] QUESTION 1 [/]",
            subtitle="Here\'s an example: 65",
            subtitle_alignment="center",
            color="yellow",
            padding=1,
        )
    )

    while True:
        user_answer = input('Enter a number: ')
        if validate_user_input1(user_answer):
            print(f'{Fore.LIGHTGREEN_EX}Awesome, thanks.\n')
            animation_loop(3)  # ensures user sees answer is received
            os.system('clear')
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
        try:  # try converting to integer
            user_input1 = int(user_input1)
            if user_input1 < 0 or user_input1 > 100:
                print(
                    'Woah, I said I number between 0 and 100.\n'
                    'Check your math...')
                return False
        except ValueError:
            print(f'I need a number, silly! You provided \
                {type(user_input1)}\n')
            return False
        except EOFError as e:
            print(
                f'EOF Error occurred: {e.with_traceback}.'
                'I\'ll have to restart to make some space...')
            main()  # restarts game
        except Exception as e:
            raise Exception(f'Unknown error occurred: {e.with_traceback}')
    return True


def get_user_input2():
    """
    Returns user input 2 as list of strings.
    """
    print(SEPARATE)
    print(
        boxen(
            "[red on yellow] Enter 3 key words you think are in the news today?\n",
            "* * * * *\n",
            "I\'ll check your answers against the top headlines from today.",
            "Each correct word will get you a juicy point, so choose wisely...\n",
            "* * * * *\n",
            "Separate each by a comma like the example below.\n",
            title="[black on cyan] QUESTION 2 [/]",
            subtitle="Example: apocalypse, AI, mutation",
            subtitle_alignment="center",
            color="yellow",
            padding=1,
        )
    )

    while True:
        input_data = input('Enter 3 key words: ')
        user_answer = [x.strip() for x in input_data.split(',')]
        # validate answer
        if validate_user_input2(user_answer):
            break
    print(SEPARATE)
    print(
        f'{Fore.LIGHTGREEN_EX}Gotcha!\n'
        'Logging your answers to my spreadsheets.\n')
    print('\nHang on just a moment...\n')
    animation_loop(3)
    print(SEPARATE)
    os.system('clear')  # clear terminal due to Heroku clear
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
        print(
            f'You only gave me {len(user_input2)} answer(s).'
            'Or you forgot to add commas. Check and try again.\n')
        print(
            'Please enter 3 key words'
            'Remember to separate each by a comma.')
        print(f'{Style.DIM}Here\'s an example: apocalypse, AI, mutation\n')
        return False
    else:
        try:
            # check if all items in user_input2 list are words
            results = list(filter(lambda word: not word[1], map(lambda word: (word, word.isalpha()), user_input2)))  # noqa
            for result in results:
                print(f'{Fore.RED}{result[0]} is not valid')
                return False
        except ValueError as e:
            print(
                f'Invalid Type: {e.args}.'
                'Please enter 3 key words. Numbers are not allowed.\n')
            return False
        except TypeError as e:
            print(
                f'Please only use words.\n'
                f'You wrote: {user_input2}'
                f'which is type {type(user_input2)}.\n'
                'Please enter 3 key words.\n'
                'Remember numbers and symbols are not allowed.\n')
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
        raise ValueError(
            f'Invalid Value: {e.args}. Please enter 3 key words.'
            'Numbers are not allowed.\n')
    except TypeError as e:
        raise TypeError(
            f'Invalid Type: {e.args}. Please enter 3 key words.'
            'Numbers are not allowed.\n')
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

        if user_input1 in range(percentage - 10, percentage + 10):
            # 1 point awarded to user
            return 1
        else:
            return 0
    except ValueError as e:
        raise ValueError(
            f'Invalid Value: {e.args}. Please enter 3 key words.'
            'Numbers are not allowed.\n')
    except TypeError as e:
        raise TypeError(f'Invalid Type: {e.args}. Please enter 3 key words.'
                        'Numbers are not allowed.\n')
    except Exception as e:
        raise Exception(f'Unknown error occurred: {e.with_traceback}')


def get_user_scores_list():
    """
    Gets column data from user scores logged from each time
    user completes game.
    """
    try:
        sheet_values = SHEET.worksheet('end_calculator').col_values(2)[1:]
        user_scores = []
        for value in sheet_values:
            value = int(value)
            user_scores.append(value)
    except TypeError as e:
        print(
            f'Error getting user scores.'
            f'This is what I got: {sheet_values}')
        raise TypeError(
            f'Invalid Type: {e.args}\n.'
            'Check sheet values from worksheet as well as internet connection')
    except TimeoutError as e:
        print(
            f'Timeout Error: {e}.\n.Check your internet connection.'
            'I\'ll try again if I have a connection now...')
        animation_loop(1)
        get_user_scores_list()
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
        print(
            f'{Fore.LIGHTRED_EX}Issue calculating your average score.'
            'Your score has not been counted.\n')
        print(
            f'User scores came back as: {user_scores}.'
            'Check your internet connection if this doesn\'t look right...')
    except TypeError as e:
        raise TypeError(
            f'Invalid Type: {e.args}.'
            'User scores came back as {type(user_scores)}\n')
    except Exception as e:
        raise Exception(f'Unknown error occurred: {e.with_traceback}')
    return math.floor(score)


def play_again():
    """
    Starts program again if y.
    Finishes program if n.
    Handles if user input invalid.
    """
    answer = input(
        'Would you like to play again? '
        f'({Fore.GREEN}y{Fore.WHITE}/{Fore.RED}n{Fore.WHITE}): \n')
    try:
        if answer.lower() == 'y':
            os.system('clear')
            main()
        elif answer.lower() == 'n':
            print(
                f'{Fore.RESET}Thank you for playing!\n'
                'Be sure to check back tomorrow with tomorrow\'s headlines.\n'
                'Who knows, maybe there\'s a real apocalypse tomorrow...')
            animation_loop(10)  # give user time to read
            os.system('clear')
            exit()  # terminate program
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

    global _headlines  # global if API call fails, so test headlines used.
    _headlines = get_headlines()
    processed_headlines = process_data(_headlines)
    keyword_list = remove_common_words(processed_headlines)
    percentage = percentage_of_wordbank_matches(keyword_list)
    headline_matches = get_wordbank_matches_list(keyword_list)

    animation_loop(1)

    # concatenate program answers for easy worksheet parsing
    program_full_answer = list(str(percentage)) + list(headline_matches)

    # get user answers
    answer1 = get_user_input1()
    answer2 = get_user_input2()

    # concatenate user answers for easy worksheet parsing
    user_full_answer = [answer1] + answer2

    # calculate scores
    user_matches = calculate_user_buzzword_points(answer2, headline_matches)
    user_percentage_score = calculate_user_percentage_score(int(answer1), percentage)  # noqa
    user_total_score = user_matches + user_percentage_score
    scores_history = get_user_scores_list()
    average_score = get_user_average_score(scores_history)
    end_results = [percentage, user_total_score]

    # update worksheets
    update_worksheet_row('program_answers', program_full_answer)
    update_worksheet_row('user_answers', user_full_answer)
    update_worksheet_cell('end_calculator', end_results)

    # report info to terminal for user
    print(
        boxen(
            "* * * * *\n",
            f"[red on yellow] WE ARE FORECASTING A {percentage} CHANCE OF APOCALYPSE TODAY! \n",
            "* * * * *\n",
            title="[black on cyan] RESULTS [/]",
            subtitle="[red] o==[]::::::::::::::> [/]",
            subtitle_alignment="center",
            color="yellow",
            padding=1,
        )
    )

    # results table
    table = Table(show_header=True, header_style="bold magenta")
    
    table.add_column("Your Answers", style="yellow", width=12)
    table.add_column("Today's Key Words", style="red")
    table.add_column("Your Total Score", justify="right")
    table.add_column("Other People's Average Score", justify="right")
    table.add_row(
        f"{user_full_answer}", 
        f"{headline_matches}", 
        f"{user_total_score}", 
        f"{average_score}"
    )

    print(
        boxen(
            "Results:\n",
            table
        )
    )
        

    # play again y/n
    play_again()


# prevent file name appearing before program is run on heroku
os.system('clear')
print('launching Zombie Bingo')
# maintain readable terminal on heroku
os.system('clear')
if __name__ == '__main__':
    main()
