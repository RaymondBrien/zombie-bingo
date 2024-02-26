![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

<!-- - Your dependencies must be placed in the `requirements.txt` file -->

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

---

# [ZOMBIE BINGO](https://zombie-bingo-a26c47d43c24.herokuapp.com)

### Zombie Bingo 🧟‍♂️: A Thrilling Apocalypse Anticipation Game!
"Welcome to Zombie Bingo 🧟‍♂️, where doomsday joins your news feed! Picture this: a thrilling blend of current events and apocalyptic anticipation in a scintillating yet simple game package in your terminal. The app scours the latest headlines for key words, and your mission, should you choose to accept it, is to guess them right, alongside guessing how likely doomsday is today. Each correct guess earns you a point, but here's the twist: the more buzzwords you nail, the closer you get to determining the likelihood of the apocalypse—on a scale of 0 to 100. It's a race against time, wits, and the impending doom ahead. Are you ready to bingo your way through the apocalypse?"

The target audience for Zombie Bingo includes:

1. **Game Enthusiasts**: Individuals with terminal access who enjoy engaging and unique gaming experiences, especially those with a twist or unconventional theme.

2. **Culture Fans**: People interested in the news, apocalyptic scenarios, and contemporary headline references.

3. **News Junkies**: Those who stay updated with current events and enjoy incorporating them into their entertainment.

4. **Trivia and Word Game Enthusiasts**: Fans of trivia and word games who enjoy challenges and testing their knowledge.

5. **Tech-Savvy Users**: Individuals comfortable with using the terminal on their respective devices, even if just for silly entertainment purposes.

6. **Age Range**: While Zombie Bingo can appeal to a broad age range, it may particularly attract younger adults and those with a penchant for humor, coding and creativity.

Zombie Bingo 🧟‍♂️ offers a humorous, succinct gaming experience by blending current events with apocalyptic anticipation. By guessing key words sourced from news headlines, players earn points and gauge the likelihood of an impending apocalypse, adding an exciting twist of actually being based on real life headlines gathered freshly each time the game is run. This game is perfect for pessimists, game enthusiasts seeking something offbeat, contemporary culture fans intrigued by apocalyptic scenarios, news junkies looking to merge current events with entertainment, trivia and word game players eager for challenges, and tech-savvy users seeking something silly and fun as a digital experience. Whether you're craving a dose of fun, a challenge for your brain, or simply a quick break from the mundane, Zombie Bingo promises to deliver an entertaining and memorable, brief experience for all.

<!-- https://ui.dev/amiresponsive?url=https://zombie-bingo-a26c47d43c24.herokuapp.com

Screenshots for the README and testing should not be inside of `assets/` or `static/` image folders.
(reminder: `assets/` and `static/` are for files used on the live site, not documentation)
Consider adding a new folder called `documentation`, and add the amiresponsive screenshot inside of that folder.
To add the image into your README, use this format:
(assuming you have a new folder called `documentation` with an image called "mockup.png") -->

<!-- ![screenshot](documentation/mockup.png)

Note: Markdown files (.md) should not contain HTML elements like `img`, `br`, `div`, `a`, etc, only Markdown formatting.
Find out more about using Markdown elements here:
https://pandao.github.io/editor.md/en.html -->


## UX

## Features

<!-- In this section, you should go over the different parts of your project,
and describe each in a sentence or so.

You will need to explain what value each of the features provides for the user,
focusing on who this website is for, what it is that they want to achieve,
and how your project is the best way to help them achieve these things.

For some/all of your features, you may choose to reference the specific project files that implement them.

IMPORTANT: Remember to always include a screenshot of each individual feature! -->

### Existing Features

- **News Headlines API**

    - Details about this particular feature, including the value to the site, and benefit for the user. Be as detailed as possible!
<!-- ADD SCREENSHOT -->
![screenshot](documentation/feature02.png)

- **Keywords Finder**

    - Removes most common words using stopwords from the NLTK library and common words defined in the wordbank.
<!-- ADD SCREENSHOT -->
![screenshot](documentation/feature03.png)

- **Google Sheets API**

    - Adds user answers, points, maintains word bank and API information directly from the terminal. Tables of data to check any time.
<!-- ADD SCREENSHOT -->
![screenshot](documentation/featurex.png)

- **User input via terminal**

    - The user answers questions directly typing into the terminal.
<!-- ADD SCREENSHOT -->
![screenshot](documentation/featurex.png)

- **User feedback**

    - The user is prompted, kept informed of current processes running and when processes have successfully finished or raised an error.
<!-- ADD SCREENSHOT -->
![screenshot](documentation/featurex.png)

- **Game restart**

    - At the end of the game, the user is prompted to restart the game or finished the game.
<!-- ADD SCREENSHOT -->
![screenshot](documentation/featurex.png)

- **Game Answers**

    - After the user has answered both main questions, the game provides the game answers alongside the user's answers, with an apocalypse probability based on the current headlines and their respective buzzwords.
<!-- ADD SCREENSHOT -->
![screenshot](documentation/featurex.png)

- **Average Score**

    - ...
<!-- ADD SCREENSHOT -->
![screenshot](documentation/featurex.png)

### Future Features

- Optional headline filtering via terminal
    - The user could add optional filters of criteria for the news API to use, including which country the program sources headlines from, or the number of results.
- Add further word bank entries
    - Users could add additional key words they think are relevant over time to impending doom, to refine the game further, especially if some words become more common over time due to media trends.
- Analytics and interpretation
    - At the end of each week, users might receive insights on their average point scores over time, represented in fun and visual ways with google charts or graphics.
- Add sound effects when results are printed
    - At the end of each game, a sound is played to add additional user feedback for improved UX. This was not possible at the current time of deployment due to issues with static file handling in Heroku.

## Tools & Technologies Used

<!-- UPDATE LINKS -->
- [Python](https://www.python.org) used as the back-end programming language.
- [Git](https://git-scm.com) used for version control. (`git add`, `git commit`, `git push`)
- [GitHub](https://github.com) used for secure online code storage.
- [Heroku](https://www.heroku.com) used for hosting the deployed back-end site.
- [Gspread](https://www.google.com...) used for...
- [Google Sheets](https://www.google.com...), used for...
- [NewsNowAPI](https://rapidapi.com/rphrp1985/api/newsnow), used for gathering a list of contemporary headlines from top news sites.
- [Google Cloud](https://www.google.com...), used for...


## Data Model

### Flowchart

To follow best practice, a flowchart was created for the app's logic,
and mapped out before coding began using
[Freeform](https://www.apple.com/uk/newsroom/2022/12/apple-launches-freeform-a-powerful-new-app-designed-for-creative-collaboration/).

Below is the flowchart of the main process of this Python program. It shows the entire cycle of the program.

![screenshot](documentation/flowchart.png)

### Classes & Functions

<!-- The program uses classes as a blueprint for the project's objects (OOP). This allows for the object to be reusable.

```python
class Person:
    """ Insert docstring comments here """
    def __init__(self, name, age, health, inventory):
        self.name = name
        self.age = age
        self.health = health
        self.inventory = inventory
``` -->

The primary functions used on this application are: 
<!-- UPDATE THIS FURTHER -->

- `get_headlines()`
    <!-- - Get sales figures input from the user. -->
- `process_data()`
    <!-- - Converts all string values into integers. -->
- `remove_common_words()`
    <!-- - Update the relevant worksheet with the data provided. -->
- `percentage_of_wordbank_matches()`
    <!-- - Compare sales with stock and calculate the surplus for each item type. -->
- `get_wordbank_matches_list()`
    <!-- - Collects columns of data from sales worksheet.
- `get_user_input()`
    <!-- -  Calculate the average stock for each item type, adding 10%. -->
- `update_worksheet_cell()`
    <!-- -  Calculate the average stock for each item type, adding 10%. -->
- `update_worksheet_row()`
    <!-- -  Calculate the average stock for each item type, adding 10%. -->
- `calculate_user_buzzword_points()`
    <!-- -  Calculate the average stock for each item type, adding 10%. -->
- `calculate_user_percentage_score()`
    <!-- -  Calculate the average stock for each item type, adding 10%. -->
- `play_again()`
    <!-- -  Calculate the average stock for each item type, adding 10%. -->
- `main()`
    - Run all program functions.

### Imports

I've used the following Python packages and/or external imported packages.

- `gspread`: used with the Google Sheets API
- `google.oauth2.service_account`: used for the Google Sheets API credentials
- `json' : used with the Google Sheets API
- 'requests' : used with the NewsNow API
- `os`: used for adding a `clear()` function
- `colorama`: used for including color in the terminal
- `nltk`: used for stopwords to remove generic works from news headlines
<!-- - 're' -->
<!-- - 'inflect' -->
- 'math': to create clear percentage calculations with math.floor
<!-- TODO add updated list here -->


## Testing

For all testing, please refer to the [TESTING.md](TESTING.md) file.

## Deployment

Code Institute has provided a [template](https://github.com/Code-Institute-Org/python-essentials-template) to display the terminal view of this backend application in a modern web browser.
This is to improve the accessibility of the project to others.

The live deployed application can be found deployed on [Heroku](https://zombie-bingo-a26c47d43c24.herokuapp.com).

<!-- CHECK THIS LINK ABOVE WORKS -->

### Heroku Deployment

This project uses [Heroku](https://www.heroku.com), a platform as a service (PaaS) that enables developers to build, run, and operate applications entirely in the cloud.

Deployment steps are as follows, after account setup:

- Select **New** in the top-right corner of your Heroku Dashboard, and select **Create new app** from the dropdown menu.
- Your app name must be unique, and then choose a region closest to you (EU or USA), and finally, select **Create App**.
- From the new app **Settings**, click **Reveal Config Vars**, and set the value of KEY to `PORT`, and the value to `8000` then select *add*.
- If using any confidential credentials, such as CREDS.JSON, then these should be pasted in the Config Variables as well.
- Further down, to support dependencies, select **Add Buildpack**.
- The order of the buildpacks is important, select `Python` first, then `Node.js` second. (if they are not in this order, you can drag them to rearrange them)

Heroku needs two additional files in order to deploy properly.

- requirements.txt
- Procfile

You can install this project's **requirements** (where applicable) using:

- `pip3 install -r requirements.txt`

If you have your own packages that have been installed, then the requirements file needs updated using:

- `pip3 freeze --local > requirements.txt`

The **Procfile** can be created with the following command:

- `echo web: node index.js > Procfile`

For Heroku deployment, follow these steps to connect your own GitHub repository to the newly created app:

Either:

- Select **Automatic Deployment** from the Heroku app.

Or:

- In the Terminal/CLI, connect to Heroku using this command: `heroku login -i`
- Set the remote for Heroku: `heroku git:remote -a app_name` (replace *app_name* with your app name)
- After performing the standard Git `add`, `commit`, and `push` to GitHub, you can now type:
	- `git push heroku main`

The frontend terminal should now be connected and deployed to Heroku!

### Local Deployment

This project can be cloned or forked in order to make a local copy on your own system.

For either method, you will need to install any applicable packages found within the *requirements.txt* file.

- `pip3 install -r requirements.txt`.

If using any confidential credentials, such as `CREDS.json` or `env.py` data, these will need to be manually added to your own newly created project as well.

#### Cloning

You can clone the repository by following these steps:

1. Go to the [GitHub repository](https://github.com/RaymondBrien/zombie-bingo) 
2. Locate the Code button above the list of files and click it 
3. Select if you prefer to clone using HTTPS, SSH, or GitHub CLI and click the copy button to copy the URL to your clipboard
4. Open Git Bash or Terminal
5. Change the current working directory to the one where you want the cloned directory
6. In your IDE Terminal, type the following command to clone my repository:
	- `git clone https://github.com/RaymondBrien/zombie-bingo.git`
7. Press Enter to create your local clone.

Alternatively, if using Gitpod, you can click below to create your own workspace using this repository.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/RaymondBrien/zombie-bingo)

Please note that in order to directly open the project in Gitpod, you need to have the browser extension installed.
A tutorial on how to do that can be found [here](https://www.gitpod.io/docs/configure/user-settings/browser-extension).

#### Forking

By forking the GitHub Repository, we make a copy of the original repository on our GitHub account to view and/or make changes without affecting the original owner's repository.
You can fork this repository by using the following steps:

1. Log in to GitHub and locate the [GitHub Repository](https://github.com/RaymondBrien/zombie-bingo)
2. At the top of the Repository (not top of page) just above the "Settings" Button on the menu, locate the "Fork" Button.
3. Once clicked, you should now have a copy of the original repository in your own GitHub account!

### Local VS Deployment

<!-- Use this space to discuss any differences between the local version you've developed, and the live deployment site on Heroku. -->
...
...
...

## Credits

### Content

<!-- 
Use this space to provide attribution links to any borrowed code snippets, elements, or resources.
A few examples have been provided below to give you some ideas.

Ideally, you should provide an actual link to every resource used, not just a generic link to the main site! -->

| Source | Location | Notes |
| --- | --- | --- |
| [Markdown Builder](https://tim.2bn.dev/markdown-builder) | README and TESTING | tool to help generate the Markdown files |
| [Tech with Tim](https://www.youtube.com/watch?v=u51Zjlnui4Y) | terminal styling | tutorial on using colorama to add colors to terminal |
| [Medium](https://medium.com/@joloiuy/creating-captivating-terminal-animations-in-python-a-fun-and-interactive-guide-2eeb2a6b25ec) | Loading animations | blog post on animations in the terminal |
| [StackOverflow](https://stackoverflow.com/questions/3462143/get-difference-between-two-lists-with-unique-entries) | Finding differences function | forum on effective difference checker methods between lists |
| [StackOverflow](https://stackoverflow.com/questions/9953619/technique-to-remove-common-wordsand-their-plural-versions-from-a-string) | text processing functions | forum on usage of stopwords to process text to remove common words with nltk |
| [Medium](https://medium.com/analytics-vidhya/deploying-nlp-model-on-heroku-using-flask-nltk-and-git-lfs-eed7d1b22b11) | nltk functions | debugging nltk stopword package errors when deploying to heroku |
| [ASCII](https://www.ascii-art.site/) | heading art | program name art used throughout program |
| [StackOverflow](https://stackoverflow.com/questions/423379/how-to-use-a-global-variable-in-a-function) | global variable usage throughout program | how to reassign global variables to ensure the backup pre-loaded headlines work if headlines API call fails due to internet connection issues or maxing out API requests |
<!-- https://stackoverflow.com/questions/22029562/python-how-to-make-simple-animated-loading-while-process-is-running -->
| [Stanford](https://cs.stanford.edu/people/nick/py/python-map-lambda.html) | input2 error handling | using lambda to more efficiently loop and find invalid values and only print the invalid ones to the terminal for an improved user experience.|


### Media

| Source | Location | Type | Notes |
| --- | --- | --- | --- |
| [Pixabay Sound Effect](https://pixabay.com/sound-effects/wrong-answer-126515/) | main function for poor answers | audio clip | free sound effect. Used when printing results at the end of the game to terminal.This was |


### Acknowledgements

- I would like to thank my Code Institute mentor, [Tim Nelson](https://github.com/TravelTimN) for their support throughout the development of this project.
- I would like to thank the [Code Institute](https://codeinstitute.net) tutor team for their assistance with troubleshooting and debugging some project issues.
- I would like to thank the [Code Institute Slack community](https://code-institute-room.slack.com) for the moral support; it kept me going during periods of self doubt and imposter syndrome.
- I would like to thank my partner (John/Jane), for believing in me, and allowing me to make this transition into software development.


