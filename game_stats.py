class GameStats:

    def __init__(self,ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False

        filename = 'save_highest_score.txt'

        with open(filename, 'r') as file_object:
            self.highest_score = int(file_object.read())

    def reset_stats(self):
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
