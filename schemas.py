from pydantic import BaseModel
from typing import Optional
from datetime import date

class TaskBase (BaseModel) :
    title : str
    description : Optional[str] = ""
    due_date : Optional[date] = None
    priority : Optional[str] = "low"
    completed : Optional[bool] = False

class TaskCreate (TaskBase) :
    project_id : int
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None
    priority: Optional[str] = None
    completed: Optional[bool] = None

class TaskInDB (TaskBase) :
    id : int
    project_id : int

    class Config :
        orm_mode = True

class ProjectBase (BaseModel) :
    name : str

class ProjectCreate (ProjectBase) : 
    pass

class ProjectInDB (ProjectBase) :
    id : int
    class Config:
        from_attributes = True
