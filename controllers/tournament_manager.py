""" Define the tournament manager controllers """

from math import ceil

from models.tournament import Tournament

from controllers.round_generator import RoundGenerator
from controllers.database_handler import DatabaseHandler

from views.tournament import CreateTournamentView, OngoingTournamentView


class TournamentManager:
    """TournamentManager controller class."""

    def __init__(self):
        """Init the following attributes:
        db_handler - instance of DatabaseHandler
        create_tournament_view - instance of CreateTournamentView
        players - list of players in the tournament
        tournament - deserialized tournament object from database
        round_generator - instance of RoundGenerator

        Init method:
        display_final_winners_list - show the ordered list of players according to their score
        update_tournament_in_db - update the tournament in db with the new data"""

        self.db_handler = DatabaseHandler()

        self.create_tournament_view = CreateTournamentView()

        """ Get player objects from their ids given by user """
        self.players = []
        for id in self.create_tournament_view.players:
            player = self.get_player_object_from_id_str(id)
            self.players.append(player)

        self.tournament = self.get_tournament(self.create_tournament_view)
        self.round_generator = RoundGenerator(
            self.tournament.id,
            self.tournament.list_of_players,
            self.tournament.number_of_rounds,
            load_from_first_match=True,
        )

        self.display_final_winners_list()
        self.update_tournament_in_db(self.tournament)

    def get_player_object_from_id_str(self, id: str):
        """Convert player ids to objects
        Args:
        id (str) - id of the player

        Returns:
        Player object"""

        for player in self.db_handler.players:
            if player.player_id == int(id):
                return player

    def get_tournament(self, create_tournament_view: CreateTournamentView):
        """Create tournament from user inputs, save it to db
        Args:
        create_tournament_view(CreateTournamentView) - instance of CreateTournamentView

        Returns:
        Deserialized tournament from db
        """

        tournament_object = self.db_handler.create_tournament(
            create_tournament_view.tournament_name,
            create_tournament_view.tournament_location,
            create_tournament_view.tournament_date,
            create_tournament_view.number_of_rounds,
            create_tournament_view.time_control,
            create_tournament_view.description,
            create_tournament_view.number_of_players,
            self.players,
        )

        """ Save tournament to db """
        serialized_tournament = self.db_handler.save_tournament_to_db(tournament_object)

        tournament = self.db_handler.get_deserialized_tournament(serialized_tournament)
        return tournament

    def display_final_winners_list(self):
        """Display final list of players with their scores"""
        print("*******************")
        print("VVoici les résultats du tournoi : ")
        for player in self.round_generator.ordered_players_in_tournament:
            print(
                f"{player} ({player.player_id}), classement : {player.ranking},"
                + " Score dans ce tournoi : {player.total_score}"
            )

    def update_tournament_in_db(self, tournament: Tournament):
        """Update tournament data in db for is_finished and list_of_rounds

        Args:
        tournament(Tournament) - instance of tournament
        """
        tournament.is_finished = True
        self.db_handler.tournaments_table.update(
            {"is_finished": True}, doc_ids=[tournament.id]
        )
        rounds_in_tournament = self.db_handler.rounds_table.search(
            self.db_handler.QueryItem.tournament_id == tournament.id
        )
        self.db_handler.tournaments_table.update(
            {"list_of_rounds": rounds_in_tournament}, doc_ids=[tournament.id]
        )
        print("***********Fin du tournoi*************")


