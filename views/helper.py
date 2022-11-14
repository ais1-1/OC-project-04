""" Define helper functions """
from datetime import datetime, date
from models.match import Match
import sys


def validate_date(date_input: str):
    """Validate date input and show error message in case of invalid date

    Args:
    date_input (str) - date input from user

    Returns:
    bool - date is valid"""

    try:
        datetime.strptime(date_input, "%d/%m/%Y").date()
        return True
    except ValueError:
        print("Date non valide. Le format doit être jj/mm/aaaa.")
        return False


def validate_date_in_future(date_input: str):
    """Validate date input is in the future and raise exception if it is not

    Arg:
    date_input (str) - date input from user

    Returns:
    bool - date is in the future"""
    now = date.today()
    valid_date = datetime.strptime(date_input, "%d/%m/%Y").date()

    try:
        if valid_date < now:
            raise Exception
        else:
            return True
    except Exception:
        print("Votre date est dans le passé. Veuillez entrer une date valide.")
        return False


def validate_date_in_past(date_input: str):
    """Validate date input is in the past and raise exception if it is not

    Arg:
    date_input (str) - date input from user

    Returns:
    bool - date is in the past"""
    now = date.today()
    valid_date = datetime.strptime(date_input, "%d/%m/%Y").date()
    try:
        if valid_date > now:
            raise Exception
        else:
            return True
    except Exception:
        print("Le date est dans le futur. Veuillez entrer une date valide.")
        return False


def validate_date_time(date_time_input: str):
    """Validate date time input and show error message in case of invalid date time

    Args:
    date_time_input (str) - date time input from user

    Returns:
    bool - date is valid"""

    try:
        datetime.strptime(date_time_input, "%d/%m/%Y:%H:%M")
        return True
    except ValueError:
        if date_time_input.strip() != "":
            print("Date time non valide !")
        return False


def validate_round_end_date(date_time_input: str):
    """Validate round's end date time is in the future

    Arg:
    date_time_input - date time input from user

    Return:
    bool - date time input is in the future"""
    now = datetime.now()
    valid_date_time = datetime.strptime(date_time_input, "%d/%m/%Y:%H:%M")
    try:
        if valid_date_time < now:
            raise Exception
        else:
            return True
    except Exception:
        print(
            "La date est incorrect, elle est dans le passé. Veuillez entrer une date valide."
        )
        return False


def validate_time_control(time_control_input: str):
    """Validate time control input if invalid show an error message

    Args:
    time_control_input(str) - time control input from user

    Returns:
    bool - time control input is valid"""
    if time_control_input.lower() == "bullet":
        time_control_input = "Bullet"
        return True
    elif time_control_input.lower() == "blitz":
        time_control_input = "Blitz"
        return True
    elif time_control_input.lower() == "coup rapide":
        time_control_input = "Coup Rapide"
        return True
    else:
        if len(time_control_input) > 0:
            print(
                "Entrée incorrect. " + "Veuillez entrez Bullet, Blitz ou Coup Rapide."
            )
        return False


def validate_winner_entry(match: Match, string_input: str):
    """Validate if the winner entry belongs to
    the players in the existing matches.

    Args:
    match (Match) - match object
    string_input (str) - winner id input from user

    Returns:
    bool - winner entry is valid"""
    id_01 = str(match.player_01.player_id)
    id_02 = str(match.player_02.player_id)
    valid_entries = [id_01, id_02, f"{id_01} {id_02}", f"{id_02} {id_01}"]
    if string_input in valid_entries:
        return True
    else:
        return False


def display_prompt_after_selection():
    """Display prompt for quitting or going back to the previous menu

    Return:
    int - user's choice"""
    user_input = ""
    try:
        user_input = int(
            input(
                "Si vous voulez quitter l'application tapez 1 ;\n"
                + "Pour retourner dans le menu précédent tapez 2 ;\nVotre choix : "
            )
        )
    except Exception:
        print("Veuillez entrer un nombre valide pour indiquer votre choix")

    if user_input == 1:
        """Quit the program"""
        sys.exit()
    else:
        user_input = 2
        return user_input

