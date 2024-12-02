from threading import Thread
from request import Request
from elevator import Elevator

class ElevatorController():
    def __init__(self, n_elevators: int, floor_min: int, floor_max: max) -> None:
        if n_elevators < 1: raise ValueError("Invalid number of elevators")
        self.elevators = []
        for i in range(n_elevators): self.elevators.append(Elevator(i, floor_min, floor_max))

    def add_request(self, request: Request): # TODO see which elevator is closer and heading the same direction
        self.elevators[0].add_request(request.floor)

    def add_requests(self, floors: list):
        for floor in floors:
            self.add_request(Request(floor))

    def run(self):
        for elevator in self.elevators:
            Thread(target=elevator.execute_requests).start()