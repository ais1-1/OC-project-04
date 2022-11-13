"""Define the match"""


class Match:
    """Match class"""

    def __init__(
        self,
        tournament_id=0,
        round_id=0,
        round_number=0,
        pair_of_players=[],
        match_id=0,
        winner=[],
    ):
        """Init the following attributes:
        -tournament_id: unique id of the tournament
                        in which the match is happening
        -round_id: unique id of the round in which the round is happening
        -pair_of_players: list of the 2 players
        -match_id: unique id of the match
        -player_01: first player in the list pair_of_players
        -player_02: second player in the list pair_of_players
        -winner: list of winner ids of the match
        -game_duration: duration of the match (could be useful for stats)"""
        self.tournament_id = tournament_id
        self.round_id = round_id
        self.round_number = round_number
        self.pair_of_players = pair_of_players
        self.player_01 = pair_of_players[0]
        self.player_02 = pair_of_players[1]
        self.match_id = match_id
        self.winner = winner
        self.game_duration = ""

    def __str__(self):
        """Used in print"""
        string = f"{self.player_01} Vs {self.player_02}"
        return string

    def get_serialized_match(self):
        """Serialize match

        Return:
        dict - serialized match"""
        serialized_match = {
            "tournament_id": self.tournament_id,
            "round_id": self.round_id,
            "round_number": self.round_number,
            "pair_of_players": [
                player.get_serialized_player() for player in self.pair_of_players
            ],
            "match_id": self.match_id,
            "winner": self.winner,
        }

        return serialized_match
