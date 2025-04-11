from database import SessionLocal
from fastapi import FastAPI , HTTPException , Depends
from sqlalchemy.orm import Session
import models , schemas

app = FastAPI()

def get_db() :
    db = SessionLocal()
    try :
        yield db
    finally :
        db.close()

@app.post("/task" , response_model = schemas.TaskInDB)

def create_task(task : schemas.TaskCreate , db : Session = Depends(get_db)) :
    project = db.query(models.Project).filter(models.Project.id == task.project_id).first()
    if not project :
        raise HTTPException(status_code = 404 , detail = "Project not found")
    
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

