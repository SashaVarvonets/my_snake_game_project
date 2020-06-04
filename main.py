from functions import show_menu_screen, run_game


# Game could be in 2 condition "WAITING" | "RUNNING"
GAME_CONDITION = "WAITING"


def draw_screen():
    pass


def start_game():
    while True:
        if GAME_CONDITION == "RUNNING":
            """
            change snake position
            draw snake
            """
        elif GAME_CONDITION == "WAITING":

            """
            waiting for pressing the start button
            change game status
            """

        """
        draw a screen
        """
        show_menu_screen()
        run_game()


if __name__ == '__main__':
    start_game()
