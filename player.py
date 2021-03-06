
class Player:
    
    def __init__(self, name, fide_id=None, rating=None, rapid=None, blitz=None, federation=""):
        self.name = name
        self.fide_id = str(fide_id)
        self.rating = rating
        self.rapid = rapid
        self.blitz = blitz
        self.federation = federation
        self.scores = {"Classical": {}, "RapidBlitz": {}}
        self.current_score = None
        
    def __repr__(self):
        return self.name + " (" + str(self.rating) + ")"