""" Define the database handler controller """
from operator import attrgetter
from tinydb import Query

from models.database import Database
from models.player import Player
from models.tournament import Tournament
from models.round import Round
from models.match import Match


class DatabaseHandler:
    """DatabaseHandler class"""

    def __init__(self):
        """Init attributes:
        database - instance of Database
        players_table - tinydb table for Player
        tournaments_table - tinydb table for Tournament
        rounds_table - tinydb table for Round
        matches_table - tinydb table for Match
        players - deserialized list of Players
        tournaments - deserialized list of Tournaments
        rounds - deserialized list of Rounds
        matches - deserialized list of matches
        QueryItem - tinydb query item

        init methods:
        create_tables - create tinydb tables
        load_deserialized_players - populate players list with deserialized Players from db
        load_deserialized_tournaments - populate tournaments list with deserialized Tournaments from db
        load_deserialized_rounds - populate rounds list with deserialized Rounds from db
        load_deserialized_matches - populate matches list with deserialized Matches from db"""

        self.database = Database()

        self.players_table = None
        self.tournaments_table = None
        self.rounds_table = None
        self.matches_table = None

        self.create_tables()

        self.players = []
        self.load_deserialized_players()

        self.tournaments = []
        self.load_deserialized_tournaments()

        self.rounds = []
        self.load_deserialized_rounds()

        self.matches = []
        self.load_deserialized_matches()

        self.QueryItem = Query()

    def create_tables(self):
        """Create tinydb tables"""
        self.players_table = self.database.db.table("players")
        self.tournaments_table = self.database.db.table("tournaments")
        self.rounds_table = self.database.db.table("rounds")
        self.matches_table = self.database.db.table("matches")

    def create_player(
        self,
        last_name: str,
        first_name: str,
        date_of_birth: str,
        sex: str,
        ranking: int,
    ):
        """Create player object.
        Args:
        last_name - players' last name
        first_name - players' first name
        date_of_birth - player's dob
        sex - player's sex
        ranking - player's ranking

        Return:
        player(Player) - player"""
        player = Player(
            last_name=last_name,
            first_name=first_name,
            date_of_birth=date_of_birth,
            sex=sex,
            total_score=0,
            ranking=ranking,
            opponents_list=[],
        )
        return player

    def save_player_to_db(self, player: Player):
        """Save player to database.
        Args:
        player(Player) - player object

        Return:
        serialized_player_updated - player dict from db, updated with the corresponding unique id"""
        serialized_player = player.get_serialized_player()

        """ Store doc_id of the saved player and update player_id with the same. """
        player_id = self.save_to_db(self.players_table, serialized_player)
        updated_ids = self.players_table.update(
            {"player_id": player_id}, doc_ids=[player_id]
        )
        serialized_player_updated = self.players_table.get(doc_id=updated_ids[0])
        return serialized_player_updated

    def save_to_db(self, table, serialized_data):
        """Insert serialized data to the corresponding table
        Args:
        table - tinydb table
        serialized_data - serialized data to save to db

        Return:
        id(int) - doc_id of the inserted data"""
        id = table.insert(serialized_data)
        return id

    def get_deserialized_player(self, serialized_player):
        """Get deserialized player from a serialized player
        Arg:
        serialized_player - player dict from db

        Return:
        player(Player) - player object"""
        player = Player(
            serialized_player["player_id"],
            serialized_player["last_name"],
            serialized_player["first_name"],
            serialized_player["date_of_birth"],
            serialized_player["sex"],
            serialized_player["total_score"],
            serialized_player["ranking"],
            serialized_player["opponents_list"],
        )
        return player

    def load_deserialized_players(self):
        """Populate the list of players with deserialized players"""
        for player in self.players_table:
            deserialized_player = self.get_deserialized_player(player)
            self.players.append(deserialized_player)

    def create_tournament(
        self,
        tournament_name: str,
        tournament_location: str,
        tournament_date: str,
        number_of_rounds: int,
        time_control: str,
        description: str,
        number_of_players: int,
        players: list,
    ):
        """Create tournament object.
        Args:
        tournament_name - Tournament's name
        tournament_location - Tournament's location
        tournament_date - Tournament's date
        number_of_rounds - number of rounds in the tournament
        time_control - time control (bullet, blitz or coup rapide)
        description - description for the tournament
        number_of_players - number of players in the tournament
        players - list of Players
        final_result - sorted list of players according to their score at the end of the tournament

        Return:
        tournament(Tournament) - tournament object"""
        tournament = Tournament(
            name=tournament_name,
            location=tournament_location,
            date=tournament_date,
            number_of_rounds=number_of_rounds,
            list_of_rounds=[],
            list_of_players=players,
            time_control=time_control,
            description=description,
            is_finished=False,
            final_result=[],
        )
        return tournament

    def save_tournament_to_db(self, tournament: Tournament):
        """Save tournament to db
        Arg:
        tournament(Tournament) - tournament object

        Return:
        serialized_tournament_updated - tournament dict from db, updated with the corresponding unique id"""
        serialized_tournament = tournament.get_serialized_tournament()

        """ Store doc_id of the saved tournament and update id of the tournament with the same. """
        tournament_id = self.save_to_db(self.tournaments_table, serialized_tournament)
        updated_ids = self.tournaments_table.update(
            {"id": tournament_id}, doc_ids=[tournament_id]
        )
        serialized_tournament_updated = self.tournaments_table.get(
            doc_id=updated_ids[0]
        )
        return serialized_tournament_updated

    def get_deserialized_tournament(self, serialized_tournament):
        """Get deserialized tournament from a serialized tournament
        Arg:
        serialized_tournament - tournament dict from db

        Return:
        tournament(Tournament) - tournament object"""
        tournament = Tournament(
            serialized_tournament["id"],
            serialized_tournament["name"],
            serialized_tournament["location"],
            serialized_tournament["date"],
            serialized_tournament["number_of_rounds"],
            [
                self.get_deserialized_round(round)
                for round in serialized_tournament["list_of_rounds"]
            ],
            [
                self.get_deserialized_player(player)
                for player in serialized_tournament["list_of_players"]
            ],
            serialized_tournament["time_control"],
            serialized_tournament["description"],
            serialized_tournament["is_finished"],
            [
                self.get_deserialized_player(player)
                for player in serialized_tournament["final_result"]
            ],
        )
        return tournament

    def load_deserialized_tournaments(self):
        """Populate the list of tournaments with deserialized tournaments"""
        for tournament in self.tournaments_table:
            deserialized_tournament = self.get_deserialized_tournament(tournament)
            self.tournaments.append(deserialized_tournament)

    def validate_player_id_exists(self, player_id: int):
        """Validate player id exists in the db
        Arg:
        player_id(int) - id to validate

        Return:
        bool - player id exists in db"""
        for player in self.players:
            if player.player_id == player_id:
                return True
        return False

    def save_round_to_db(self, round: Round):
        """Save round to database.
        Arg:
        round(Round) - round object

        Return:
        serialized_round_updated - round dict from db, updated with corresponding unique id"""
        serialized_round = round.get_serialized_round()

        """ Store doc_id of the saved round and update id with the same. """
        round_id = self.save_to_db(self.rounds_table, serialized_round)
        updated_ids = self.rounds_table.update({"id": round_id}, doc_ids=[round_id])
        serialized_round_updated = self.rounds_table.get(doc_id=updated_ids[0])
        return serialized_round_updated

    def get_deserialized_round(self, serialized_round):
        """Get deserialized round from a serialized round

        Arg:
        serialized_round - round dict from db

        Return:
        round(Round) - round object"""
        round = Round(
            serialized_round["id"],
            serialized_round["round_number"],
            serialized_round["round_name"],
            serialized_round["tournament_id"],
            [
                self.get_deserialized_match(match)
                for match in serialized_round["matches"]
            ],
            serialized_round["is_round_finished"],
        )
        round.start_date_time = serialized_round["start_date_time"]
        round.end_date_time = serialized_round["end_date_time"]
        return round

    def load_deserialized_rounds(self):
        """Populate the list of rounds with deserialized ronuds."""
        for round in self.rounds_table:
            deserialized_round = self.get_deserialized_round(round)
            self.rounds.append(deserialized_round)

    def save_match_to_db(self, match: Match):
        """Save match to database.
        Arg:
        match(Match) - match object

        Return:
        serialized_match_updated - match dict from db, updated with corresponding unique id"""
        serialized_match = match.get_serialized_match()

        """ Store doc_id of the saved match and update match_id with the same. """
        match_id = self.save_to_db(self.matches_table, serialized_match)
        updated_ids = self.matches_table.update(
            {"match_id": match_id}, doc_ids=[match_id]
        )
        serialized_match_updated = self.matches_table.get(doc_id=updated_ids[0])
        return serialized_match_updated

    def get_deserialized_match(self, serialized_match):
        """Get deserialized match from a serialized match
        Arg:
        serialized_match - match dict from db

        Return:
        match(Match) - match object"""
        match = Match(
            serialized_match["tournament_id"],
            serialized_match["round_id"],
            serialized_match["round_number"],
            [
                self.get_deserialized_player(player)
                for player in serialized_match["pair_of_players"]
            ],
            serialized_match["match_id"],
            serialized_match["winner"],
        )
        return match

    def load_deserialized_matches(self):
        """Populate the list of matches with deserialized matches"""
        for match in self.matches_table:
            deserialized_match = self.get_deserialized_match(match)
            self.matches.append(deserialized_match)

    def order_player_alphabetically(self, players: list):
        """Sort players in the alphabetical order
        Arg:
        players - list of players to be sorted

        Return:
        sorted_list - sorted list of players"""
        sorted_list = sorted(players, key=lambda player: player.last_name)
        return sorted_list

    def order_player_by_rank(self, players: list):
        """Sort players in the order of their ranking
        Arg:
        players - list of players to be sorted

        Return:
        sorted_list - sorted list of players"""
        sorted_list = sorted(players, key=attrgetter("ranking"), reverse=False)
        return sorted_list

    def get_players_in_a_tournament(self, tournament_id: int):
        """Get player in a tournament from tournament's id
        Arg:
        tournament_id - unique id of the tournament

        Return:
        list_of_players - list of Players in the tournament"""
        list_of_players = []
        for tournament in self.tournaments:
            if tournament.id == tournament_id:
                list_of_players = tournament.list_of_players
        return list_of_players

    def get_player_object_from_id(self, player_id: int):
        """Get player object from player_id

        Arg:
        player_id - unique id of the player

        Return:
        player object"""
        for player in self.players:
            if player.player_id == player_id:
                return player
