""" Define the main menu view """
import sys

from views.report_menu import ReportMenuView

from controllers.tournament_manager import TournamentManager, OngoingTournamentManager
from controllers.player_creator import PlayerCreator
from controllers.player_updater import PlayerUpdater


MENU_OPTIONS = {
    1: "Créer un tournoi",
    2: "Charger un tournoi en cours",
    3: "Ajouter des joueurs",
    4: "Modifier le classement des joueurs",
    5: "Voir les rapports",
    6: "Quitter l'application",
}


TITLE = "CTM - Chess Tournament Manager"
TITLE_DECO = "*******************************"


class MainMenuView:
    """MainMenuView class"""

    def __init__(self):
        """Init the following attribute:
        choice - choice of the user from the MENU_OPTIONS (1 to 6)

        Init methods:
        display_menu - display the available options with title
        get_user_selection - user prompt"""
        self.choice = ""
        self.display_menu()
        self.get_user_selection()

    def display_menu(self):
        """Display the main menu with the title of the program."""
        print(TITLE_DECO)
        print(TITLE)
        print(TITLE_DECO)
        for key in MENU_OPTIONS.keys():
            print(key, " : ", MENU_OPTIONS[key])

    def get_user_selection(self):
        """Display the user input section to enter a choice
        and return the choice."""
        self.choice = 0

        while self.choice > 6 or self.choice <= 0:
            try:
                self.choice = int(input("Saisissez votre choix : "))
                if self.choice > 6 or self.choice <= 0:
                    raise Exception
                else:
                    pass
            except Exception:
                print(
                    "Veuillez entrer un nombre entre 1 et 6"
                    + " pour indiquer votre choix"
                )

        if self.choice == 1:
            """Create tournament"""
            TournamentManager()
        elif self.choice == 2:
            """Load ongoing tournament"""
            OngoingTournamentManager()
        elif self.choice == 3:
            """Save new player to database"""
            PlayerCreator()
        elif self.choice == 4:
            """Update player's ranking"""
            PlayerUpdater()
        elif self.choice == 5:
            """Generate reports"""
            ReportMenuView()
        elif self.choice == 6:
            """Exit the program"""
            sys.exit()
        else:
            print(
                "Veuillez entrer un nombre entre 1 et 6" + " pour indiquer votre choix"
            )
            self.choice = 0
