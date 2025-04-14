# 使用官方 Python 映像檔
FROM python:3.10-slim

# 設定工作目錄
WORKDIR /app

# 複製需求檔
COPY requirements.txt .

# 安裝必要套件
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式所有檔案到 container 中
COPY . .

# 預設啟動指令（使用 uvicorn 啟動 FastAPI）
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]