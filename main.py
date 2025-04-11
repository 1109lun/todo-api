from database import SessionLocal
from fastapi import FastAPI
from sqlalchemy import text

app = FastAPI()

@app.get("/test-db")

def test_db() :
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        return {"message": "Database connection is working!"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()