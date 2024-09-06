import pygame
import pprint

class JoystickController:
    def __init__(self):
        """Initialize the joystick and keyboard components"""
        pygame.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        # Initialize axis, button, hat, and keyboard data
        self.axis_data = {
            0: 0.0,
            1: 0.0,
            2: 0.0,
            3: 0.0
        }
        self.button_data = {
            i: False for i in range(self.joystick.get_numbuttons())
        }
        self.hat_data = {}
        self.keyboard_data = {
            pygame.K_m: False,  # Key 'm'
            pygame.K_o: False,   # Key 'o'
            pygame.K_k: False   # Key 'k'
        }

        # Initialize hat data
        for i in range(self.joystick.get_numhats()):
            self.hat_data[i] = (0, 0)

        # Create a window
        self.screen = pygame.display.set_mode((640, 480))  # Adjust the size as needed
        pygame.display.set_caption("Joystick and Keyboard Input")

    def listen(self):
        """Listen for joystick and keyboard events and update data"""
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                self.axis_data[event.axis] = round(event.value, 2)
            elif event.type == pygame.JOYBUTTONDOWN:
                self.button_data[event.button] = True
            elif event.type == pygame.JOYBUTTONUP:
                self.button_data[event.button] = False
            elif event.type == pygame.JOYHATMOTION:
                self.hat_data[event.hat] = event.value
            elif event.type == pygame.KEYDOWN:
                if event.key in self.keyboard_data:
                    self.keyboard_data[event.key] = True
            elif event.type == pygame.KEYUP:
                if event.key in self.keyboard_data:
                    self.keyboard_data[event.key] = False

        # Optionally, update keyboard state for all keys
        keys = pygame.key.get_pressed()
        for key in self.keyboard_data.keys():
            if keys[key]:
                self.keyboard_data[key] = True
            else:
                self.keyboard_data[key] = False

    def get_key_name(self, key):
        """Get the name of the key based on its pygame key constant"""
        try:
            return pygame.key.name(key)
        except Exception as e:
            return f"Unknown key ({key})"

def main():
    controller = JoystickController()
    running = True
    while running:
        controller.listen()
        
        # Check for the QUIT event to close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Clear the screen
        controller.screen.fill((0, 0, 0))  # Fill the screen with black
        
        # Print axis data
        print("Axis Data:", controller.axis_data)
        # Print button states
        print("Button Data:", controller.button_data)
        # Print hat data
        print("Hat Data:", controller.hat_data)
        # Print keyboard data
        print("Keyboard Data:")
        for key, pressed in sorted(controller.keyboard_data.items()):
            print(f"  {controller.get_key_name(key)}: {'Pressed' if pressed else 'Released'}")
        
        pygame.display.flip()  # Update the display
        pygame.time.wait(100)  # To prevent flooding the console with messages

    pygame.quit()

if __name__ == "__main__":
    main()
