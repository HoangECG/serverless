import requests
import json

# Thông tin của Google Sheets
sheet_id = '1fQ-Q-5Rh-ir52kqxY7w2faiHGBH581m-riPA4CnQipY'
range_ = 'Sheet1!A1'  # Vị trí bắt đầu của dữ liệu
api_key = 'AIzaSyARx2UnEZ_gUra4BNBc6_xGYkTX-7TvWDY'

# Dữ liệu cần ghi
data = {
    "values": [
        ["Name", "Age"],
        ["Alice", 30],
        ["Bob", 25]
    ]
}

# URL của Google Sheets API
url = f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{range_}?valueInputOption=RAW&key={api_key}'

# Gửi yêu cầu PUT để cập nhật dữ liệu
response = requests.put(url, json=data)

# Kiểm tra kết quả
if response.status_code == 200:
    print("Dữ liệu đã được cập nhật thành công!")
else:
    print(f"Error: {response.status_code}, {response.text}")
