""" Define the player view """
from views.helper import validate_date, validate_date_in_past
from controllers.database_handler import DatabaseHandler


class PlayerView:
    """PlayerView class"""

    def __init__(self):
        """Init attributes:
        last_name - last name of the player capitalized
        first_name - first name of the player (in upper case)
        date_of_birth - date of birth of the player
        sex - sex of the player
        ranking - ranking of the player (positive integer)
        player_id_to_update - id of the player to update ranking
        new_ranking - ranking of the player after update
        db_handler - instance of DatabaseHandler"""
        self.last_name = ""
        self.first_name = ""
        self.date_of_birth = ""
        self.sex = ""
        self.ranking = ""

        self.player_id_to_update = ""
        self.new_ranking = ""

        self.db_handler = DatabaseHandler()

    def display_add_player_menu(self):
        """Display add player to database view"""
        print(
            "Veuillez entrer les informations suivantes "
            + "pour ajouter un nouveau joueur :"
        )

        while self.last_name.strip() == "":
            self.last_name = input("Nom de famille : ").upper()

        while self.first_name == "":
            self.first_name = input("Prénom : ").capitalize()

        while self.date_of_birth.strip() == "":
            self.date_of_birth = input("Date de naissence (dd/mm/aaaa) : ")
            if not validate_date(self.date_of_birth):
                self.date_of_birth = ""
            elif not validate_date_in_past(self.date_of_birth):
                self.date_of_birth = ""
            else:
                pass

        while self.sex == "":
            self.sex = input("Sexe : ")

        while not self.ranking.isnumeric():
            self.ranking = input("Classement : ")
            if (
                self.ranking.isnumeric()
                and int(self.ranking) < 0
                or not self.ranking.isnumeric()
            ):
                self.ranking = ""
                print("Entrée invalide. Veuillez saissir un chiffre positif.")
            else:
                pass

    def display_player_updater_menu(self):
        """Display update player's ranking view"""
        while not self.player_id_to_update.isnumeric():
            print("Liste de joueur enregistrées et leur id")
            print("****************************************")
            for player in self.db_handler.players:
                print(f"{player} : {player.player_id}")

            self.player_id_to_update = input("Id du joueur à modifier :")
            if not self.db_handler.validate_player_id_exists(
                int(self.player_id_to_update)
            ):
                self.player_id_to_update = ""
                print("Entrée invalide.")
            else:
                print("Player info :")
                for player in self.db_handler.players:
                    if player.player_id == int(self.player_id_to_update):
                        print(f"{player}; classement : {player.ranking}")

        while not self.new_ranking.isnumeric():
            self.new_ranking = input("Nouvelle valeur de classement : ")
            if (
                self.new_ranking.isnumeric()
                and int(self.new_ranking) < 0
                or not self.new_ranking.isnumeric()
            ):
                self.new_ranking = ""
                print("Entrée invalide.Veuillez saissir un chiffre positif.")
            else:
                pass
