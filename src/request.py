# Outside the elevator, request has floor and direction (to determine which elevator is best to get them)
# Inside the elevator, request only has floor

class Request():
    def __init__(self, floor: int, direction: int = None):
        self.floor = floor
        self.direction = direction