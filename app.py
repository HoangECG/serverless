from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

app = FastAPI()

class DeviceStatus(BaseModel):
    pcname: str
    program: str
    status: str
    errs: int

json_file_path = "device_status.json"

def load_data():
    try:
        if os.path.exists(json_file_path):
            with open(json_file_path, "r") as f:
                return json.load(f)
        else:
            return []  # Trả về danh sách trống nếu file không tồn tại
    except Exception as e:
        print(f"Error loading data from {json_file_path}: {e}")
        return []

def save_to_json(data):
    try:
        with open(json_file_path, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving data to {json_file_path}: {e}")

@app.post("/status/")
async def update_status(status: DeviceStatus):
    print(f"Received data: {status.dict()}")  # Debug log

    try:
        existing_data = load_data()

        device_exists = False
        for device in existing_data:
            if device["pcname"] == status.pcname:
                device["status"] = status.status
                device["errs"] = status.errs
                device_exists = True
                break

        if not device_exists:
            existing_data.append(status.dict())

        save_to_json(existing_data)
        return {"message": "Status updated successfully!"}
    except Exception as e:
        print(f"Error in update_status: {e}")
        return {"error": "Failed to update status"}

@app.get("/status/")
async def get_all_status():
    try:
        existing_data = load_data()
        return {"devices": existing_data}
    except Exception as e:
        print(f"Error in get_all_status: {e}")
        return {"error": "Failed to retrieve status"}
