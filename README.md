# Chess Tournament Manager - CTM

This is a project done as part of my degree program at Openclassrooms.

It manages tournaments and players for a chess club. 

Running the project will give you access to the main menu. The main menu contains the following options :
1. Créer un tournoi :

    This option allows you to create a new tournament. Then the program will generate rounds and matches according to the information that are given by the user. The matches are generated following the swiss tournament system. At the end of each round, one needs to enter the winners of each match and the date and time of the end of the round.
2. Charger un tournoi en cours :

    This option is to load an ongoing tournament.
3. Ajouter des joueurs :

    This is to add players to the database. Note that you need a few players in the first place to conduct a tournament.
4. Modifier le classement des joueurs :

    This allows to modify the ranking of players.
5. Voir les rapports :

    This allows to generate reports related to players and a tournament.
6. Quitter l'application :

    This quits the program.

## Create a virtual environment

Requirement : Python3.3 or later

Open a terminal at the root of the project directory, and enter the following command:

    python -m venv <name of the virtual environment>

For example:

    python -m venv env

This will create a directory named *env* inside your project directory.

## Activate the virtual environment

In the project directory, open a terminal and enter the following command:

    source <name of the virtual environment>/bin/activate

## Install dependencies

Again, inside the project directory, in your terminal, enter the following command:

    pip install -r requirements.txt

This will install all the required modules to run the application. Those are tinydb, flake8 and flake8-html.

## Launch the application

With the virtual environment activated, in your terminal inside the project directory:

    python main.py

## Generate flake8-html report

In your terminal at the root of the project directory enter the following command:

    flake8 --format=html --htmldir=flake-report

This will generate new html flake8 reports inside the directory called flake-report. The file setup.cfg in the project directory has set maximum line length to 119 and it excludes .git, .gitignore, __pycache__, env and venv. If your venv is named differently than env or venv, you can its name in the setup.cfg.
