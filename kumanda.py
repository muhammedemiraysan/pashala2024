import pygame


class JoystickController:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        #self.num_axes = self.joystick.get_numaxes()

    def get_axes_values(self):
        # Handle Pygame Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

        # Get Values of Joystick Axes
        axis_0 = self.joystick.get_axis(0)
        axis_1 = self.joystick.get_axis(1)
        axis_2 = self.joystick.get_axis(2)
        axis_3 = self.joystick.get_axis(3)
        button_1 = self.joystick.get_button(0)
        return (str(axis_0) + "," + str(axis_1) + "," + str(axis_2) + "," + str(axis_3) + "," + str(button_1))

    def run(self):
        # Loop Until User Quits
        done = False
        while not done:
            # Get Joystick Axes Values
            axes_values = self.get_axes_values()

            # Check if Axes Values are Valid
            if axes_values is None:
                done = True
            else:
                # Print Axes Values to Console
                print(f"Axis 0: {axes_values[0]:.2f}, Axis 1: {axes_values[1]:.2f}, Axis 2: {axes_values[2]:.2f}, Axis 3: {axes_values[3]:.2f}")

        # Quit Pygame
        pygame.quit()
