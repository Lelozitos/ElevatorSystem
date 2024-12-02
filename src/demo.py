from elevator_controller import ElevatorController
import time

# verbose = True
# verboseprint = print if verbose else lambda *a, **k: None

controller = ElevatorController(2, 0, 5)

controller.run()
controller.add_requests([5, 1])
time.sleep(1)
controller.add_requests([3])
time.sleep(40)
controller.add_requests([2])