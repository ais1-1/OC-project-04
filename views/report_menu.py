""" Define report menu views"""
import sys
from controllers.database_handler import DatabaseHandler
from views.helper import display_prompt_after_selection

REPORTMENU_OPTIONS = {
    1: "Les joueurs",
    2: "Les tournois",
    3: "Quitter l'application",
}

PLAYER_REPORT_OPTIONS = {
    1: "Par ordre alphabétique",
    2: "Par classement",
    3: "Retourner au menu précédent",
}

TOURNAMENT_REPORT_MAIN_OPTIONS = {
    1: "Liste de tous les tournois",
    2: "Rapport spécifique à un tournoi",
    3: "Retourner au menu précédent",
}

TOURNAMENT_REPORT_OPTIONS = {
    1: "Liste de tous les joueurs du tournoi",
    2: "Liste de tous les tours du tournoi",
    3: "Liste de tous les matchs du tournoi",
    4: "Retourner au menu précédent",
}


class ReportMenuView:
    """ReportMenuView class"""

    def __init__(self):
        """Init method:
        display_menu - prompt for user to choose"""
        self.display_menu()

    def display_menu(self):
        """Display prompt for user to choose from given options"""
        print("------------------")
        print("VOIR LES RAPPORTS")
        print("------------------")
        choice = ""

        for key in REPORTMENU_OPTIONS.keys():
            print(key, " : ", REPORTMENU_OPTIONS[key])

        try:
            choice = int(input("Saisissez votre choix : "))
        except Exception:
            print(
                "Veuillez entrer un nombre entre 1 et 4" + " pour indiquer votre choix"
            )

        if choice == 1:
            """Show player's report menu"""
            PlayerReportMenuView()
        elif choice == 2:
            """Show tournament specific menu"""
            TournamentReportMenuView()
        elif choice == 3:
            """Exit the programme"""
            sys.exit()
        else:
            """Show a message in the case of invalid entry"""
            print("!!!Choix invalide." + " Veuillez entrer un nombre entre 1 et 3 !!!")
            self.display_menu()


class PlayerReportMenuView:
    """PlayerReportMenuView class"""

    def __init__(self):
        """Init attribute:
        db_handler - instance of DatabaseHandler

        Init method:
        display_menu - display user prompt to choose
        get_user_selection - get user choice and act accordingly"""
        self.db_handler = DatabaseHandler()
        self.display_menu()
        self.get_user_selection()

    def display_menu(self):
        """Display user prompt to choose"""
        for key in PLAYER_REPORT_OPTIONS.keys():
            print(key, " : ", PLAYER_REPORT_OPTIONS[key])

    def get_user_selection(self):
        """Get user choice and show ordered players according to user choice"""
        choice = ""

        try:
            choice = int(input("Saisissez votre choix : "))
        except Exception:
            print(
                "Veuillez entrer un nombre entre 1 et 3" + " pour indiquer votre choix"
            )

        if choice == 1:
            """Sort all player in the database in alphabetical order"""
            print("Voici la liste des joueurs dans l'ordre alphabetique et leur id :")
            ordered_players = self.db_handler.order_player_alphabetically(
                self.db_handler.players
            )
            for player in ordered_players:
                print(f"{player} ({player.player_id})")
            """ Ask if quit or go back """
            final_choice = display_prompt_after_selection()
        elif choice == 2:
            """Sort all player in the database in their ranking's order"""
            print("Voici la liste des joueurs dans l'ordre de leur classement :")
            ordered_players_by_rank = self.db_handler.order_player_by_rank(
                self.db_handler.players
            )
            for player in ordered_players_by_rank:
                print(f"{player} ({player.player_id}) : {player.ranking}")
            """ Ask if quit or go back """
            final_choice = display_prompt_after_selection()
        elif choice == 3:
            """Show the main report generator menu"""
            ReportMenuView()
        else:
            """Show a message in the case of invalid entry"""
            print("!!!Choix invalide." + " Veuillez entrer un nombre entre 1 et 3 !!!")
            self.get_user_selection()

        if final_choice == 2:
            """Go back to report menu"""
            ReportMenuView()


