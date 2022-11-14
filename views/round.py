""" Define the round view """
from datetime import datetime

from models.round import Round
from views.helper import (
    validate_winner_entry,
    validate_date_time,
    validate_round_end_date,
)
from controllers.database_handler import DatabaseHandler


class RoundView:
    """Round view during a tournament"""

    def __init__(self, round: Round, number_of_matches: int, match_number_to_load=1):
        """Init the following attributes:
        db_handler - instance of DatabaseHandler
        round - Current round object
        number_of_matches - number of matches in the round
        match_number_to_load - number of the match to load in the round
        round_end_date_time - End date time of the round
        winners_list - Winners ids as string in a list, string to handle when there is a draw
        matches - list of Match objects

        Init methods:
        display_round_prompt - Prompt for the user
        save_round_to_db_with_matches - Save round with the current matches to the db"""
        self.db_handler = DatabaseHandler()
        self.round = round
        self.number_of_matches = number_of_matches
        self.match_number_to_load = match_number_to_load
        self.round_end_date_time = ""
        self.winners_list = []
        self.matches = []

        self.display_round_prompt()
        self.round_end_date_time = datetime.now()
        self.save_round_to_db_with_matches()

    def display_round_prompt(self):
        """Diplay generated matches and prompt for winners and end date time."""
        print(f"--------MATCHS POUR TOUR {self.round.round_number}--------")
        for match in self.round.matches:
            match_number = self.round.matches.index(match) + 1
            print("****Match " + str(match_number) + "****")
            for player in match.pair_of_players:
                print(player, " (", player.player_id, ")")
        print("------FIN DU MATCH-----")

        iterations = self.number_of_matches - self.match_number_to_load
        while iterations > 0:
            match_number = int(self.number_of_matches - iterations + 1)
            winner = ""
            while winner.strip() == "":
                match_number_str = str(match_number)
                winner = input(
                    "Veuillez entrer l'id du gagnant du match "
                    + match_number_str
                    + "\n(en cas de match nul, entrez l'ids"
                    + " des deux joueurs séparés d'un éspace) : "
                )
                while not validate_winner_entry(
                    self.round.matches[match_number - 1], winner
                ):
                    print("Éntrée invalide. Veuillez réessayer")
                    winner = input(
                        "Veuillez entrer l'id du gagnant du match "
                        + match_number_str
                        + " : "
                    )
                winner_to_list = winner.split(" ")
                self.round.matches[match_number - 1].winner = []
                for w in winner_to_list:
                    if w.isnumeric():
                        self.round.matches[match_number - 1].winner.append(int(w))
                        self.round.matches[
                            match_number - 1
                        ].round_number = self.round.round_number
                        """ Save match to db """
                        serialized_match = self.db_handler.save_match_to_db(
                            self.round.matches[match_number - 1]
                        )
                        match = self.db_handler.get_deserialized_match(serialized_match)
                        self.matches.append(match)
            self.winners_list.append(winner_to_list)
            iterations -= 1


    def save_round_to_db_with_matches(self):
        """Save round to database with the generated matches."""
        self.round.matches = self.matches
        serialized_round = self.db_handler.save_round_to_db(self.round)
        self.round = self.db_handler.get_deserialized_round(serialized_round)
