from database import SessionLocal
from fastapi import FastAPI , HTTPException , Depends , status
from sqlalchemy.orm import Session
import models , schemas

app = FastAPI()

def get_db() :
    db = SessionLocal()
    try :
        yield db
    finally :
        db.close()

@app.post("/tasks" , response_model = schemas.TaskInDB , status_code=status.HTTP_201_CREATED)

def create_task(task : schemas.TaskCreate , db : Session = Depends(get_db)) :
    project = db.query(models.Project).filter(models.Project.id == task.project_id).first()
    if not project :
        raise HTTPException(status_code = 404 , detail = "Project not found")
    
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/projects/{project_id}/tasks" , response_model = list[schemas.TaskInDB])

def get_tasks(project_id : int , db : Session = Depends(get_db)) :
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project :
        raise HTTPException(status_code = 404 , detail = "Project not found")
    return project.tasks

@app.delete("/tasks/{task_id}" , status_code=status.HTTP_204_NO_CONTENT)

def delete_task(task_id : int , db : Session = Depends(get_db)) :
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task :
        raise HTTPException(status_code = 404 , detail = "Task not found")
    
    db.delete(task)
    db.commit()
    return {"message" : "Task deleted successfully"}

@app.put("/tasks/{task_id}")

def update_task(task_id : int , updated_task : schemas.TaskUpdate , db : Session = Depends(get_db) ) :
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task :
        raise HTTPException(status_code = 404 , detail = "Task not found")
    
    for key , value in updated_task.model_dump(exclude_unset=True).items() :
        setattr(task , key , value)

    db.commit()
    db.refresh(task)
    return {"message" : "Task updated successfully"}

@app.post("/projects" , response_model = schemas.ProjectInDB , status_code=status.HTTP_201_CREATED)

def create_project(project : schemas.ProjectCreate , db : Session = Depends(get_db)) :
    db_project = models.Project(name = project.name)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@app.get("/projects" , response_model = list[schemas.ProjectInDB])

def get_projects(db : Session = Depends(get_db)) :
    projects = db.query(models.Project).all()
    return projects

@app.get("/projects/{project_id}" , response_model = schemas.ProjectInDB)

def get_project(project_id : int , db : Session = Depends(get_db)) :
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project :
        raise HTTPException(status_code = 404 , detail = "Project not found")
    return project

@app.delete("/projects/{project_id}" , status_code=status.HTTP_204_NO_CONTENT)

def delete_project(project_id : int , db : Session = Depends(get_db) ) :
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project :
        raise HTTPException(status_code = 404 , detail = "Project not found")
    
    db.delete(project)
    db.commit()
    return {"message" : "Project deleted successfully"}

@app.put("/projects/{project_id}")   
def update_project(project_id : int , updated_project : schemas.ProjectBase , db : Session = Depends(get_db)) :
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project :
        raise HTTPException(status_code = 404 , detail = "Project not found")
    
    for key , value in updated_project.model_dump(exclude_unset=True).items() :
        setattr(project , key , value)

    db.commit()
    db.refresh(project)
    return {"message" : "Project updated successfully"}
