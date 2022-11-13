""" Define the tournament views """
from views.helper import (
    validate_date,
    validate_time_control,
    validate_date_in_future,
    prompt_quit_or_continue,
)
from controllers.database_handler import DatabaseHandler


class CreateTournamentView:
    """CreateTournamentView class"""

    def __init__(self):
        """Init the following attributes:
        tournament_name - name of the tournament
        tournament_location - location of the tournament
        tournament_date - date of the tournament
        number_of_rounds - nubmer of rounds in the tournament
        time_control - time_control of the tournament
                    (bullet, blitz or coup rapide)
        description - description of the tournament
        number_of_players - number of players in the tournament
        players - list of player's ids
        db_handler - instance of DatabaseHandler

        Init methods:
        displaye_tournament_menu - prompt of tournament infos
        add_player - prompt for adding player's (by id) in the tournament"""
        self.tournament_name = ""
        self.tournament_location = ""
        self.tournament_date = ""
        self.number_of_rounds = ""
        self.time_control = ""
        self.description = ""
        self.number_of_players = ""
        self.players = []
        self.db_handler = DatabaseHandler()

        self.display_tournament_menu()
        self.add_player()
        prompt_quit_or_continue()

    def display_tournament_menu(self):
        """User prompt to enter tournaments' info"""

        print(
            "Veuillez entrer les informations suivantes "
            + "pour créer un nouveau tournoi :"
        )

        while self.tournament_name.strip() == "":
            self.tournament_name = input("Nom du tournoi : ")

        while self.tournament_location == "":
            self.tournament_location = input("Lieu : ")

        while self.tournament_date.strip() == "":
            self.tournament_date = input("Date (jj/mm/aaaa) : ")
            if not validate_date(self.tournament_date):
                self.tournament_date = ""
            elif not validate_date_in_future(self.tournament_date):
                self.tournament_date = ""
            else:
                pass

        while not self.number_of_rounds.isnumeric():
            self.number_of_rounds = input("Nombre de tours : ")
            if self.number_of_rounds.strip() == "":
                self.number_of_rounds = 4
                print("Le nombre de tours par défaut est 4.")
                break

        while not validate_time_control(self.time_control):
            self.time_control = input(
                "Contrôle du temps " + "(Bullet/Blitz/Coup rapide): "
            )

        while self.description == "":
            self.description = input("Description : ")

        """ Make sure that number of players is greater than double the number of rounds,
        to avoid a bug in swiss tournament algorithm. """
        minimum_nb_of_players = 2 * int(self.number_of_rounds)
        while (
            not self.number_of_players.isnumeric()
            or int(self.number_of_players) < minimum_nb_of_players
        ):
            print("Le nombre de joueurs minimum est", minimum_nb_of_players)
            self.number_of_players = input("Nombre de joueurs : ")

    def add_player(self):
        """Propmt to enter players' ids."""

        print("Entrez l'id d'un joueur à ajouter :")
        print("Voici la liste des joueurs avec leur id -")
        for player in self.db_handler.players:
            print(f"{player.first_name} {player.last_name} ({player.player_id})")
        print("----------Fin de la liste--------")

        number_of_players = int(self.number_of_players)

        while len(self.players) < number_of_players:
            new_player = input(
                f"Joueur {str(len(self.players) + 1)}/{number_of_players} : "
            )
            if self.db_handler.validate_player_id_exists(int(new_player)) and not (
                new_player in self.players
            ):

                self.players.append(new_player)
            elif new_player in self.players:
                print(
                    "Joueur déjà entré dans la liste. "
                    + "Veuillez sélectionner un autre joueur."
                )
            else:
                print(
                    "Le joueur n'est pas enregistré dans la base de données."
                    + "Veuillez ajouter le joueur en accédant à l'option « Ajuter des joueurs »"
                    + " dans le menu principal."
                )


class OngoingTournamentView:
    """OngoingTournamentView class"""

    def __init__(self):
        """Init attributes:
        db_handler - DatabaseHandler instance
        tournament_id - tournament's id input from user
        ongoing_tournaments - unfinished tournaments in the database
        tournament - Tournament corresponding to the unique id given by the user

        Init method:
        display_user_prompt - display user prompt"""
        self.db_handler = DatabaseHandler()
        self.tournament_id = ""
        self.ongoing_tournaments = []
        self.tournament = self.display_user_prompt()

    def display_user_prompt(self):
        """User prompt to enter unique id of the tournament to load.
        Return:
        tournament(Tournament) - tournament object corresponding to user entry"""

        print("Liste de nom/s et id/s de tournoi en cours : ")
        for tournament in self.db_handler.tournaments:
            if tournament.is_finished is False:
                print(f"{tournament.name} : {tournament.id}")
                self.ongoing_tournaments.append(tournament)
        while not self.tournament_id.isnumeric():
            self.tournament_id = input("L'id de tournoi a charger : ")

            if self.tournament_id.strip() == "" or not self.tournament_id.isnumeric():
                self.tournament_id = ""
                print("Entrée invalide.")
            elif not self.validate_tournament_in_list(int(self.tournament_id)):
                self.tournament_id = ""
                print("Entrée invalide. Veuillez choisir un id depuis le list dessus.")
            prompt_quit_or_continue()

        print("Vous avez choisi", self.tournament_id, "voici les infos lieés :")
        for tournament in self.db_handler.tournaments:
            if int(self.tournament_id) == tournament.id:
                print(
                    f"Nom du tournoi : {tournament.name} \nLieu : {tournament.location} \n"
                    + "Date : {tournament.date} \nNombre de tours : {tournament.number_of_rounds} \nListe de tours :"
                )
                for round in tournament.list_of_rounds:
                    print(" ", round)
                print(
                    f"Nombre de joueurs : {len(tournament.list_of_players)} \nListe de Joueurs :"
                )
                for player in tournament.list_of_players:
                    print(" ", player)
                print(
                    f"Control du temps : {tournament.time_control} \nDescription : {tournament.description}"
                )
                return tournament
                prompt_quit_or_continue()

    def validate_tournament_in_list(self, tournament_id: int):
        """Validate the tournament selected by the user is an unfinished one.
        Arg:
        tournament_id - unique id of the tournament

        Return:
        bool - tournament is in the ongoing_tournaments list"""
        tournament_ids = []
        for tournament in self.ongoing_tournaments:
            tournament_ids.append(tournament.id)
        if tournament_id in tournament_ids:
            return True
        else:
            return False
