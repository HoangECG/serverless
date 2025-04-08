from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Sử dụng dictionary để lưu trạng thái
device_status_dict = {}

class DeviceStatus(BaseModel):
    pcname: str
    program: str
    status: str
    errs: int

@app.post("/api/")
async def update_status(status: DeviceStatus):
    try:
        # Lưu trạng thái vào dictionary
        device_status_dict[status.pcname] = {
            "program": status.program,
            "status": status.status,
            "errs": status.errs
        }
        return {"message": "Status updated successfully!"}
    except Exception as e:
        print(f"Error in update_status: {e}")
        return {"error": "Failed to update status"}

@app.get("/api/")
async def get_all_status():
    try:
        # Trả về tất cả trạng thái từ dictionary
        if not device_status_dict:
            return {"message": "No devices found"}

        # Sắp xếp các card: đưa những card không phải "running" lên trên
        sorted_devices = sorted(device_status_dict.items(), key=lambda x: x[1]["status"] != "running", reverse=False)

        # Chuyển đổi lại thành dictionary sau khi sắp xếp
        sorted_device_dict = {pcname: status for pcname, status in sorted_devices}

        return {"devices": sorted_device_dict}
    except Exception as e:
        print(f"Error in get_all_status: {e}")
        return {"error": f"Failed to retrieve status: {e}"}
