from threading import Lock, Condition
from time import sleep
# from demo import verboseprint

verboseprint = print

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
        verboseprint(f"[Elevator {self.id:<2}] Door opened on floor {self.floor}")
        sleep(1)

    def close_door(self) -> None:
        verboseprint(f"[Elevator {self.id:<2}] Door closed on floor {self.floor}")
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

    def move_to_floor(self, floor: int) -> None:
        self.direction = 1 if floor > self.floor else -1 if floor < self.floor else 0
        verboseprint(f"[Elevator {self.id:<2}] Heading to floor {floor}")

        while self.floor != floor:
            self.next_floor()

        # Stop at the floor
        self.direction = 0
        self.open_door()
        self.close_door()

    def add_request(self, floor: int) -> None:
        if floor < self.floor_min or floor > self.floor_max: raise ValueError(f"Requested floor {floor} is out of range")
        with self.condition:
            if len(self.request_list) > 0:
                for i in range(len(self.request_list)):
                    if self.request_list[i] > floor:
                        self.request_list.insert(i, floor)
                        break
            else: self.request_list.append(floor)

            verboseprint(f"[Elevator {self.id:<2}] Request added for floor {floor}  {self.request_list}")
            self.condition.notify()
    
    def add_request_last(self, floor: int) -> None:
        if floor < self.floor_min or floor > self.floor_max: raise ValueError(f"Requested floor {floor} is out of range")
        with self.condition:
            self.request_list.append(floor)
            verboseprint(f"[Elevator {self.id:<2}] Request added for floor {floor}")
            self.condition.notify()

    def execute_requests(self) -> None:
        while True:
            with self.condition:
                while not self.request_list:
                    verboseprint(f"[Elevator {self.id:<2}] Waiting for requests...")
                    self.condition.wait()

                floor = self.request_list.pop(0)

            self.move_to_floor(floor)

    def raise_not_operational(self) -> None:
        if not self.is_operational: raise Exception("Not operational")

    def __str__(self) -> str:
        return f"Elevator {self.id} is at {self.floor} - {'Running' if self.direction != 0 else 'Waiting'}"