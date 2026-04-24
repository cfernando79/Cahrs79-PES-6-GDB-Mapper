# player.py
class Player:
    def __init__(self, pid, name, nationality, club_idx):
        self.id = pid
        self.name = name
        self.nationality = nationality
        self.club_idx = club_idx

    def get_club(self, club_db):
        return club_db.get_name(self.club_idx)