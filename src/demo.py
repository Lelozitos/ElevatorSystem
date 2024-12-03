from elevator_controller import ElevatorController
from request import Request
import time
import random

# Main demo function
def demo():
    print("=== Starting Elevator System Demo ===")
    
    # Initialize the ElevatorController
    controller = ElevatorController(2, 0, 5)  # 2 elevators, floors 0 to 5
    
    try:
        # Start the elevator threads -> maybe run automatic from constructor?
        controller.run()
        
        # Add some initial requests
        controller.add_requests([5, 1])
        time.sleep(1)
        controller.add_requests([3])
        time.sleep(5)
        
        # Simulate dynamic requests
        for _ in range(5):
            floor = random.randint(0, 5)
            controller.add_request(Request(floor))
            time.sleep(random.uniform(1, 3))
        
        # Let the demo run
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("Shutting down elevators...")
        controller.shutdown()  # Ensure elevators stop gracefully

# Run the demo
if __name__ == "__main__":
    demo()
