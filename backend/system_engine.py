import threading
import time
from dataclasses import dataclass
from common.data_classes import ServerId, SERVERS
from common.server import ServerInstance
import copy

MEASUREMENT_TIME = 0.01  # seconds
MAX_DRIVE_PLOT_MEASURMENTS = 50
MAX_SENSOR_PLOT_MEASURMENTS = 50

ERROR_DETECTED = 666
STATUS_OK = 7


@dataclass
class VelocityPlot:
    meassurement_time: list[int] #TODO: make sure it's int not float
    rpm:  list[int] #TODO: make sure it's int not float

@dataclass
class TorquePlot:
    meassurement_time: list[int] #TODO: make sure it's int not float
    torque:  list[int] #TODO: make sure it's int not float

@dataclass
class SensorMeasurementPlot:
    meassurement_time: list[float] = None #TODO: make sure it's int not float
    sensors_meassurement:  dict[int, list[float]] = None

@dataclass
class TestMap:
    timestamp: list[int] #TODO: make sure it's int not float
    setpoint:  list[int] #TODO: make sure it's int not float


class SystemEngine:
    def __init__(self, data_logger, sensor_reader, server_connections: list[ServerInstance]):
        self.data_logger = data_logger
        
        #TODO: fix it (remove motor_controler instance)
        self.server_connections = server_connections

        self.sensor_reader = sensor_reader
  
        self.velocity_setpoint = 0
        self.meassurement_time = 0
        
        self.test_map_speed = TestMap(timestamp=[0, 5, 10], setpoint=[0, 300, 500]) #TODO: wrap testmaps in dictionary
        self.test_map_torque = TestMap(timestamp=[0, 5, 10], setpoint=[0, 100, 200])
        
        self.map_test_startup_time = None

        self.velocity_plots = {
                                ServerId.motor_drive: VelocityPlot(meassurement_time=[], rpm=[]),
                                ServerId.load_drive: VelocityPlot(meassurement_time=[], rpm=[])
        }
        
        self.torque_plots = {
                                ServerId.motor_drive: TorquePlot(meassurement_time=[], torque=[]),
                                ServerId.load_drive: TorquePlot(meassurement_time=[], torque=[])
        }

        self.sensor_meassurement_plots = SensorMeasurementPlot()

        self.MAP_CONTROL = 12
        self.SETPOINT_CONTROL = 73
        self.control = self.SETPOINT_CONTROL

        self.thread = None
        self.test_active = False
        self.lock = threading.Lock()

        self.TEST_RUN_TIME = 10 #[s]
        self.MAX_MOTOR_SPEED = 3000 #[rpm]
        self.MAX_LOAD_TORQUE = 350 #TODO: check this value


    def get_server(self, server_id: ServerId) -> ServerInstance:
        #TODO: make mutex?
        return self.server_connections[server_id]

    def initialize(self):
        for server in self.server_connections.values():
            if server is not None:
                print(server)
                server.initialize()

    def set_control_type(self, control_type): #TODO: remove this function
        if control_type != self.MAP_CONTROL and control_type != self.SETPOINT_CONTROL:
            print("not a proper control type")
            return
        self.control = control_type

    def get_measurements(self): #TODO: consider switching to queue
        with self.lock:
            return copy.deepcopy(self.sensor_meassurement_plots) #TODO: make sure we dont need a deep copy here, return a copy to avoid race conditions
    
    def get_motor_test_map(self, drive: ServerId):
        #TODO: add mutex
        #TODO: consider a deep copy
        if drive == ServerId.motor_drive:
            return self.test_map_speed
        elif drive == ServerId.load_drive:
            return self.test_map_torque
        #TODO: throw exeption in else


    def clean_test_maps(self):
        self.test_map_speed = TestMap(timestamp=[0], setpoint=[0])
        self.test_map_torque = TestMap(timestamp=[0], setpoint=[0])

    def set_motor_test_map_speed(self, test_map): #TODO: change as in get_motor_test_map
        #TODO: consider a deep copy
        self.test_map_speed.timestamp = test_map.timestamp #TODO: add mutex
        self.test_map_speed.setpoint = test_map.setpoint

    def set_motor_test_map_torque(self, test_map): #TODO: change as in get_motor_test_map
        #TODO: consider a deep copy
        self.test_map_torque.timestamp = test_map.timestamp #TODO: add mutex
        self.test_map_torque.setpoint = test_map.setpoint

    def set_velocity(self, velocity):
        #add mutex
        self.velocity_setpoint = velocity

    def get_velocity_plots(self) -> dict[ServerId: VelocityPlot]:
        with self.lock:
            #TODO: consider deep copy
            return self.velocity_plots

    def get_torque_plots(self) -> dict[ServerId: TorquePlot]:
        with self.lock:
            #TODO: consider deep copy
            return self.torque_plots
        

    def get_time(self):
        return self.meassurement_time

    def set_map_test_time(self, new_time):
        self.TEST_RUN_TIME = new_time

    def get_torque_map_size(self):
        scale_ratio = self.TEST_RUN_TIME/(4*self.MAX_LOAD_TORQUE)
        return self.TEST_RUN_TIME, self.MAX_LOAD_TORQUE, scale_ratio
    
    def get_speed_map_size(self):
        scale_ratio = self.TEST_RUN_TIME/(4*self.MAX_MOTOR_SPEED)
        return self.TEST_RUN_TIME, self.MAX_MOTOR_SPEED, scale_ratio

    def monitor_meassurements(self):
        # TODO: if temp is not in proper range, disable testing
        # TODO: if torque is not in proper range, disable testing?
        # TODO: if motor_speed is not in proper range, disable testing?

        # TODO: other dangerous cases?
        pass

    def test_running(self):
        return self.test_active

    def update_meassurements_plot(self, meassurement_time, meassurements: dict[int, float]):
        #TODO: add mutexes

        if self.sensor_meassurement_plots.meassurement_time is None:
            self.sensor_meassurement_plots.meassurement_time = []
        if self.sensor_meassurement_plots.sensors_meassurement is None:
            self.sensor_meassurement_plots.sensors_meassurement = {}

        self.sensor_meassurement_plots.meassurement_time.append(meassurement_time)        
            
        if len(self.sensor_meassurement_plots.meassurement_time) > MAX_SENSOR_PLOT_MEASURMENTS: 
            self.sensor_meassurement_plots.meassurement_time = self.sensor_meassurement_plots.meassurement_time[-MAX_SENSOR_PLOT_MEASURMENTS:]

        for sensor_id, meassurement_data in meassurements.items():
            series = self.sensor_meassurement_plots.sensors_meassurement.setdefault(sensor_id, [])
            series.append(meassurement_data)                     

            if len(series) > MAX_SENSOR_PLOT_MEASURMENTS:
                self.sensor_meassurement_plots.sensors_meassurement[sensor_id] = series[-MAX_SENSOR_PLOT_MEASURMENTS:]

    def update_velocity_plots(self, meassurement_time):
        for drive_type, plot_data in self.velocity_plots.items():
            velocity = self.server_connections[drive_type].get_speed() #TODO: make sure it doesnt block controller (mutex)

            if len(plot_data.meassurement_time) > MAX_DRIVE_PLOT_MEASURMENTS:
                plot_data.rpm.pop(0)
                plot_data.meassurement_time.pop(0)

            plot_data.rpm.append(velocity)
            plot_data.meassurement_time.append(meassurement_time)

    def update_torque_plots(self, meassurement_time):
        for drive_type, plot_data in self.torque_plots.items():
            torque = self.server_connections[drive_type].get_torque() #TODO: make sure it doesnt block controller (mutex)

            if len(plot_data.meassurement_time) > MAX_DRIVE_PLOT_MEASURMENTS:
                plot_data.torque.pop(0)
                plot_data.meassurement_time.pop(0)

            plot_data.torque.append(torque)
            plot_data.meassurement_time.append(meassurement_time)

    def run_motor_maps(self, current_time):
        # for drive in self.server_connections.keys():
        #     testmap = self.get_motor_test_map(drive)
        #     self.server_connections[drive].run_motor_map(current_time, testmap.timestamp, testmap.setpoint)    
        motor_drive = self.server_connections[ServerId.motor_drive]
        load_drive = self.server_connections[ServerId.load_drive]


        testmap_motor_drive = self.get_motor_test_map(ServerId.motor_drive)
        motor_drive.run_motor_map_speed(current_time, testmap_motor_drive.timestamp, testmap_motor_drive.setpoint)      

        testmap_load_drive = self.get_motor_test_map(ServerId.load_drive)
        load_drive.run_motor_map_torque(current_time, testmap_load_drive.timestamp, testmap_load_drive.setpoint)      


    def motor_data_processing(self, test_time):
        self.meassurement_time = test_time #TODO: set correct time for measurements
        meassurements, _ = self.sensor_reader.read_all()

        with self.lock: #TODO: chceck all the mutexes
            self.update_meassurements_plot(test_time, meassurements) #TODO:make sure those plots arent updated to often
            
            self.update_velocity_plots(test_time)
            self.update_torque_plots(test_time)
            
        #TODO: add torque, speed etc to meassuremets
        self.data_logger.log(meassurements)
        
        if self.monitor_meassurements():
            self.server_connections[ServerId.motor_drive].reset()
            #TODO: disable testing
            self.map_test_startup_time = None
            raise Exception("Motor control error")

    def reset_velocity_plots(self):
        self.velocity_plots = {
            ServerId.motor_drive: VelocityPlot(meassurement_time=[], rpm=[]),
            ServerId.load_drive: VelocityPlot(meassurement_time=[], rpm=[])
        }

    def reset_torque_plots(self):
        self.torque_plots = {
            ServerId.motor_drive: TorquePlot(meassurement_time=[], torque=[]),
            ServerId.load_drive: TorquePlot(meassurement_time=[], torque=[])
        }

    def motor_map(self):
        self.map_test_startup_time = time.time()
        self.reset_velocity_plots()
        self.reset_torque_plots()

        while self.server_connections[ServerId.motor_drive].running():
            current_time = time.time() - self.map_test_startup_time
            
            are_motor_drives_connected = self.server_connections[ServerId.motor_drive].get_connection_status().connected and self.server_connections[ServerId.load_drive].get_connection_status().connected
            # are_motor_drives_connected = self.server_connections[ServerId.motor_drive].get_connection_status().connected #TODO: remove this stub
            if current_time > self.TEST_RUN_TIME or (not are_motor_drives_connected):
                self.server_connections[ServerId.motor_drive].disable_motors() #TODO: handle disabling properly, TODO:maybe make class for storing and disabling both drives
                break

            self.motor_data_processing(current_time)
            
            self.run_motor_maps(current_time)   #TODO: make sure the setpoint isnt set to often

            time.sleep(MEASUREMENT_TIME)

        #TODO: handle disabling map test corectly
        self.map_test_startup_time = None

    def test_execution(self):  
        self.test_active = True 
        while True: #TODO: clean while loops here (motor_map)
            #TODO: pack test into functions
            if self.server_connections[ServerId.motor_drive].running():
                try:
                    if self.control == self.MAP_CONTROL:
                        self.motor_map()

                except Exception as e:
                    # ensure motors are disabled at the end of the test
                    self.test_active = False
                    self.server_connections[ServerId.motor_drive].reset()
                    print("test_execution() error: ", e)
                    #TODO: test if throwing exeptions is working in both scenerios
            
            #TODO: handle motor disabling properly
            time.sleep(MEASUREMENT_TIME) #TODO: refactor this function so this thread doesnt block the whole program