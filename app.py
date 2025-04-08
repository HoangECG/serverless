from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

class DeviceStatus(BaseModel):
    pcname: str
    program: str
    status: str
    errs: int

# Kết nối đến cơ sở dữ liệu SQLite
def connect_db():
    conn = sqlite3.connect("device_status.db")
    return conn

# Tạo bảng trong database nếu chưa có
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS devices 
                    (pcname TEXT PRIMARY KEY, program TEXT, status TEXT, errs INTEGER)''')
    conn.commit()
    conn.close()

# Lưu trạng thái vào cơ sở dữ liệu
def save_to_db(status: DeviceStatus):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''INSERT OR REPLACE INTO devices (pcname, program, status, errs) 
                      VALUES (?, ?, ?, ?)''', (status.pcname, status.program, status.status, status.errs))
    conn.commit()
    conn.close()

# Lấy tất cả dữ liệu từ cơ sở dữ liệu
def load_from_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM devices')
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.post("/status/")
async def update_status(status: DeviceStatus):
    try:
        save_to_db(status)
        return {"message": "Status updated successfully!"}
    except Exception as e:
        print(f"Error in update_status: {e}")
        return {"error": "Failed to update status"}

@app.get("/status/")
async def get_all_status():
    try:
        devices = load_from_db()
        return {"devices": devices}
    except Exception as e:
        print(f"Error in get_all_status: {e}")
        return {"error": "Failed to retrieve status"}
