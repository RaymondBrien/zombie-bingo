![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

## Reminders

- Your code must be placed in the `run.py` file
- Your dependencies must be placed in the `requirements.txt` file
- Do not edit any of the other files or your code may not deploy properly

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

---

# [ZOMBIE BINGO](https://zombie-bingo-a26c47d43c24.herokuapp.com)

🛑🛑🛑🛑🛑 START OF NOTES (to be deleted) 🛑🛑🛑🛑🛑



### Zombie Bingo 🧟‍♂️: A Thrilling Apocalypse Anticipation Game!
"Welcome to Zombie Bingo 🧟‍♂️, where the undead meet your news feed! Picture this: a thrilling blend of current events and apocalyptic anticipation. Our app scours the latest headlines for buzzwords, and your mission, should you choose to accept it, is to guess them right. Each correct guess earns you a point, but here's the twist: the more buzzwords you nail, the closer you get to determining the likelihood of the apocalypse—on a scale of 1 to 5. It's a race against time, wits, and the impending undead. Are you ready to bingo your way through the apocalypse?"

The target audience for Zombie Bingo includes:

1. **Game Enthusiasts**: Individuals who enjoy engaging and unique gaming experiences, especially those with a twist or unconventional theme.

2. **Pop Culture Fans**: People interested in zombies, apocalyptic scenarios, and pop culture references.

3. **News Junkies**: Those who stay updated with current events and enjoy incorporating them into their entertainment.

4. **Trivia and Word Game Players**: Fans of trivia and word games who enjoy challenges and testing their knowledge.

5. **Tech-Savvy Users**: Individuals comfortable with using apps and digital platforms for entertainment purposes.

6. **Age Range**: While Zombie Bingo can appeal to a broad age range, it may particularly attract younger adults and those with a penchant for humor and creativity.

Zombie Bingo 🧟‍♂️ offers a refreshingly unique gaming experience by blending current events with apocalyptic anticipation. By guessing buzzwords sourced from news headlines, players earn points and gauge the likelihood of an impending apocalypse—adding an exciting twist to traditional bingo gameplay. This app is perfect for game enthusiasts seeking something offbeat, pop culture fans intrigued by zombies and apocalyptic scenarios, news junkies looking to merge current events with entertainment, trivia and word game players eager for challenges, and tech-savvy users seeking engaging digital experiences. Whether you're craving a dose of fun, a challenge for your brain, or simply a break from the mundane, Zombie Bingo promises to deliver an entertaining and memorable gaming experience for all.

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

- **Wordbank List**

    - Details about this particular feature, including the value to the site, and benefit for the user. Be as detailed as possible!

![screenshot](documentation/feature01.png)

- **News Headlines API**

    - Details about this particular feature, including the value to the site, and benefit for the user. Be as detailed as possible!

![screenshot](documentation/feature02.png)

- **Text Processing**

    - To remove all punctuation and parse to lowercase characters.

![screenshot](documentation/feature03.png)

- **Keywords Finder**

    - Removes most common words using stopwords from the NLTK library and common words defined in the wordbank.

![screenshot](documentation/feature03.png)

- **Google Sheets API**

    - Adds user answers, points, maintains wordbank and API information directly from the terminal. Tables of data to use for google charts for data visualization.

![screenshot](documentation/featurex.png)

- **User input via terminal**

    - The user answers questions directly typing into the terminal.

![screenshot](documentation/featurex.png)

- **User feedback**

    - The user is prompted, kept informed of current processes running and when processes have successfully finished or raised an error.

![screenshot](documentation/featurex.png)

- **Game restart**

    - At the end of the game, the user is prompted to restart the game or finished the game.

![screenshot](documentation/featurex.png)

- **Game Answers**

    - After the user has answered both main questions, the game provides the game answers alongside the user's answers, with an aplocalypse probability based on the current headlines and their respective buzzwords.

![screenshot](documentation/featurex.png)

### Future Features

- Optional headline filtering via terminal
    - The user could add optional filters of criteria for the news API to use, including its main sources or number of results.
- Add further wordbank entries
    - Users could add additional stopwords and buzzwords to the wordbank to refine the game further, espeically if some words become more common over time due to media trends.
- Analytics and interpretation
    - At the end of each week, users will receive insights on their average point scores over time.

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
- [Google Charts](https://www.google.com...), used for...


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

🛑🛑🛑🛑🛑 END OF NOTES (to be deleted) 🛑🛑🛑🛑🛑

## Credits

<!-- In this section you need to reference where you got your content, media, and extra help from.
It is common practice to use code from other repositories and tutorials,
however, it is important to be very specific about these sources to avoid plagiarism. -->

<!-- - Stackoverflow (http://stackoverflow.com) (UPDATE URL): set find difference  -->




### Content

🛑🛑🛑🛑🛑 START OF NOTES (to be deleted) 🛑🛑🛑🛑🛑
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
| [Markdown Builder](https://tim.2bn.dev/markdown-builder) | README and TESTING | tool to help generate the Markdown files |
<!-- | [strftime](https://strftime.org) | CRUD functionality | helpful tool to format date/time from string | -->
<!-- | [WhiteNoise](http://whitenoise.evans.io) | entire site | hosting static files on Heroku temporarily | -->

### Media

<!-- 🛑🛑🛑🛑🛑 START OF NOTES (to be deleted) 🛑🛑🛑🛑🛑

Use this space to provide attribution links to any images, videos, or audio files borrowed from online.
A few examples have been provided below to give you some ideas.

If you're the owner (or a close acquaintance) of all media files, then make sure to specify this.
Let the assessors know that you have explicit rights to use the media files within your project.

Ideally, you should provide an actual link to every media file used, not just a generic link to the main site!
The list below is by no means exhaustive. Within the Code Institute Slack community, you can find more "free media" links
by sending yourself the following command: `!freemedia`. -->

| Source | Location | Type | Notes |
| --- | --- | --- | --- |
| [Pexels](https://www.pexels.com) | entire site | image | favicon on all pages |
| [Audio Micro](https://www.audiomicro.com/free-sound-effects) | game page | audio | free audio files to generate the game sounds |


### Acknowledgements

<!-- Use this space to provide attribution to any supports that helped, encouraged, or supported you throughout the development stages of this project.
A few examples have been provided below to give you some ideas. -->

- I would like to thank my Code Institute mentor, [Tim Nelson](https://github.com/TravelTimN) for their support throughout the development of this project.
- I would like to thank the [Code Institute](https://codeinstitute.net) tutor team for their assistance with troubleshooting and debugging some project issues.
- I would like to thank the [Code Institute Slack community](https://code-institute-room.slack.com) for the moral support; it kept me going during periods of self doubt and imposter syndrome.
- I would like to thank my partner (John/Jane), for believing in me, and allowing me to make this transition into software development.


