""" Define the round generator controller """
from operator import attrgetter

from models.player import Player
from models.round import Round
from models.match import Match

from views.round import RoundView

from controllers.database_handler import DatabaseHandler


class RoundGenerator:
    """Round generator controller"""

    def __init__(
        self,
        tournament_id: int,
        list_of_players: [],
        number_of_rounds: int,
        load_from_first_match: bool,
        starting_round_number=1,
        starting_match_number=0,
    ):
        """Init the following attributes:
        db_handler - instance of DatabaseHandler
        tournament_id - unique id of the tournament
        list_of_players - list of player objects
        number_of_rounds - number of rounds in the tournament
        load_from_first_match (bool) - load from match number 1
        starting_round_number - round number to load
        starting_match_number - match number to load
        round_view - RoundView object
        rounds - list of Round objects in the tournament
        number_of_matches_in_round - number of matches in a round
        final_result - sorted list of players according to their scores in the tournament

        Init the methods:
        handle_odd_number_of_players - add a nobody player
        if the number of players in the tournament is odd
        create_first_round_and_save - generate first round and save to db
        create_next_round_and_save - generate next round and save to db
        delete_no_player - delete the nobody if added in case of odd number of players"""

        self.db_handler = DatabaseHandler()
        self.tournament_id = tournament_id
        self.list_of_players = list_of_players
        self.number_of_rounds = number_of_rounds
        self.load_from_first_match = load_from_first_match
        self.starting_round_number = starting_round_number
        self.starting_match_number = starting_match_number

        self.handle_odd_number_of_players(self.list_of_players)
        self.number_of_matches_in_round = len(self.list_of_players) / 2

        self.round_view = None
        self.rounds = []
        self.final_result = []

        if self.load_from_first_match:
            """Load from first round and first match"""
            self.starting_round_number = 2
            self.starting_match_number = 0
            self.create_first_round_and_save(starting_match=0)
            self.create_next_rounds_and_save(
                starting_round_number=self.starting_round_number,
                starting_match=self.starting_match_number,
            )
        elif self.starting_round_number == 1:
            """Load from first round but not from first match"""
            self.create_first_round_and_save(self.starting_match_number)
            self.create_next_rounds_and_save(starting_round_number=2, starting_match=0)
        else:
            """Load from rounds greater than 1"""
            for round in self.db_handler.rounds:
                if int(round.tournament_id) == self.tournament_id:
                    self.rounds.append(round)
            self.create_next_rounds_and_save(
                starting_round_number=self.starting_round_number,
                starting_match=self.starting_match_number,
            )

        self.final_result = self.sort_player_by_score(self.list_of_players)
        self.delete_no_player()

    def sort_player_by_ranking(self, players_list: list):
        """Sort players by their ranking
        Args:
        players_list - list of player objects

        Returns:
        list - sorted list of players"""
        sorted_list = sorted(players_list, key=attrgetter("ranking"), reverse=False)
        return sorted_list

    def sort_player_by_score(self, players_list: list):
        """Sort players by their ranking and then sort the list by score
        Args:
        players_list - list of player objects

        Returns:
        list - sorted list of players"""
        sorted_players_by_rank = self.sort_player_by_ranking(players_list)
        sorted_list = sorted(
            sorted_players_by_rank, key=lambda player: player.total_score, reverse=True
        )
        return sorted_list

    def handle_odd_number_of_players(self, players: list):
        """Add a player object named nobody incase of odd number of players
        in the tournament

        Args:
        players (list) - List of player objects"""
        no_player = Player(
            player_id=0,
            last_name="nobody",
            first_name="nobody",
            date_of_birth="",
            sex="",
            total_score=0,
            ranking=1000000,
            opponents_list=[],
        )
        if len(players) % 2 == 0:
            pass
        else:
            players.append(no_player)
            self.list_of_players.append(no_player)

    def delete_no_player(self):
        """Delete no player from players"""
        if len(self.list_of_players) % 2 != 0:
            del self.list_of_players[-1]

    def generate_first_round(self):
        """Generate first round according to swiss system

        Returns:
        list - list of matches in the first round"""
        players = self.sort_player_by_ranking(self.list_of_players)
        first_matches = []

        half_the_total_players = int(len(self.list_of_players) / 2)
        for i in range(0, half_the_total_players):
            player_01 = players[i]
            player_02 = players[i + half_the_total_players]
            player_01.opponents_list.append(player_02.player_id)
            player_02.opponents_list.append(player_01.player_id)
            """ Create match object """
            match_name = Match(
                tournament_id=self.tournament_id,
                round_number=1,
                pair_of_players=(player_01, player_02),
            )
            first_matches.append(match_name)
        return first_matches

    def get_player_object_from_id(self, player_id: int):
        """Get player object from player_id

        Arg:
        player_id - unique id of the player

        Return:
        player object"""
        for player in self.list_of_players:
            if player.player_id == player_id:
                return player

    def add_score(self, winners_id_list):
        """Add score according to the match results
         - winner gain 1 point
         - if match is a draw winners gain 0.5 points

        Args:
        winners_id_list - list of winners id strings from RoundView"""

        for winner in winners_id_list:
            if len(winner) > 1:
                for w in winner:
                    if w.isnumeric():
                        player = self.get_player_object_from_id(int(w))
                        player.total_score = player.total_score + 0.5
            else:
                player = self.get_player_object_from_id(int(winner[0]))
                player.total_score = player.total_score + 1.0

        for tournament in self.db_handler.tournaments:
            if tournament.id == self.tournament_id:
                self.update_players_score_in_tournament(tournament)

    def generate_next_round(self):
        """Generate next round according to swiss system

        Returns:
        list - list of matches in the next round"""

        players = self.sort_player_by_score(self.list_of_players)
        has_a_match = {}
        for player in players:
            has_a_match[player] = False

        matches = []

        """Special case to match the last player with the closest possible one.
        This makes sure that in case of odd number of players,
        a player cannot be left apart more than once. """
        if len(self.list_of_players) % 2 != 0:
            last_player = players[-1]
            has_a_match[last_player] = True
            reversed_players = players
            reversed_players.reverse()
            for opponent in reversed_players:
                if (
                    has_a_match[opponent] is False
                    and opponent.player_id not in last_player.opponents_list
                ):
                    player_02 = opponent
                    has_a_match[player_02] = True
                    last_player.opponents_list.append(player_02.player_id)
                    player_02.opponents_list.append(last_player.player_id)
                    match_name = Match(
                        tournament_id=self.tournament_id,
                        round_number=-1,
                        pair_of_players=(last_player, player_02),
                        winner=[],
                    )
                    matches.append(match_name)
                    break

        for i in range(0, int(len(players))):
            player_01 = players[i]
            if has_a_match[player_01] is False:
                has_a_match[player_01] = True
                for opponent in players:
                    if (
                        has_a_match[opponent] is False
                        and opponent.player_id not in player_01.opponents_list
                    ):
                        player_02 = opponent
                        has_a_match[player_02] = True
                        player_01.opponents_list.append(player_02.player_id)
                        player_02.opponents_list.append(player_01.player_id)
                        match_name = Match(
                            tournament_id=self.tournament_id,
                            round_number=-1,
                            pair_of_players=(player_01, player_02),
                            winner=[],
                        )
                        matches.append(match_name)
                        break

        return matches

    def create_first_round_and_save(self, starting_match: int):
        """Generate first round and save it to db

        Arg:
        starting_match - match number to start (starting from 0)"""
        """ Create first round object """
        first_matches = self.generate_first_round()
        round_01 = Round(
            round_number=1,
            round_name="Round1",
            tournament_id=self.tournament_id,
            matches=first_matches,
        )

        """ Create RoundView object for the first round and
        mark the first round as finished. """
        self.round_view = RoundView(
            round_01, self.number_of_matches_in_round, starting_match
        )
        round_01 = self.round_view.round
        round_01.is_round_finished = True
        """ Add score for winners """
        self.add_score(self.round_view.winners_list)
        """ Save the end date time """
        round_01.end_date_time = str(self.round_view.round_end_date_time)
        first_matches = self.round_view.matches
        saved_first_matches = []
        """ Reload matches to round """
        for match in self.db_handler.matches:
            if match.tournament_id == self.tournament_id and match.round_number == 1:
                saved_first_matches.append(match)
        """ Update matches with round's id """
        for match in saved_first_matches:
            match.round_id = round_01.id
            self.db_handler.matches_table.update(
                {"round_id": round_01.id}, doc_ids=[match.match_id]
            )
        """ Update round in db """
        self.db_handler.rounds_table.update(
            {"is_round_finished": True}, doc_ids=[round_01.id]
        )
        self.db_handler.rounds_table.update(
            {"end_date_time": round_01.end_date_time}, doc_ids=[round_01.id]
        )
        self.rounds.append(round_01)
        """ Load the saved rounds again in db_handler's list """
        self.db_handler.load_deserialized_rounds()

    def create_next_rounds_and_save(
        self, starting_round_number: int, starting_match: int
    ):
        """Create RoundView object for all the rounds except the first

        Args:
        starting_round_number - round number to be generated
        starting_match - match number to be generated"""

        for r in range(starting_round_number, int(self.number_of_rounds) + 1):
            round_name = "round" + str(r)
            """ Create round object """
            current_matches = self.generate_next_round()
            current_round = Round(
                round_number=r,
                round_name=round_name,
                tournament_id=self.tournament_id,
                matches=current_matches,
            )
            print("debug", starting_match)
            """ Create RoundView object for the round """
            self.round_view = RoundView(
                current_round, self.number_of_matches_in_round, starting_match
            )
            current_round = self.round_view.round
            """ Add score for winners """
            self.add_score(self.round_view.winners_list)
            """ Mark the round as finished and update end date time """
            current_round.end_date_time = str(self.round_view.round_end_date_time)
            current_round.is_round_finished = True
            current_matches = self.round_view.matches
            current_saved_matches = []
            """ Reload matches to round """
            for match in self.db_handler.matches:
                if (
                    match.tournament_id == self.tournament_id
                    and match.round_number == r
                ):
                    current_saved_matches.append(match)
            """ Update matches with round's id """
            for match in current_saved_matches:
                match.round_id = current_round.id
                self.db_handler.matches_table.update({"round_id": current_round.id})
            self.rounds.append(current_round)
            """ Update round in db """
            self.db_handler.rounds_table.update(
                {"is_round_finished": True}, doc_ids=[current_round.id]
            )
            self.db_handler.rounds_table.update(
                {"end_date_time": current_round.end_date_time},
                doc_ids=[current_round.id],
            )
            self.rounds.append(current_round)
            """ Load rounds again to the db_handler list"""
            self.db_handler.load_deserialized_rounds()

    def update_players_score_in_tournament(self, tournament):
        """Update players list in the tournament with their score"""
        tournament.list_of_players = self.list_of_players
        players_serialized = []
        for player in self.list_of_players:
            serialized_player = player.get_serialized_player()
            players_serialized.append(serialized_player)
        self.db_handler.tournaments_table.update(
            {"list_of_players": players_serialized}, doc_ids=[tournament.id]
        )