class TournamentReportMenuView:
    """TournamentReportMenuView class"""

    def __init__(self):
        """Init attributes:
        tournament_id(int) - id of the tournament given by the user
        players(list) - list of players in the tournament
        db_handler - instance of DatabaseHandler

        Init method:
        display_tournament_selection_menu - display user prompt for tournament selection"""
        self.tournament_id = 0
        self.players = []
        self.db_handler = DatabaseHandler()

        self.display_tournament_main_menu()

    def display_tournament_main_menu(self):
        """Display menu to choose which report to be generated, all tournaments' or one specific"""
        option = ""

        for key in TOURNAMENT_REPORT_MAIN_OPTIONS.keys():
            print(key, " : ", TOURNAMENT_REPORT_MAIN_OPTIONS[key])

        try:
            option = int(input("Saisissez votre choix : "))
        except Exception:
            print("Veuillez entrer un nombre entre 1 et 3 pour indiquer votre choix")

        if option == 1:
            """Show the list of all the tournament"""
            self.display_all_tournaments()
            final_choice = display_prompt_after_selection()
        elif option == 2:
            """Display list of tournaments to choose one from it"""
            self.display_tournament_selection_menu()
        elif option == 3:
            """Go back to the previous menu"""
            ReportMenuView()
        else:
            """Show a message in the case of invalid entry"""
            print("!!!Choix invalide. Veuillez entrer un nombre entre 1 et 3 !!!")
            self.display_tournament_main_menu()

        if final_choice == 2:
            """Go back to the previous menu"""
            self.display_tournament_main_menu()

    def display_all_tournaments(self):
        """Display all tournaments in db"""
        print("-------Liste de tous les tournois---------")
        i = 1
        for tournament in self.db_handler.tournaments:
            print(
                f"{i}. Nom : {tournament.name}, Lieu : {tournament.location}, Date : {tournament.date}\n"
            )
            print("")
            print("Liste des joueurs :")
            for player in tournament.list_of_players:
                print(f"    {player}")
            print("")
            print("Nombre de tours : ", tournament.number_of_rounds)
            for round in self.db_handler.rounds:
                if round.tournament_id == tournament.id:
                    print("")
                    print(
                        f"{round.round_name}, Numéro du tour : {round.round_number},"
                        + f" Tour terminé : {round.is_round_finished}"
                    )
                    print("")
                    print("Matchs :")
                    for match in self.db_handler.matches:
                        if (
                            match.tournament_id == tournament.id
                            and match.round_number == round.round_number
                        ):
                            self.get_printable_match_with_winners(match)
            print("")
            print(
                f"Control du temps : {tournament.time_control}, Description : {tournament.description}\n"
                + f"Tournoi fini : {tournament.is_finished}"
            )
            if tournament.is_finished:
                print("")
                print(" Résultats du tournoi :")
                for player in tournament.final_result:
                    print(
                        f"   {player} ({player.player_id}), classement : {player.ranking},"
                        + f" Score : {player.total_score}"
                    )
            print("------")
            i += 1

    def display_tournament_selection_menu(self):
        """Display user prompt to choose tournament to generate report"""
        choice = ""

        try:
            print("Saisissez l'id d'un tournoi pour afficher son rapport")
            print("Voici la liste des tournois avec leur id dans la base de donnée")
            for tournament in self.db_handler.tournaments:
                print(f"({tournament.id}) {tournament}")

            choice = int(input("Saisissez l'id d'un tournoi : "))
            """ Ask if quit or continue """
        except Exception:
            print("Veuillez entrer un id valide !")
            self.display_tournament_selection_menu()

        """ Validate if tournament exists in db else request again """
        if self.validate_tournament_in_db(choice):
            self.tournament_id = choice
        else:
            print("Entrée invalide. Veuillez choisir un id depuis la liste donnée.")
            self.display_tournament_selection_menu()

        """ Display the menu to choose which report to be generated """
        self.display_menu()

    def validate_tournament_in_db(self, tournament_id: int):
        """Validate the selected tournament exists
        Arg:
        tournament_id(int) - id of the tournament to validate

        Returns:
        bool - tournament exist in the database"""
        tournament_ids = []
        for tournament in self.db_handler.tournaments:
            tournament_ids.append(tournament.id)

        if tournament_id in tournament_ids:
            return True
        else:
            return False

    def display_menu(self):
        """Display menu to choose which report to be generated"""
        option = ""

        for key in TOURNAMENT_REPORT_OPTIONS.keys():
            print(key, " : ", TOURNAMENT_REPORT_OPTIONS[key])

        try:
            option = int(input("Saisissez votre choix : "))
        except Exception:
            print("Veuillez entrer un nombre entre 1 et 4 pour indiquer votre choix")

        if option == 1:
            """Show players' menu to choose the order"""
            self.display_player_menu()
        elif option == 2:
            """Display rounds in the tournament"""
            self.display_rounds()
        elif option == 3:
            """Display matches in the tournament"""
            self.display_matches()
        elif option == 4:
            """Go back to the previous menu to choose tournament"""
            self.display_tournament_selection_menu()
        else:
            """Show a message in the case of invalid entry"""
            print("!!!Choix invalide." + " Veuillez entrer un nombre entre 1 et 4 !!!")
            self.display_menu()

    def display_player_menu(self):
        """Display menu to choose in which order players' to be listed"""
        for key in PLAYER_REPORT_OPTIONS.keys():
            print(key, " : ", PLAYER_REPORT_OPTIONS[key])

        for tournament in self.db_handler.tournaments:
            if tournament.id == self.tournament_id:
                self.players = tournament.list_of_players

        """ Get player sorting selection from user """
        self.get_player_order_selection()

    def get_player_order_selection(self):
        """Get user's choice on in which order players to be listed"""
        choice = ""

        try:
            choice = int(input("Saisissez votre choix : "))
        except Exception:
            print(
                "Veuillez entrer un nombre entre 1 et 3" + " pour indiquer votre choix"
            )

        if choice == 1:
            print("Voici la liste des joueurs dans l'ordre alphabetique et leur id :")
            ordered_players = self.db_handler.order_player_alphabetically(self.players)
            for player in ordered_players:
                print(f"{player} ({player.player_id})")
            """ Ask if quit or go back """
            final_choice = display_prompt_after_selection()
        elif choice == 2:
            print("Voici la liste des joueurs dans l'ordre de leur classement :")
            ordered_players_by_rank = self.db_handler.order_player_by_rank(self.players)
            for player in ordered_players_by_rank:
                print(f"{player} ({player.player_id}) : {player.ranking}")
            """ Ask if quit or go back """
            final_choice = display_prompt_after_selection()
        elif choice == 3:
            """Go back to the previous menu"""
            self.display_menu()
        else:
            """Show a message in the case of invalid entry"""
            print("!!!Choix invalide." + " Veuillez entrer un nombre entre 1 et 3 !!!")
            self.get_player_order_selection()

        if final_choice == 2:
            """Go back to the previous menu"""
            self.display_player_menu()

    def display_rounds(self):
        """Display rounds of the tournament"""
        print("\n Les tours du tournoi", self.tournament_id, "\n\n")
        for round in self.db_handler.rounds:
            if round.tournament_id == self.tournament_id:
                print("")
                print(f"{round.round_name}; Numéro de tour : {round.round_number} ;")
                print("")
                print("Matchs dans le tour : ")
                for match in self.db_handler.matches:
                    if (
                        match.tournament_id == round.tournament_id
                        and match.round_number == round.round_number
                    ):
                        self.get_printable_match_with_winners(match)
        print("\n\n")
        """ Ask if quit or go back """
        final_choice = display_prompt_after_selection()
        if final_choice == 2:
            """Go back to previous menu"""
            self.display_menu()

    def display_matches(self):
        """Display matches in the tournament"""
        print("\n Les matchs du tournoi", self.tournament_id, "\n\n")
        for match in self.db_handler.matches:
            if match.tournament_id == self.tournament_id:
                self.get_printable_match_with_winners(match)
        print("\n\n")
        """ Ask if quit or go back """
        final_choice = display_prompt_after_selection()
        if final_choice == 2:
            """Go back to previous menu"""
            self.display_menu()

    def get_winners_from_list(self, winners: list):
        """Get winners from the list of their ids
        Arg:
        winners(list) - list of winner ids

        Return:
        List of player objects"""
        winner_list = []
        for w in winners:
            winner = self.db_handler.get_player_object_from_id(w)
            winner_list.append(winner)
        return winner_list

    def get_printable_match_with_winners(self, match):
        """Get winners of a match and print one by one."""
        print("")
        winner = self.get_winners_from_list(match.winner)
        print(f"{match} ; gagnant/s :")
        for i in range(0, len(winner)):
            print(" ", winner[i])
