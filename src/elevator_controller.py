from threading import Thread
from request import Request
from elevator import Elevator

class ElevatorController():
    def __init__(self, n_elevators: int, floor_min: int, floor_max: max):
        if n_elevators < 1: raise ValueError("Invalid number of elevators")
        self.elevators = []
        for i in range(n_elevators): self.elevators.append(Elevator(i, floor_min, floor_max))
        self.threads = []
        # self.run()

    def add_request(self, request: Request) -> None: # TODO In theory you can't request same floor twice, make sure of that
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


        if chosen in opposite_direction:
            chosen.add_request_last(target_floor)
        else:
            chosen.add_request(target_floor)

    def add_requests(self, floors: list) -> None:
        for floor in floors:
            self.add_request(Request(floor))

    def run(self) -> None:
        for elevator in self.elevators:
            Thread(target=elevator.execute_requests, daemon=True).start()

    def shutdown(self):
        for elevator in self.elevators:
            elevator.is_operational = False
            elevator.direction = 0
        for thread in self.threads:
            thread.join()