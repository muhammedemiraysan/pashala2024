import tkinter as tk
from tkinter import ttk
import json

class ROVController:
    def __init__(self, master):
        self.master = master
        master.title("ROV Motor Controller")

        # Default maximum speed values
        self.motor_speeds = [250] * 9  # 6 motors + 2 turrets + 1 servo
        self.motor_directions = [0] * 9  # All forward directions by default
        self.config_file = "motor_config.json"

        self.create_widgets()
        self.load_config()

    def create_widgets(self):
        # Frame for motor controls
        control_frame = ttk.Frame(self.master)
        control_frame.grid(row=0, column=0, padx=10, pady=10)

        # Labels and sliders for motors
        motor_labels = ["Sol Ön", "Sol Üst", "Sol Arka", "Sağ Ön", "Sağ Üst", "Sağ Arka"]

        for i in range(6):  # 6 motors
            label_text = motor_labels[i]
            ttk.Label(control_frame, text=label_text).grid(row=i, column=0, padx=5)

            max_speed_label = ttk.Label(control_frame, text="Max Speed")
            max_speed_label.grid(row=i, column=1, padx=5)

            # Entry widget for setting maximum speed
            max_speed_entry = ttk.Entry(control_frame, width=10)
            max_speed_entry.insert(tk.END, str(self.motor_speeds[i]))
            max_speed_entry.grid(row=i, column=2, padx=5)

            # Update maximum speed function
            update_button = ttk.Button(control_frame, text="Update", command=lambda motor=i, entry=max_speed_entry: self.update_max_speed_from_entry(motor, entry))
            update_button.grid(row=i, column=3, padx=5)

            # Slider for setting maximum speed
            max_speed_slider = ttk.Scale(control_frame, from_=0, to=500, orient='horizontal',
                                         command=lambda val, motor=i: self.update_max_speed_from_slider(motor, val))
            max_speed_slider.set(self.motor_speeds[i])
            max_speed_slider.grid(row=i, column=4, padx=5)

            direction_label = ttk.Label(control_frame, text="Direction")
            direction_label.grid(row=i, column=5, padx=5)

            direction_button = ttk.Button(control_frame, text="Forward" if self.motor_directions[i] == 0 else "Reverse",
                                          command=lambda motor=i: self.toggle_direction(motor))
            direction_button.grid(row=i, column=6, padx=5)

            max_speed_value_label = ttk.Label(control_frame, text=str(self.motor_speeds[i]))
            max_speed_value_label.grid(row=i, column=7, padx=5)

            # Store references in the frame
            setattr(self, f"motor{i}_max_speed_entry", max_speed_entry)
            setattr(self, f"motor{i}_max_speed_slider", max_speed_slider)
            setattr(self, f"motor{i}_direction_button", direction_button)
            setattr(self, f"motor{i}_max_speed_value_label", max_speed_value_label)

        # Labels and sliders for turrets
        turret_labels = ["Turret 1", "Turret 2"]

        for i in range(6, 8):  # 2 turrets
            label_text = turret_labels[i - 6]
            ttk.Label(control_frame, text=label_text).grid(row=i, column=0, padx=5)

            max_speed_label = ttk.Label(control_frame, text="Max Speed")
            max_speed_label.grid(row=i, column=1, padx=5)

            # Entry widget for setting maximum speed
            max_speed_entry = ttk.Entry(control_frame, width=10)
            max_speed_entry.insert(tk.END, str(self.motor_speeds[i]))
            max_speed_entry.grid(row=i, column=2, padx=5)

            # Update maximum speed function
            update_button = ttk.Button(control_frame, text="Update", command=lambda motor=i, entry=max_speed_entry: self.update_max_speed_from_entry(motor, entry))
            update_button.grid(row=i, column=3, padx=5)

            # Slider for setting maximum speed
            max_speed_slider = ttk.Scale(control_frame, from_=0, to=500, orient='horizontal',
                                         command=lambda val, motor=i: self.update_max_speed_from_slider(motor, val))
            max_speed_slider.set(self.motor_speeds[i])
            max_speed_slider.grid(row=i, column=4, padx=5)

            direction_label = ttk.Label(control_frame, text="Direction")
            direction_label.grid(row=i, column=5, padx=5)

            direction_button = ttk.Button(control_frame, text="Forward" if self.motor_directions[i] == 0 else "Reverse",
                                          command=lambda motor=i: self.toggle_direction(motor))
            direction_button.grid(row=i, column=6, padx=5)

            max_speed_value_label = ttk.Label(control_frame, text=str(self.motor_speeds[i]))
            max_speed_value_label.grid(row=i, column=7, padx=5)

            # Store references in the frame
            setattr(self, f"motor{i}_max_speed_entry", max_speed_entry)
            setattr(self, f"motor{i}_max_speed_slider", max_speed_slider)
            setattr(self, f"motor{i}_direction_button", direction_button)
            setattr(self, f"motor{i}_max_speed_value_label", max_speed_value_label)

        # Labels and sliders for servo
        i = 8  # Servo
        label_text = "Servo"
        ttk.Label(control_frame, text=label_text).grid(row=i, column=0, padx=5)

        max_speed_label = ttk.Label(control_frame, text="Max Speed")
        max_speed_label.grid(row=i, column=1, padx=5)

        # Entry widget for setting maximum speed
        max_speed_entry = ttk.Entry(control_frame, width=10)
        max_speed_entry.insert(tk.END, str(self.motor_speeds[i]))
        max_speed_entry.grid(row=i, column=2, padx=5)

        # Update maximum speed function
        update_button = ttk.Button(control_frame, text="Update", command=lambda motor=i, entry=max_speed_entry: self.update_max_speed_from_entry(motor, entry))
        update_button.grid(row=i, column=3, padx=5)

        # Slider for setting maximum speed
        max_speed_slider = ttk.Scale(control_frame, from_=0, to=500, orient='horizontal',
                                     command=lambda val, motor=i: self.update_max_speed_from_slider(motor, val))
        max_speed_slider.set(self.motor_speeds[i])
        max_speed_slider.grid(row=i, column=4, padx=5)

        direction_label = ttk.Label(control_frame, text="Direction")
        direction_label.grid(row=i, column=5, padx=5)

        direction_button = ttk.Button(control_frame, text="Forward" if self.motor_directions[i] == 0 else "Reverse",
                                      command=lambda motor=i: self.toggle_direction(motor))
        direction_button.grid(row=i, column=6, padx=5)

        max_speed_value_label = ttk.Label(control_frame, text=str(self.motor_speeds[i]))
        max_speed_value_label.grid(row=i, column=7, padx=5)

        # Store references in the frame
        setattr(self, f"motor{i}_max_speed_entry", max_speed_entry)
        setattr(self, f"motor{i}_max_speed_slider", max_speed_slider)
        setattr(self, f"motor{i}_direction_button", direction_button)
        setattr(self, f"motor{i}_max_speed_value_label", max_speed_value_label)

        # Canvas for motor symbols
        self.canvas = tk.Canvas(self.master, width=500, height=400)
        self.canvas.grid(row=0, column=1, padx=10, pady=10)

        # Motor symbols
        self.motor_symbols = []

        motor_positions = [(50, 50), (50, 150), (50, 250),
                           (250, 50), (250, 150), (250, 250)]
        motor_labels = ["Sol Ön", "Sol Üst", "Sol Arka", "Sağ Ön", "Sağ Üst", "Sağ Arka"]

        for i, (x, y) in enumerate(motor_positions):
            symbol = self.canvas.create_rectangle(x, y, x+40, y+40, fill="blue")
            self.motor_symbols.append(symbol)
            self.canvas.create_text(x + 20, y + 45, text=motor_labels[i], font=("Arial", 10), fill="black")

        # Turret symbols
        turret_positions = [(350, 50), (350, 150)]
        turret_labels = ["Turret 1", "Turret 2"]

        for i, (x, y) in enumerate(turret_positions):
            symbol = self.canvas.create_rectangle(x, y, x+40, y+40, fill="green")
            self.motor_symbols.append(symbol)
            self.canvas.create_text(x + 20, y + 45, text=turret_labels[i], font=("Arial", 10), fill="black")

        # Servo symbol
        x, y = 450, 250
        symbol = self.canvas.create_rectangle(x, y, x+40, y+40, fill="red")
        self.motor_symbols.append(symbol)
        self.canvas.create_text(x + 20, y + 45, text="Servo", font=("Arial", 10), fill="black")

        # Save configuration button
        save_button = ttk.Button(self.master, text="Save Configuration", command=self.save_config)
        save_button.grid(row=1, column=0, columnspan=2, pady=10)

    def update_max_speed_from_slider(self, motor, value):
        self.motor_speeds[motor] = int(float(value))
        max_speed_value_label = getattr(self, f"motor{motor}_max_speed_value_label")
        max_speed_value_label.config(text=str(self.motor_speeds[motor]))
        self.update_motor_color(motor)

    def update_max_speed_from_entry(self, motor, entry):
        try:
            speed = int(entry.get())
            if 0 <= speed <= 500:
                self.motor_speeds[motor] = speed
                max_speed_slider = getattr(self, f"motor{motor}_max_speed_slider")
                max_speed_slider.set(speed)
                max_speed_value_label = getattr(self, f"motor{motor}_max_speed_value_label")
                max_speed_value_label.config(text=str(speed))
                self.update_motor_color(motor)
            else:
                print(f"Invalid speed value for motor {motor}. Must be between 0 and 500.")
        except ValueError:
            print(f"Invalid speed value for motor {motor}. Must be an integer.")

    def toggle_direction(self, motor):
        if self.motor_directions[motor] == 0:
            self.motor_directions[motor] = 1
            direction_button = getattr(self, f"motor{motor}_direction_button")
            direction_button.config(text="Reverse")
        else:
            self.motor_directions[motor] = 0
            direction_button = getattr(self, f"motor{motor}_direction_button")
            direction_button.config(text="Forward")
        self.update_motor_color(motor)

    def update_motor_color(self, motor):
        speed = self.motor_speeds[motor]
        direction = self.motor_directions[motor]
        normalized_speed = speed / 500  # Normalize to 0-1 range
        intensity = int(normalized_speed * 255)
        if direction == 0:
            color = f'#0000{intensity:02x}'  # Blue color, intensity with speed
        else:
            color = f'#{intensity:02x}0000'  # Red color, intensity with speed

        if motor < 6:
            self.canvas.itemconfig(self.motor_symbols[motor], fill=color)
        elif motor == 6 or motor == 7:
            self.canvas.itemconfig(self.motor_symbols[motor], fill=color)
        else:
            self.canvas.itemconfig(self.motor_symbols[motor], fill=color)

    def save_config(self):
        config = {
            "motor_speeds": self.motor_speeds,
            "motor_directions": self.motor_directions
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f)
        print("Configuration saved!")

    def load_config(self):
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.motor_speeds = config.get("motor_speeds", self.motor_speeds)
                self.motor_directions = config.get("motor_directions", self.motor_directions)
        except FileNotFoundError:
            print("Configuration file not found. Using default values.")
        except json.JSONDecodeError:
            print("Error reading configuration file. Using default values.")

        for i in range(9):  # 6 motors + 2 turrets + 1 servo
            self.update_motor_color(i)
            max_speed_entry = getattr(self, f"motor{i}_max_speed_entry")
            max_speed_entry.delete(0, tk.END)
            max_speed_entry.insert(tk.END, str(self.motor_speeds[i]))

            max_speed_slider = getattr(self, f"motor{i}_max_speed_slider")
            max_speed_slider.set(self.motor_speeds[i])

            direction_button = getattr(self, f"motor{i}_direction_button")
            direction_button.config(text="Forward" if self.motor_directions[i] == 0 else "Reverse")

            max_speed_value_label = getattr(self, f"motor{i}_max_speed_value_label")
            max_speed_value_label.config(text=str(self.motor_speeds[i]))


def run_rov_controller():
    root = tk.Tk()
    app = ROVController(root)
    root.mainloop()

if __name__ == "__main__":
    run_rov_controller()
