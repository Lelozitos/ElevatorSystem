from threading import Lock, Condition
from time import sleep

verboseprint = print # TODO make a decent verboseprint

class Elevator():
    def __init__(self, id: int, floor_min: int, floor_max: int, floor: int = 0):
        self.id = id
        self.floor_min = floor_min
        self.floor_max = floor_max
        self.floor = 0
        self.direction = 0
        self.request_list = []
        self.is_operational = True
        self.lock = Lock()
        self.condition = Condition(self.lock)
    
    def open_door(self) -> None:
        verboseprint(f"Elevator {self.id:<2} -> Door opened on floor {self.floor}")
        sleep(1)

    def close_door(self) -> None:
        verboseprint(f"Elevator {self.id:<2} -> Door closed on floor {self.floor}")
        sleep(1)

    def next_floor(self) -> None:
        self.raise_not_operational()
        match self.direction:
            case 1:
                if self.floor + 1 > self.floor_max: raise ValueError("Cannot move up: Max floor reached")
                sleep(2)
                self.floor += 1 # self.floor += self.direction

            case -1:
                if self.floor - 1 < self.floor_min: raise ValueError("Cannot move down: Min floor reached")
                sleep(2)
                self.floor -= 1 # self.floor += self.direction
                
            case _:
                raise Exception("Direction is not set. Elevator is stationary")

    def move_to_floor(self, target_floor: int) -> None:
        verboseprint(f"Elevator {self.id:<2} -> Heading to floor {target_floor}")
        self.direction = 1 if target_floor > self.floor else -1 if target_floor < self.floor else 0

        while self.floor != target_floor:
            self.next_floor()

        # Stop at the floor
        self.direction = 0
        self.open_door()
        self.close_door()

    def add_request(self, floor: int) -> None:
        if floor < self.floor_min or floor > self.floor_max: raise ValueError(f"Requested floor {floor} is out of range")
        with self.condition:
            verboseprint(f"Elevator {self.id:<2} -> Request added for floor {floor}")
            self.request_list.append(floor)
            self.request_list.sort() # TODO works for now, but if someone calls the elevator down while it's going up, better to not stop at floor rn, only when backing
            self.condition.notify()

    def execute_requests(self) -> None: # TODO what if elevator is called in a between floor while heading towards another floor?
        while True:
            with self.condition:
                while not self.request_list:
                    verboseprint(f"Elevator {self.id:<2} -> Waiting for requests...")
                    self.condition.wait()

                target_floor = self.request_list.pop(0)

            self.move_to_floor(target_floor)

    def raise_not_operational(self) -> None:
        if not self.is_operational: raise Exception("Not operational")

    def __str__(self) -> str:
        return f"Elevator {self.id} is at {self.floor} - {'Running' if self.direction != 0 else 'Waiting'}"