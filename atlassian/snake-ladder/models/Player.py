

class Player:
    def __init__(self, player_name) -> None:
        self.player_name = player_name
        self.position = ()
        pass
    
    def get_position(self):
        return self.position
    
    def set_position(self, position):
        self.position = position
        return True