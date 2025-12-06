#1. log loccaly into files
# 2. publish via mqtt
# 3. monitor meassurements during test (web page?)
#TODO: consider batching writes in order to reduce number of file opens/closes
#TODO: consider using USB filesystem instead of SD card for better durability

from abc import ABC, abstractmethod
from datetime import datetime, timezone
import csv
import os

class StorageBackend(ABC):
    @abstractmethod
    def save(self, data: dict):
        pass

class MqttPublisher(ABC):
    @abstractmethod
    def send(self, data: dict):
        pass

class CSVStorage(StorageBackend):
    def __init__(self, file_dir: str):
        self.filename = self.create_filename(file_dir)
        self.fieldnames = None  # dynamically set on first log

    def create_filename(self, file_dir: str) -> str:
        # Ensure directory exists
        os.makedirs(file_dir, exist_ok=True)

        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        return f"{file_dir}data_log_{timestamp}.csv"
        
    def save(self, data: dict):
        if self.fieldnames is None:
            self.fieldnames = list(data.keys())
            with open(self.filename, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
                writer.writerow(data)
        else:
            with open(self.filename, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writerow(data)

class DataLogger:
    def __init__(self, storage: StorageBackend, publisher: MqttPublisher = None):
        self.storage = storage
        self.publisher = publisher

    def log(self, measurement: dict):
        """Add timestamp and save/send measurement"""
        measurement_with_time = {"timestamp": datetime.now(timezone.utc).isoformat(), **measurement}
        
        # Save locally
        self.storage.save(measurement_with_time)
        # publish
        if self.publisher:
            self.publisher.send(measurement_with_time)