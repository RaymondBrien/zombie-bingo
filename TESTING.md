# Testing

Return back to the [README.md](README.md) file.

## Code Validation

<!-- 
It's recommended to validate each file using the API URL.
This will give you a custom URL which you can use on your testing documentation.
It makes it easier to return back to a file to validate it again in the future.
Use the steps above to generate your own custom URLs for each Python file.

**IMPORTANT**: `E501 line too long` errors

You must strive to fix any Python lines that are too long ( >80 characters ).
In rare cases where you cannot break the lines [without breaking the functionality],
then by adding `# noqa` to the end of those lines will ignore linting validation.

`# noqa` = **NO Quality Assurance**

**NOTE**: You must include 2 *spaces* before the `#`, and 1 *space* after the `#`.

Do not use `# noqa` all over your project just to clear down validation errors!
This can still cause a project to fail, for failing to fix actual PEP8 validation errors.

Sometimes strings or variables get too long, or long `if` conditional statements.
These are acceptable instances to use the `# noqa`.

When trying to fix "line too long" errors, try to avoid using `/` to split lines.
A better approach would be to use any type of opening bracket, and hit Enter just after that.

Any opening bracket type will work: `(`, `[`, `{`.

By using an opening bracket, Python knows where to appropriately indent the next line of code,
without having to "guess" yourself and attempt to tab to the correct indentation level.

Sample Python code validation documentation below (tables are extremely helpful!).
-->

I have used the recommended [PEP8 CI Python Linter](https://pep8ci.herokuapp.com) to validate all of my Python files.

| File | CI URL | Screenshot | Notes |
| --- | --- | --- | --- |
| run.py | 
[PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/RaymondBrien/zombie-bingo/main/run.py) | 
![screenshot](documentation/py-validation-run.png) | 
xxxxxxxxx |

| x | x | x | repeat for all remaining Python files |



## Defensive Programming
<!-- 


PP3 (Python-only):
- Users must enter a valid letter/word/string when prompted
- Users must choose from a specific list only -->

<!-- You should include any manual tests performed, and the expected results/outcome.

Testing should be replicable.
Ideally, tests cases should focus on each individual section of every page on the website.
Each test case should be specific, objective, and step-wise replicable. -->

<!-- Instead of adding a general overview saying that everything works fine,
consider documenting tests on each element of the page
(ie. button clicks, input box validation, navigation links, etc.) by testing them in their happy flow,
and also the bad/exception flow, mentioning the expected and observed results,
and drawing a parallel between them where applicable. -->

<!-- Consider using the following format for manual test cases:

Expected Outcome / Test Performed / Result Received / Fixes Implemented

- **Expected**: "Feature is expected to do X when the user does Y."
- **Testing**: "Tested the feature by doing Y."
- (either) **Result**: "The feature behaved as expected, and it did Y."
- (or) **Result**: "The feature did not respond to A, B, or C."
- **Fix**: "I did Z to the code because something was missing." -->


Defensive programming was manually tested with the below user acceptance testing:

| Section | Expectation | Test | Result | Fix | Screenshot |

| --- | --- | --- | --- | --- | --- |

| Start | | x |x |x | ![screenshot](documentation/feature01a.jpeg) |
| Start | x| x |x |x | ![screenshot](documentation/feature01b.png) |
| Q1 | x| x |x |x | ![screenshot](documentation/feature01.png) |
| Q1 | x| x |x |x | ![screenshot](documentation/feature01.png) |
| Q1 | x| x |x |x | ![screenshot](documentation/feature01.png) |
| Q1 | x| x |x |x | ![screenshot](documentation/feature01.png) |
| Q2 | x| x |x |x | ![screenshot](documentation/feature01.png) |
| Q2 | x| x |x |x | ![screenshot](documentation/feature01.png) |
| Q2 | x| x |x |x | ![screenshot](documentation/feature01.png) |
| Q2 | x| x |x |x | ![screenshot](documentation/feature01.png) |
| Q2 | x| x |x |x | ![screenshot](documentation/feature01.png) |
| End | x| x |x |x | ![screenshot](documentation/feature01.png) |
| End | x| x |x |x | ![screenshot](documentation/feature01.png) |
| End | x| x |x |x | ![screenshot](documentation/feature01.png) |

1
Landing page - DONE
Pressing enter starts the game
Press enter when instructed
The Game started as expected
No fix required.

2
Landing page - DONE
Ctrl C will confirm if user wants to leave the game. If not, the game will continue.

---
3
Question 1 - DONE
Only will accept number. Will prompt user to try again if not a number (for example if a letter or symbol was used).

4
Question 1 - DONE
Will accept two-digit numbers as well as single digit numbers (e.g. 72 or 3). 

5
Question 1 - TO FIX 
Only will accept number between 0 and 100. Will prompt user to try again if not within range.

6
Question 1 - DONE 
If format is correct, user will receive confirmation that answer has been received and will move on to question 2.

---
7
Question 2
If user does not put in three words, user will be prompted again to put in three words.

8
Question 2
Answers must be separated by commas. If they are not separated by commas, user will be prompted again.

9
Question 2
User cannot use numbers or symbols. If user uses numbers or symbols, user will be prompted again.

10
Question 2
If one answer within their three words is not valid, the incorrect answer will highlighted to the user and the user will be prompted to try again.

11
Question 2
If answer is in correct format, user will receive confirmation that: their answer has been logged; that their information is being logged to a spreadsheet.


---

12
End of Game
When user is asked 'Would you like to play again?', if 'y' is selected, the terminal will clear and the program will run again.

13
End of Game
When user is asked 'Would you like to play again?', if 'n' is selected, the program will finish after printing 'thank you for playing'.

14
End of Game
When user is asked 'Would you like to play again?', if the user does not press 'y' or 'n' then the program will prompt the user to type only 'y' or 'n'. If no input is provided then the program will sleep after 2 minutes.


## Bugs
<!-- 
This section is primarily used for JavaScript and Python applications,
but feel free to use this section to document any HTML/CSS bugs you might run into.

It's very important to document any bugs you've discovered while developing the project.
Make sure to include any necessary steps you've implemented to fix the bug(s) as well.

**PRO TIP**: screenshots of bugs are extremely helpful, and go a long way! -->


- Python `'ModuleNotFoundError'` when trying to import module from imported package

    ![screenshot](documentation/bug03.png)

    - To fix this, I _____________________.


- Python `E501 line too long` (93 > 79 characters)

    ![screenshot](documentation/bug04.png)

    - To fix this, I _____________________.

## Unfixed Bugs

<!-- You will need to mention unfixed bugs and why they were not fixed.
This section should include shortcomings of the frameworks or technologies used.
Although time can be a big variable to consider, paucity of time and difficulty understanding
implementation is not a valid reason to leave bugs unfixed.

If you've identified any unfixed bugs, no matter how small, be sure to list them here.
It's better to be honest and list them, because if it's not documented and an assessor finds the issue,
they need to know whether or not you're aware of them as well, and why you've not corrected/fixed them. -->


- For PP3, when using a helper `clear()` function, any text above the height of the terminal does not clear, and remains when you scroll up.

    ![screenshot](documentation/unfixed-bug02.png)

    - Attempted fix: I tried to adjust the terminal size, but it only resizes the actual terminal, not the allowable area for text.


<!-- 

If you legitimately cannot find any unfixed bugs or warnings, then use the following sentence: -->



There are no remaining bugs that I am aware of.
