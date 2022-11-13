""" Define the player updater controller """
from views.player import PlayerView
from controllers.database_handler import DatabaseHandler


class PlayerUpdater:
    """PlayerUpdater class"""

    def __init__(self):
        """Init attribute:
        db_handler - instance of DatabaseHandler

        Init method:
        display_player_updater_view - display view for updating player's ranking"""
        self.db_handler = DatabaseHandler()
        self.display_player_updater_view()

    def display_player_updater_view(self):
        """Display user prompt for updating player's ranking"""
        user_answer = "y"
        while not user_answer.lower() == "n":
            """Instanciate PlayerView and display rank updater view"""
            player = PlayerView()
            player.display_player_updater_menu()
            """ Update ranking of the player in database """
            updated_ids = self.db_handler.players_table.update(
                {"ranking": int(player.new_ranking)},
                doc_ids=[int(player.player_id_to_update)],
            )
            serialized_player_updated = self.db_handler.players_table.get(
                doc_id=updated_ids[0]
            )
            updated_player = self.db_handler.get_deserialized_player(
                serialized_player_updated
            )
            print("Le classement a été mise à jour.")
            print(
                f"Le classement de {updated_player} maitenant est {updated_player.ranking}"
            )
            user_answer = input(
                "Voulez-vous modifier classement d'un autre joueur (o/n) : "
            )
