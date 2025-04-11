from database import SessionLocal
from fastapi import FastAPI , HTTPException
from sqlalchemy import text

app = FastAPI()

