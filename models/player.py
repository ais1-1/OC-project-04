"""Define the player"""


class Player:
    """Player class"""

    def __init__(
        self,
        player_id=0,
        last_name="",
        first_name="",
        date_of_birth="",
        sex="",
        total_score=0,
        ranking=0,
        opponents_list=[],
    ):
        """Init the following attributes:
        -player_id: unique id for the player
        -last_name: last name of the player
        -first_name: first name of the player
        -date_of_birth: date of birth in the format dd/mm/yyyy
        -sex: sex of the player (male or female)
        -total_score: total score of the player in the tournament
        -ranking: ranking of the player, a positive integer
        -opponents_list: list of opponent player ids in a tournament
        """
        self.player_id = player_id
        self.last_name = last_name
        self.first_name = first_name
        self.date_of_birth = date_of_birth
        self.sex = sex
        self.total_score = total_score
        self.ranking = ranking
        self.opponents_list = opponents_list

    def __str__(self):
        """Used in print"""
        return f"{self.last_name} {self.first_name}"

    def get_serialized_player(self):
        """Serialize player

        Return:
        dict - serialized player"""
        serialized_player = {
            "player_id": self.player_id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "date_of_birth": self.date_of_birth,
            "sex": self.sex,
            "total_score": self.total_score,
            "ranking": self.ranking,
            "opponents_list": self.opponents_list,
        }

        return serialized_player
