from threading import Thread
from request import Request
from elevator import Elevator

class ElevatorController():
    def __init__(self, n_elevators: int, floor_min: int, floor_max: max) -> None:
        if n_elevators < 1: raise ValueError("Invalid number of elevators")
        self.elevators = []
        for i in range(n_elevators): self.elevators.append(Elevator(i, floor_min, floor_max))
        # self.run()

    def add_request(self, request: Request):
        target_floor = request.floor
        direction = request.direction

        same_direction = []
        stopped = []
        opposite_direction = []

        for elevator in self.elevators:
            if elevator.direction == direction:
                if (direction == 1 and elevator.floor <= target_floor) or (
                    direction == -1 and elevator.floor >= target_floor
                ):
                    same_direction.append(elevator)
            elif elevator.direction == 0:
                stopped.append(elevator)
            else:
                opposite_direction.append(elevator)

        if same_direction:
            chosen = min(same_direction, key=lambda e: abs(e.floor - target_floor))
        elif stopped:
            chosen = min(stopped, key=lambda e: abs(e.floor - target_floor))
        elif opposite_direction:
            chosen = min(opposite_direction, key=lambda e: abs(e.floor - target_floor))
        else:
            raise Exception("No elevators available")

        chosen.add_request(target_floor)

    def add_requests(self, floors: list):
        for floor in floors:
            self.add_request(Request(floor))

    def run(self):
        for elevator in self.elevators:
            Thread(target=elevator.execute_requests, daemon=True).start()