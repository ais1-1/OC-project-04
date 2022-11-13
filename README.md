# Chess Tournament Manager - CTM

This is a project done as part of my degree program at Openclassrooms.

It manages tournaments and players for a chess club. Running the project will give you access to the main menu. The main menu contains the following options :
1. Créer un tournoi
    This option will allow you to create a new tournament. Then the program will generate rounds and matches according to the information that are given by the user. The matches are generated following the swiss tournament system. At the end of each round, one needs to enter the winners and the date and time of the end of the round.
2. Charger un tournoi en cours
    This option is to load an ongoing tournament.
3. Ajouter des joueurs
    This is to add players to the database. Note that you need a few players in the first place to conduct a tournament.
4. Modifier le classement des joueurs
    This allows to modify the ranking of players.
5. Voir les rapports
    This allows to generate reports related to players and a tournament.
6. Quitter l'application
    This quits the program.

## Create a virtual environment

Requirement : Python3.3 or later

Open terminal at the root of the project directory, and enter the following command:

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

This will install all the required modules to run the python script.

## Execute the python script

In your terminal inside the project directory:

    python main.py

