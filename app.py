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
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as f:
            return json.load(f)
    return []

def save_to_json(data):
    with open(json_file_path, "w") as f:
        json.dump(data, f, indent=4)

@app.post("/status/")
async def update_status(status: DeviceStatus):
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

@app.get("/status/")
async def get_all_status():
    # Lấy dữ liệu từ file JSON
    existing_data = load_data()
    return {"devices": existing_data}
