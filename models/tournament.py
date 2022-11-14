"""Define the tournament"""


class Tournament:
    """Tournament class"""

    def __init__(
        self,
        id=0,
        name="",
        location="",
        date="",
        number_of_rounds=4,
        list_of_rounds=[],
        list_of_players=[],
        time_control="",
        description="",
        is_finished=False,
    ):
        """Init the following attributes:
        -id: Tournament's unique id, 0 by default
        -name: name of the tournament
        -location: location of the tournament
        -date: tournament date
        -number_of_rounds: 4 by default
        -list_of_rounds: list of round objects
        -list_of_players: list of player objects
        -time_control: type of time limit for
            a tournament (bullet, blitz or rapid)
        -description: general remarks of the tournament director
        -is_finished: boolean to indicate end of the tournament
        """
        self.id = id
        self.name = name
        self.location = location
        self.date = date
        self.number_of_rounds = number_of_rounds
        self.list_of_rounds = list_of_rounds
        self.list_of_players = list_of_players
        self.time_control = time_control
        self.description = description
        self.is_finished = is_finished

    def __str__(self):
        """Used in print"""
        return f"Tournoi {self.name}, Lieu : {self.location}, le {self.date}"

    def get_serialized_tournament(self):
        """Serialize tournament

        Return:
        dict - serialized tournament"""
        serialized_tournament = {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "number_of_rounds": self.number_of_rounds,
            "list_of_rounds": [
                round.get_serialized_round() for round in self.list_of_rounds
            ],
            "list_of_players": [
                player.get_serialized_player() for player in self.list_of_players
            ],
            "time_control": self.time_control,
            "description": self.description,
            "is_finished": self.is_finished,
        }

        return serialized_tournament
