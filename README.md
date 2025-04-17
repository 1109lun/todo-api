# FastAPI x Docker x VM 部署說明文件

## 📌 專案簡介
本專案為一個使用 FastAPI 撰寫的 To-Do List 待辦清單 API，從零開始練習建構完整的後端系統，包含：
- 建立 RESTful API
- 使用 Docker 運行 PostgreSQL 資料庫
- 整合資料庫與 FastAPI
- 使用 Alembic 進行資料表管理
- 最後使用 Docker + SSH 將專案部署至遠端 VM

---

## 🧱 技術與工具
- Python 3.x + FastAPI + Uvicorn
- PostgreSQL 資料庫（Docker container 運行）
- SQLAlchemy + Alembic 做資料表定義與管理
- Docker / Docker Compose
- SSH tunnel 映射 port
- DockerHub 託管 image
- .env 環境變數管理

---

## 🚧 3-2 使用 Docker 運行 PostgreSQL

### 步驟流程：
1. 安裝 Docker Engine（使用 CLI）或 Docker Desktop（有 GUI）
2. 使用 `docker-compose` 啟動 Postgres：

```yaml
db:
  image: postgres:15
  restart: always
  environment:
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: password
    POSTGRES_DB: todo_db
  volumes:
    - pgdata:/var/lib/postgresql/data
volumes:
  pgdata:
```

3. 進入 container：
```bash
docker exec -it <container_id> psql -U postgres -d todo_db
```
並執行幾條 SQL 新增資料確認資料存在。

4. 重啟 container，資料仍在即為成功使用 volume。

---

## 🧠 .env 設定建議

.env
```
DATABASE_URL=postgresql://postgres:password@db:5432/todo_db
```
並使用 `python-dotenv` 或 FastAPI `Settings` 模組讀取。

將 `.env` 加入 `.gitignore`，避免敏感資訊被上傳：
```
.env
```

---

## 🛠️ 3-3 建立待辦清單 API（FastAPI）

### 功能需求：
- 任務管理 CRUD：
  - `POST /task`
  - `GET /project/{project_id}/task`
  - `PUT /task/{task_id}`
  - `DELETE /task/{task_id}`
- 專案管理 CRUD：
  - `POST /project`
  - `GET /projects`
  - `DELETE /project/{id}` → 同時刪除對應任務

### 注意：
- 回傳需正確 HTTP 狀態碼（2xx 成功 / 4xx 錯誤）
- CRUD 遵循 REST 命名規則
- 使用 SQLAlchemy 定義資料表（Project、Task）
- 使用 Alembic 建立 migration 管理版本

---

## 🚀 3-4 使用 Docker + SSH 部署

### 本機建立 Docker image 並上傳 DockerHub
```bash
docker build --platform=linux/amd64 -t lugchy/todo-api:latest .
docker push lugchy/todo-api:latest
```

### 在 VM 上 Pull & Run
```bash
ssh ylchang@140.116.247.125 -p 23822
# 密碼登入（netdb）

# 在 VM 上拉 image
sudo docker pull lugchy/todo-api:latest
sudo docker run -d -p 8000:8000 lugchy/todo-api:latest
```

### 開啟 SSH Tunnel 在本機預覽
```bash
ssh -L 8000:localhost:8000 ylchang@140.116.247.125 -p 23822
```
本地瀏覽器開啟： http://localhost:8000/docs

---

## ✅ 成果驗收標準
- 成功執行 `docker run`，container 保持在背景中持續運行
- 資料庫 volume 正確運作，重啟後資料不會遺失
- API 回應正確、Swagger UI 可操作
- SSH tunnel 能在本機成功開啟 `/docs`
- .env 無誤，未被上傳至 GitHub

---

## 🎯 學習重點與收穫
- 從本地開發過渡到遠端部署的完整後端開發流程
- 使用 Docker 封裝與環境一致性
- 熟悉 PostgreSQL + SQLAlchemy + Alembic 流程
- 熟悉 RESTful API 設計與 FastAPI 開發
- 熟悉 SSH tunnel、container log、錯誤排查與多平台部署

---