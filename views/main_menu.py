""" Define the main menu view """


MENU_OPTIONS = {
    1: "Créer un tournoi",
    2: "Charger un tournoi en cours",
    3: "Ajouter des joueurs",
    4: "Modifier le classement des joueurs",
    5: "Voir les rapports",
    6: "Quitter l'application",
}


TITLE = "CTM - Chess Tournament Manager"
TITLE_DECO = "*******************************"


class MainMenuView:
    """MainMenuView class"""

    def __init__(self):
        """Init the following attribute:
        choice - choice of the user from the MENU_OPTIONS (1 to 6)

        Init methods:
        display_menu - display the available options with title
        get_user_selection - user prompt"""
        self.choice = ""
        self.display_menu()
        self.get_user_selection()

    def display_menu(self):
        """Display the main menu with the title of the program."""
        print(TITLE_DECO)
        print(TITLE)
        print(TITLE_DECO)
        for key in MENU_OPTIONS.keys():
            print(key, " : ", MENU_OPTIONS[key])

    def get_user_selection(self):
        """Display the user input section to enter a choice
        and return the choice."""
        self.choice = 0

        while self.choice > 6 or self.choice <= 0:
            try:
                self.choice = int(input("Saisissez votre choix : "))
                if self.choice > 6 or self.choice <= 0:
                    raise Exception
                else:
                    pass
            except Exception:
                print(
                    "Veuillez entrer un nombre entre 1 et 6"
                    + " pour indiquer votre choix"
                )

        if self.choice == 1:
            return 1
        elif self.choice == 2:
            return 2
        elif self.choice == 3:
            return 3
        elif self.choice == 4:
            return 4
        elif self.choice == 5:
            return 5
        elif self.choice == 6:
            return 6
        else:
            print(
                "Veuillez entrer un nombre entre 1 et 6" + " pour indiquer votre choix"
            )
            self.choice = 0
