""" Entry point """

import sys

from controllers.tournament_manager import TournamentManager, OngoingTournamentManager
from controllers.player_creator import PlayerCreator
from controllers.player_updater import PlayerUpdater

from views.main_menu import MainMenuView
from views.report_menu import ReportMenuView


""" Instanciate the main menu view """
main_menu = MainMenuView()

""" Instanciate controllers according to the user input """
main_menu_user_choice = main_menu.choice
if main_menu_user_choice == 1:
    """Create tournament"""
    tournament_manager = TournamentManager()
elif main_menu_user_choice == 2:
    """Load ongoing tournament"""
    ongoing_tournament_manager = OngoingTournamentManager()
elif main_menu_user_choice == 3:
    """Save new player to database"""
    player_creator = PlayerCreator()
elif main_menu_user_choice == 4:
    """Update player's ranking"""
    player_updater = PlayerUpdater()
elif main_menu_user_choice == 5:
    """Generate reports"""
    report_menu_view = ReportMenuView()
elif main_menu_user_choice == 6:
    """Exit the program"""
    sys.exit()
else:
    print("Veuillez réessayer.")
