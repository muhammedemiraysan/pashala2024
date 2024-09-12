class PID:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.previous_error = 0
        self.integral = 0
        
    def compute(self, setpoint, measurement):
        error = setpoint - measurement
        P = self.Kp * error
        self.integral += error
        I = self.Ki * self.integral
        D = self.Kd * (error - self.previous_error)
        output = P + I + D
        self.previous_error = error
        return output
    
    def is_within_tolerance(self, measurement, setpoint, tolerance):
        return abs(setpoint - measurement) <= tolerance
