import psycopg2
from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI()

class DeviceStatus(BaseModel):
    pcname: str
    program: str
    status: str
    errs: int

# Kết nối đến PostgreSQL (thay SQLite)
def connect_db():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    return conn

# Tạo bảng trong PostgreSQL nếu chưa có
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS devices 
                    (pcname TEXT PRIMARY KEY, program TEXT, status TEXT, errs INTEGER)''')
    conn.commit()
    conn.close()

# Gọi hàm tạo bảng khi ứng dụng khởi động
create_table()

# Lưu trạng thái vào cơ sở dữ liệu PostgreSQL
def save_to_db(status: DeviceStatus):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO devices (pcname, program, status, errs) 
                      VALUES (%s, %s, %s, %s) ON CONFLICT (pcname) DO UPDATE 
                      SET status = EXCLUDED.status, errs = EXCLUDED.errs''', 
                   (status.pcname, status.program, status.status, status.errs))
    conn.commit()
    conn.close()

# Lấy tất cả dữ liệu từ PostgreSQL
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
        if not devices:
            return {"message": "No devices found"}
        return {"devices": devices}
    except Exception as e:
        print(f"Error in get_all_status: {e}")
        return {"error": f"Failed to retrieve status: {e}"}
