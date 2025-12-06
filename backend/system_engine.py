import threading
import time

MEASUREMENT_TIME = 0.01  # seconds
MAX_PLOT_MEASURMENTS = 1000
TEST_RUN_TIME = 20 #[s]
MAX_MOTOR_SPEED = 3000 #[rpm]

ERROR_DETECTED = 666
STATUS_OK = 7

class SystemEngine:
    def __init__(self, data_logger, motor_controller, sensor_reader):
        self.data_logger = data_logger
        self.motor_controller = motor_controller
        self.sensor_reader = sensor_reader

        self.meassurements = self.sensor_reader._sensors
        self.velocity_setpoint = 0
        self.meassurement_time = 0
        
        self.test_map = {'timestamp': [0, 5, 10, 15], 'rpm': [0, 300, 500, 1000]}
        self.map_test_startup_time = None

        self.velocity_plot = {"meassurement_time": [], "rpm": []}
        
        self.MAP_CONTROL = 12
        self.SETPOINT_CONTROL = 73
        self.control = self.SETPOINT_CONTROL

        self.thread = None
        self.test_active = False
        self.lock = threading.Lock()

    def initialize(self):
        self.motor_controller.initialize()

    def set_control_type(self, control_type):
        if control_type != self.MAP_CONTROL and control_type != self.SETPOINT_CONTROL:
            print("not a proper control type")
            return
        self.control = control_type

    def get_measurements(self): #TODO: consider switching to queue
        with self.lock:
            return self.meassurements.copy()  # return a copy to avoid race conditions
    
    def get_motor_test_map(self):
        #TODO: add mutex
        return self.test_map['timestamp'].copy(), self.test_map['rpm'].copy()
    
    def set_motor_test_map(self, timestamps:list[int], rpms:list[int]):
        self.test_map['timestamp'] = timestamps #TODO: add mutex
        self.test_map['rpm'] = rpms

    def set_velocity(self, velocity):
        #add mutex
        self.velocity_setpoint = velocity

    def get_velocity_plot(self):
        with self.lock:
            return self.velocity_plot["rpm"].copy(), self.velocity_plot["meassurement_time"].copy()

    def get_time(self):
        return self.meassurement_time

    def get_map_size(self):
        scale_ratio = TEST_RUN_TIME/(4*MAX_MOTOR_SPEED)
        return TEST_RUN_TIME, MAX_MOTOR_SPEED, scale_ratio

    def monitor_meassurements(self):
        # TODO: if temp is not in proper range, disable testing
        # TODO: if torque is not in proper range, disable testing?
        # TODO: if motor_speed is not in proper range, disable testing?

        # TODO: other dangerous cases?
        pass

    def test_running(self):
        return self.test_active

    def motor_data_processing(self, test_time):
        self.meassurement_time = test_time #TODO: set correct time for measurements
        meassurements, _ = self.sensor_reader.read_all()

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
            self.map_test_startup_time = None
            raise Exception("Motor control error")

    def motor_map(self):
        self.map_test_startup_time = time.time()
        while self.motor_controller.running():
            current_time = time.time() - self.map_test_startup_time
            if current_time > TEST_RUN_TIME:
                self.motor_controller.disable_motors() #TODO: handle disabling properly

            timestamp_map, rpm_map = self.get_motor_test_map()
            self.motor_controller.run_motor_map(current_time, timestamp_map, rpm_map)          

            self.motor_data_processing(current_time)
            time.sleep(MEASUREMENT_TIME)

        #TODO: handle disabling map test corectly
        self.map_test_startup_time = None

    def test_execution(self):  
        self.test_active = True 
        while True:
            if self.motor_controller.running():
                try:
                    if self.control == self.MAP_CONTROL:
                        self.motor_map()

                    elif self.control == self.SETPOINT_CONTROL:
                        self.motor_controller.set_speed(self.velocity_setpoint)
                        self.motor_data_processing(time.time())

                except Exception as e:
                    # ensure motors are disabled at the end of the test
                    self.test_active = False
                    self.motor_controller.reset()
                    print(e)
                    #TODO: test if throwing exeptions is working in both scenerios
            
            #TODO: handle motor disabling properly
            time.sleep(MEASUREMENT_TIME) #TODO: refactor this function so this thread doesnt block the whole program