class OngoingTournamentManager:
    """OngoingTournamentManager controller class"""

    def __init__(self):
        """Init the following attributes:
        db_handler - instance of DatabaseHandler
        ongoing_tournament_view - instance of OngoingTournamentView
        tournament - tournament to load
        generated_rounds - already generated rounds in the tournament
        generated_matches - already generated matches in the tournament
        starting_round_number - starting round number while loading the tournament
        starting_match_nubmer - starting match number while loading the tournament
        round_generator - instance of RoundGenerator

        Init methods:
        get_generated_rounds - populate the list of generated rounds in the tournament
        get_generated_matches - populate the list of generated matches in the tournament
        display_final_winners_list - show the ordered list of players according to their score
        update_tournament_ - update the tournament in db with the new data
        """
        self.db_handler = DatabaseHandler()
        self.ongoing_tournament_view = OngoingTournamentView()
        self.tournament = self.ongoing_tournament_view.tournament

        self.generated_rounds = []
        self.get_generated_rounds()

        self.generated_matches = []
        self.get_generated_matches()

        self.starting_round_number = self.get_starting_round()

        self.starting_match_number = self.get_starting_mach_number()

        self.round_generator = self.load_and_genrate_rounds()

        """ Update tournament data if all rounds are finished and number of rounds
        in the tournament is same as the last round's number """
        if (self.round_generator.rounds[-1].is_round_finished is True) and (
            int(self.round_generator.rounds[-1].round_number)
            == int(self.tournament.number_of_rounds)
        ):
            self.display_final_winners_list()
            self.update_tournament()
            print("***********Fin du tournoi*************")
        else:
            pass

    def get_generated_rounds(self):
        """Get generated rounds in the tournament from database and populate the generated_rounds list."""
        for round in self.db_handler.rounds:
            if int(round.tournament_id) == int(self.tournament.id):
                self.generated_rounds.append(round)

    def get_generated_matches(self):
        """Get generated matches in the tournament from database and populate the generated_matches list."""
        for match in self.db_handler.matches:
            if match.tournament_id == self.tournament.id:
                self.generated_matches.append(match)

    def get_starting_round(self):
        """Get the starting round number of the tournament to load

        Return:
        starting_round_number - starting round number while loading the tournament"""
        if len(self.generated_rounds) > 0:
            """Increment the last generated round's number by 1."""
            starting_round_number = int(self.generated_rounds[-1].round_number) + 1
            return starting_round_number

    def get_starting_mach_number(self):
        """Get the starting match number of the tournament to load

        Return:
        starting_match_number - starting matchund number while loading the tournament"""

        """ Number of matches in a round calculated from the tournament's list of players.
        Use ceil to include the odd number of players condition. """
        number_of_matches_in_round = ceil(len(self.tournament.list_of_players) / 2)
        number_of_generated_matches = len(self.generated_matches)
        number_of_generated_rounds = len(self.generated_rounds)
        """ Number of generated matches if one more round which is not yet saved has played.
        To ask for the end datetime if the user interepts before. """
        number_to_compare = (
            number_of_generated_rounds + 1
        ) * number_of_matches_in_round
        if len(self.generated_rounds) > 0 and (
            number_of_generated_matches != number_to_compare
        ):
            starting_match_number = int(
                number_of_generated_matches % number_of_matches_in_round
            )
            return starting_match_number
        elif number_of_generated_matches == number_to_compare:
            starting_match_number = number_of_matches_in_round
            return starting_match_number

    def load_and_genrate_rounds(self):
        """Create instance of RoundGenerator with apporpriate values"""
        if len(self.generated_rounds) == 0 and len(self.generated_matches) == 0:
            print("*****Reprise du 1er tour et 1er match*****")
            self.round_generator = RoundGenerator(
                self.tournament.id,
                self.tournament.list_of_players,
                self.tournament.number_of_rounds,
                load_from_first_match=True,
            )
        elif len(self.generated_rounds) == 0 and len(self.generated_matches) > 0:
            print("*****Reprise du 1er tour*****", len(self.generated_matches))
            self.round_generator = RoundGenerator(
                self.tournament.id,
                self.tournament.list_of_players,
                self.tournament.number_of_rounds,
                load_from_first_match=False,
                starting_round_number=1,
                starting_match_number=len(self.generated_matches),
            )
        else:
            print(f"*****Reprise du {self.starting_round_number}em tour*****")
            self.round_generator = RoundGenerator(
                self.tournament.id,
                self.tournament.list_of_players,
                self.tournament.number_of_rounds,
                load_from_first_match=False,
                starting_round_number=self.starting_round_number,
                starting_match_number=self.starting_match_number,
            )
        return self.round_generator

    def display_final_winners_list(self):
        """Display final list of players with their scores"""
        print("*******************")
        print("Voici les résultats du tournoi : ")
        for player in self.round_generator.ordered_players_in_tournament:
            print(
                f"{player} ({player.player_id}), classement : {player.ranking},"
                + " Score dans ce tournoi : {player.total_score}"
            )

    def update_tournament(self):
        """Update tournament data for is_finished and list_of_rounds"""
        self.tournament.is_finished = True
        self.db_handler.tournaments_table.update(
            {"is_finished": True}, doc_ids=[self.tournament.id]
        )
        rounds_in_tournament = self.db_handler.rounds_table.search(
            self.db_handler.QueryItem.tournament_id == self.tournament.id
        )
        self.db_handler.tournaments_table.update(
            {"list_of_rounds": rounds_in_tournament}, doc_ids=[self.tournament.id]
        )
