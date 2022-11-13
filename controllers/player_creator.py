""" Define the player creator controller """
from views.player import PlayerView
from controllers.database_handler import DatabaseHandler


class PlayerCreator:
    """PlayerCreator class"""

    def __init__(self):
        """Init attribute:
        db_handler - instance of DatabaseHandler

        Init method:
        display_player_view - display view for adding a player to the database"""
        self.db_handler = DatabaseHandler()
        self.display_player_view()

    def display_player_view(self):
        """Display user prompt for adding a player to the database"""
        user_answer = "y"
        while not user_answer.lower() == "n":
            """Instanciate PlayerView and display add player view"""
            player = PlayerView()
            player.display_add_player_menu()
            """ Create Player from user infos and save it to db. """
            player_object = self.db_handler.create_player(
                player.last_name,
                player.first_name,
                player.date_of_birth,
                player.sex,
                int(player.ranking),
            )
            self.db_handler.save_player_to_db(player_object)
            user_answer = input("Voulez-vous ajouter un autre joueur (o/n) : ")
