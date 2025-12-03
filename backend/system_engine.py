import time
import threading
import time

MEASUREMENT_TIME = 0.01  # seconds
MAX_PLOT_MEASURMENTS = 1000
TEST_RUN_TIME = 1800 #[10s]
MAX_MOTOR_SPEED = 3000 #[10rpm]


class SystemEngine:
    def __init__(self, data_logger, motor_controller, sensor_reader):
        self.data_logger = data_logger
        self.motor_controller = motor_controller
        self.sensor_reader = sensor_reader

        self.meassurements = self.sensor_reader._sensors
        self.velocity_setpoint = 0
        self.meassurement_time = 0
        
        self.velocity_plot = {"meassurement_time": [], "rpm": []}
        
        self.thread = None
        self.test_active = False
        self.lock = threading.Lock()

    def get_measurements(self): #TODO: consider switching to queue
        with self.lock:
            return self.meassurements.copy()  # return a copy to avoid race conditions
    
    def set_velocity(self, velocity):
        #add mutex
        self.velocity_setpoint = velocity

    def get_velocity_plot(self):
        with self.lock:
            return self.velocity_plot["rpm"].copy(), self.velocity_plot["meassurement_time"].copy()

    def get_time(self):
        return self.meassurement_time

    def get_map_size(self):
        return TEST_RUN_TIME, MAX_MOTOR_SPEED

    def monitor_meassurements(self):
        # TODO: if temp is not in proper range, disable testing
        # TODO: if torque is not in proper range, disable testing?
        # TODO: if motor_speed is not in proper range, disable testing?

        # TODO: other dangerous cases?
        pass

    def test_running(self):
        return self.test_active

    def test_execution(self):  
        self.test_active = True 
        self.motor_controller.run_motor_map()
        try:
            while self.motor_controller.running():
                #TODO: add option for sweaching motor control (setpoint/mottor map)
                self.motor_controller.run_motor_map()
                self.motor_controller.set_speed(self.velocity_setpoint)

                meassurements, self.meassurement_time = self.sensor_reader.read_all()

                with self.lock:
                    self.meassurements = meassurements.copy() #TODO: make sure meassurements is doesn't contain nested objects (this is shallow copy)
                    motor_velocity = self.motor_controller.get_speed() #TODO: make sure it doesnt block controller (mutex)

                    self.velocity_plot["rpm"].append(motor_velocity) #TODO: save time and velocity to one datastructure
                    self.velocity_plot["meassurement_time"].append(self.meassurement_time)
                    if len(self.velocity_plot["meassurement_time"]) > MAX_PLOT_MEASURMENTS:
                        self.velocity_plot["rpm"].pop(0)
                        self.velocity_plot["meassurement_time"].pop(0)

                self.data_logger.log(meassurements)
                
                if self.monitor_meassurements():
                    self.motor_controller.reset()
                    #TODO: disable testing
                    break

                time.sleep(MEASUREMENT_TIME)
        finally:
            # ensure motors are disabled at the end of the test
            self.test_active = False
            self.motor_controller.reset()