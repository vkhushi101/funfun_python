from collections import defaultdict
from enum import Enum
import re, csv, json
from datetime import datetime
import pytz
from typing import Dict
from fastapi import FastAPI, Query, Depends
import uvicorn

app = FastAPI()

class Device(Enum):
    SENSOR="sensor"
    CAMERA="camera"
    THERMOSTAT="thermostat"
    UNKNOWN="unknown"
    @classmethod
    def get_device_type(cls, device_type: str):
        return cls._value2member_map_.get(device_type, cls.UNKNOWN).name
    
class Health(Enum):
    HEALTHY=100
    WARNING=50
    CRITICAL=0
    UNKNOWN=-1
    @classmethod
    def get_health_value(cls, health_status: str):
        return cls.__members__.get(health_status.upper(), cls.UNKNOWN)

class DeviceDataProcessor:
    def __init__(self):
        self.jsons = defaultdict(list)

    def _append_to_jsons_list(self, entry):
        device_type = Device.get_device_type(entry["device_type"])
        entry["device_type"] = device_type
        if str(entry["device_id"]) not in map(lambda x: x["device_id"], self.jsons[device_type]):
            self.jsons[device_type].append(entry)

    def load_csv_to_jsons(self, filename: str):
        with open(filename, 'r') as csvfile:
            for entry in csv.DictReader(csvfile):
                metric_data = {
                    "temperature": entry["temperature"],
                    "humidity": entry["humidity"],
                    "pressure": entry["pressure"]
                }
                for key in ["temperature", "humidity", "pressure"]:
                    del entry[key]
                entry["metric_data"] = metric_data
                self._append_to_jsons_list(entry)

    def load_json_file_to_jsons(self, json_filename):
        with open(json_filename, 'r') as jsonfile:
            for entry in json.load(jsonfile):
                self._append_to_jsons_list(entry)

    def _format_timestamp(self, timestamp: str) -> str:
        iso8601_regex = r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)'
        match = re.match(iso8601_regex, timestamp)
        if match:
            local_time = datetime.strptime(match[0], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.utc)
            return local_time.strftime("%Y-%m-%d")
        return None

    def _convert_degrees(self, degrees_F):
        return round((int(degrees_F) - 32) * 5 / 9, 2)

    def _normalize_pressure(self, pressure):
        return round(int(pressure) / 100, 2)

    def _normalize_humidity(self, humidity):        
        return f"{humidity}%"

    def _create_full_name(self, device_name, device_type):
        return device_name + device_type

    def sanitize_and_transform(self) -> Dict[any, any]:
        for v in self.jsons.values(): 
            for j in v[:]:
                valid_timestamp = self._format_timestamp(j["timestamp"])
                if not valid_timestamp:
                    v.remove(j)
                    continue
                j["timestamp"] = valid_timestamp
                j["metric_data"]["temperature"] = self._convert_degrees(j["metric_data"]["temperature"])
                j["metric_data"]["pressure"] = self._normalize_pressure(j["metric_data"]["pressure"])
                j["metric_data"]["humidity"] = self._normalize_humidity(j["metric_data"]["humidity"])
                j["health_score"] = Health.get_health_value(j["health_status"]).value
                del j["health_status"]
                j["device_full_name"] = self._create_full_name(j["device_name"], j["device_type"])
        return self.jsons

    def sort_and_filter_data(self):
        return {
            k: sorted(
                [entry for entry in v if entry["health_score"] != -1],
                key=lambda x: x["health_score"]
            )
            for k, v in self.jsons.items() 
            if k != Device.UNKNOWN.name
        }


processor = DeviceDataProcessor()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/csv_to_json")
def load_csv_to_json(filename: str = Query(...)):
    processor.load_csv_to_jsons(filename)
    return {"status": "loaded"}

@app.post("/json_to_json/{filename}")
def load_json_to_json(filename: str):
    processor.load_json_file_to_jsons(filename)
    return {"status": "json loaded"}

@app.post("/sanitize")
def sanitize_data():
    return json.dumps(processor.sanitize_and_transform(), indent=2)

@app.get("/result")
def get_sorted_filtered_data():
    return json.dumps(processor.sort_and_filter_data(), indent=2)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
