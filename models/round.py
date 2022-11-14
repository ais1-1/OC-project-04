"""Define the round"""
from datetime import datetime


class Round:
    """Round class"""

    def __init__(
        self,
        id=0,
        round_number=0,
        round_name="",
        tournament_id=0,
        matches=[],
        is_round_finished=False,
    ):
        """Init the following attirbutes:
        -id: unique id for the round
        -round_number: round number within a tournament
        -round_name: round name
        -tournament_id: unique id of the tournament in which
                        the round is happening
        -is_round_finished: boolean to indicate end of the round
        -matches: list of matches assosciated with the round
        -start_date_time: date and time of the beginning of the round
        -end_date_time: date and time of the ending"""
        self.id = id
        self.round_number = round_number
        self.round_name = round_name
        self.tournament_id = tournament_id
        self.is_round_finished = is_round_finished
        self.matches = matches
        self.start_date_time = datetime.now()
        self.end_date_time = ""

    def __str__(self):
        """Used in print"""
        string = f"{self.round_name} {self.round_number} with matches {self.matches}"
        return string

    def get_serialized_round(self):
        """Serialize round

        Return:
        dict - serialized round"""
        serialized_round = {
            "id": self.id,
            "round_number": self.round_number,
            "round_name": self.round_name,
            "tournament_id": self.tournament_id,
            "matches": [match.get_serialized_match() for match in self.matches],
            "is_round_finished": self.is_round_finished,
            "start_date_time": str(self.start_date_time),
            "end_date_time": str(self.end_date_time),
        }

        return serialized_round
