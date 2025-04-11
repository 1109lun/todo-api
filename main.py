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

@app.get("/project/{project_id}/task" , response_model = list[schemas.TaskInDB])

def get_tasks(project_id : int , db : Session = Depends(get_db)) :
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project :
        raise HTTPException(status_code = 404 , detail = "Project not found")
    return project.tasks

@app.delete("/task/{task_id}")

def delete_task(task_id : int , db : Session = Depends(get_db)) :
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task :
        raise HTTPException(status_code = 404 , detail = "Task not found")
    
    db.delete(task)
    db.commit()
    return {"message" : "Task deleted successfully"}

